import re
import os
import time
import pickle
import openai
import random

import pandas as pd
import numpy as np

# TODO: Handpick examples that display optional, exclusive and essential actions
# TODO: Put Exclusive actions like (act1() or act2() or act3())
# TODO: Test optional objects better
def get_acts_objs(acts_text):
    acts = [act.split("(")[0].strip() for act in acts_text.split("),") if act.split("(")[0].strip() != ""]
    objs_list = re.findall(r'\((.*?)\)', acts_text)

    objs = []
    for obj in objs_list:
        objs += obj.split(",")

    return acts, objs


def compute_f1_acts(true_dict, preds):
    true_objs = []
    type = "acts"
    essential = true_dict["essential"][type].copy()
    optional = true_dict["optional"][type].copy()
    exclusive = true_dict["exclusive"][type].copy()
    words = test_data["words"]

    total_tagged = len(preds)
    total_truth = len(essential) + len(exclusive)
    right_es, right_op, right_ex = 0, 0, 0
    for item in preds:
        if item in essential:
            right_es += 1
            true_objs += true_dict["essential"]["act_obj"][essential.index(item)][1]    # Add the corresponding objects
            essential.remove(item)  # Removes from the left

        elif item in optional:
            right_op += 1
            total_truth += 1
            true_objs += true_dict["optional"]["act_obj"][optional.index(item)][1]      # Add the corresponding objects
            optional.remove(item)

    for item_list in exclusive:
        item_list_w = [words[w_id] for w_id in item_list]
        intersect = set(item_list_w).intersection(preds)
        # There can only appear 1 exclusive action amongst the predictions
        if len(intersect) == 1:
            right_ex += 1
            i = item_list_w.index(list(intersect)[0])           # Find the object indices of the matched action
            act_objs = [words[w_id] for w_id in test_data["acts2objs"][item_list[i]]]
            true_objs += act_objs

    total_right = right_es + right_op + right_ex
    precision = total_right / total_tagged
    recall = total_right / total_truth
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1, true_objs


def compute_f1_objs(true, preds):
    total_right = 0
    total_truth = len(true)
    total_tagged = len(preds)
    true_cpy = true.copy()

    if total_truth == 0 or total_tagged == 0:
        return 0.0, 0.0, 0.0

    for item in preds:
        if item in true_cpy:
            total_right += 1
            true_cpy.remove(item)

    precision = total_right / total_tagged
    recall = total_right / total_truth
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1


def get_data(sample, max_sents):
    # Action | (Objs) | Type
    data = {
        "data_id": [],
        "data_str": [],
        "related": {},
        "acts2objs": {},
        "sents": [],
        "words": sample["words"],
        "word2sent": sample["word2sent"]
    }

    data_id = data["data_id"]
    data_str = data["data_str"]
    related = data["related"]
    acts2objs = data["acts2objs"]
    ws = sample["words"]

    # Get maximum word id of the last action in the last sentence
    last_w, max_sents = 0, min(max_sents, len(sample["sents"]))
    for s in sample["sents"][:max_sents]:
        last_w += len(s)
        data["sents"].append(s)

    for act_dict in sample["acts"]:
        act_idx = act_dict['act_idx']
        if act_idx > last_w-1: break
        obj_idxs = act_dict['obj_idxs'][0]

        related[act_idx] = act_dict["related_acts"]
        data_id.append([act_idx, obj_idxs, act_dict['act_type']])

        act_w, objs_w = ws[act_idx].lower(), [ws[obj].lower() for obj in obj_idxs]
        data_str.append([act_w, objs_w, act_dict['act_type']])

        acts2objs[act_idx] = obj_idxs

    return data


def get_query_strs(data):
    text_str = ""
    for s in data["sents"]:
        text_str += " ".join(s) + ".\n"

    acts_str = ""
    for (act, objs, id) in data["data_str"]:
        acts_str += "{}({}), ".format(act, ",".join(objs))

    acts_str = acts_str[:-2]  # remove last comma
    return text_str, acts_str


def send_query_gpt3(query):
    print("Sending query...", end=" ")
    start = time.time()
    response = openai.Completion.create(
        engine=gpt3_engine,
        prompt=query,
        temperature=gpt3_temp,
        max_tokens=gpt3_max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print("{:.2f}s elapsed".format(time.time() - start))
    text_response = response["choices"][0]["text"]

    return text_response


def get_test_dict(data):
    test_dict = {
        "essential": {
            "act_obj": [],
            "acts": [],
            "objs": []
        },
        "optional": {
            "act_obj": [],
            "acts": [],
            "objs": []
        },
        "exclusive": {
            "act_obj": {},
            "acts": [],
            "objs": []
        },
    }

    related = data["related"]
    acts = set()
    for act in related:
        rel = related[act]
        if len(rel) > 0:
            aux = [act] + rel
            aux.sort()
            acts.add(tuple(aux))
    test_dict["exclusive"]["acts"] = list(acts)

    acts2objs = data["acts2objs"]
    for acts in test_dict["exclusive"]["acts"]:
        test_dict["exclusive"]["objs"].append([acts2objs[act] for act in acts])

    types = list(test_dict.keys())
    for (act, objs, type), (act_id, objs_id, _) in zip(data["data_str"], data["data_id"]):
        es_op_ex = test_dict[types[type - 1]]
        if types[type - 1] != "exclusive":
            es_op_ex["act_obj"].append([act, objs])
            es_op_ex["acts"].append(act)
            es_op_ex["objs"].append(objs)

    return test_dict


if __name__ == '__main__':
    wiki = pickle.load(open("EASDRL/data/wikihow_labeled_text_data.pkl", "rb"))
    win = pickle.load(open("EASDRL/data/win2k_labeled_text_data.pkl", "rb"))
    cook = pickle.load(open("EASDRL/data/cooking_labeled_text_data.pkl", "rb"))
    _ = pickle.load(open("EASDRL/data/cooking_dependency.pkl", "rb"))

    # ================= Params =================
    random.seed(42)
    ENGINES = ["babbage", "ada"]  #["davinci", "curie", "babbage", "ada"]
    DOMAINS = {"win": win, "cook": cook, "wiki": wiki}

    gpt3_engine = "babbage"  # davinci, curie, babbage, ada
    gpt3_temp = 0.0  # Set to 0 for reproducibility
    gpt3_max_tokens = 150

    results_file = "data.csv"
    openai.api_key = os.environ["OPENAI_API_KEY"]
    n_examples = 2  # The amount of text cannot go over 2048
    n_runs = 1
    max_sents = 15
    cnt = n_runs
    count_unfinished_responses = True
    tags = ["\n\nTEXT: \n", "\nACTIONS: \n"]
    # ==========================================

    for gpt3_engine in ENGINES:
        for domain_name in DOMAINS:
            domain = DOMAINS[domain_name]
            # precision, recall, f1: [actions, objects]
            results = {"precision": [0, 0], "recall": [0, 0], "f1": [0, 0]}

            print("ENGINE: {} | DOMAIN: {}".format(gpt3_engine, domain_name))
            print("-" * 28)

            for i in range(n_runs):
                print("[+] RUN {}:".format(i), end=" ")

                # Randomly sample text sequences from the domain
                samples = random.sample(domain, n_examples + 1)
                # train_samples = domain[1:n_examples + 1]
                # test_sample = domain[0]  # domain[n_examples:n_examples + 1]
                train_samples = samples[:n_examples]
                test_sample = samples[n_examples: n_examples+1][0]

                query = ""
                for sample in train_samples:
                    data_sample = get_data(sample, max_sents)
                    text_str, acts_str = get_query_strs(data_sample)
                    query += tags[0] + text_str + tags[1] + acts_str

                test_data = get_data(test_sample, max_sents)
                text_str_test, _ = get_query_strs(test_data)

                query += tags[0] + text_str_test + tags[1]
                query = query.strip()

                test_true_dict = get_test_dict(test_data)

                # ----- Send query to GPT3 and check correct output -----
                gpt3_response = send_query_gpt3(query)
                if not count_unfinished_responses and tags[0].strip() not in gpt3_response:
                    print("[-]: Tag not found in response, continuing...")
                    print(gpt3_response)
                    cnt -= 1
                    continue
                # -------------------------------------------------------

                # Get just the actions
                gpt3_acts_text = gpt3_response.split(tags[0].strip())[0]
                pred_acts, pred_objs = get_acts_objs(gpt3_acts_text)

                prec, rec, f1, true_objs = compute_f1_acts(test_true_dict, pred_acts)
                results["precision"][0] += prec
                results["recall"][0] += rec
                results["f1"][0] += f1

                print("[acts] Precision: {:.2f} | Recall: {:.2f} | F1: {:.2f}".format(
                    prec, rec, f1
                ))

                prec, rec, f1 = compute_f1_objs(true_objs, pred_objs)
                results["precision"][1] += prec
                results["recall"][1] += rec
                results["f1"][1] += f1

                print("[objs] Precision: {:.2f} | Recall: {:.2f} | F1: {:.2f}".format(
                    prec, rec, f1
                ))

            ########### Averages ###########
            x = []
            print("[+]: AVERAGES over {} runs".format(cnt))
            for i, name in enumerate(["acts", "objs"]):
                for op in ["precision", "recall", "f1"]:
                    results[op][i] /= cnt
                    results[op][i] = round(results[op][i], 4)

                print("[{}]: Precision: {:.4f} | Recall: {:.4f} | F1: {:.4f}".format(
                    name, results["precision"][i], results["recall"][i], results["f1"][i]
                ))

            prec, rec, f1 = results["precision"], results["recall"], results["f1"]
            x = [list(DOMAINS.keys()).index(domain_name), ENGINES.index(gpt3_engine),
                 n_runs, prec[0], rec[0], f1[0], prec[1], rec[1], f1[1]]

            ########### Save data ###########
            print("[+]: Saving data \n\n")
            cols = ["domain", "engine", "runs", "prec_acts", "rec_acts", "f1_acts", "prec_objs", "rec_objs", "f1_objs"]
            new_data = pd.DataFrame(np.array(x).reshape(1, -1), columns=cols)
            df = pd.read_csv(results_file).append(new_data) if os.path.exists(results_file) else new_data
            df.to_csv(results_file, index=False)
            #################################



#############################################################################
# def old_compute_f1_objs(true_dict, preds):
#     type = "objs"
#     essential = true_dict["essential"][type].copy()
#     optional = true_dict["optional"][type].copy()
#     exclusive = true_dict["exclusive"][type].copy()
#     words = test_data["words"]
#
#     # Flatten the data for objects
#     if type == "objs":
#         essential = [item for sublist in essential for item in sublist]
#         optional = [item for sublist in optional for item in sublist]
#         exclusive = []
#
#     total_tagged = len(preds)
#     total_truth = len(essential)
#
#     right_es, right_op, right_ex = 0, 0, 0
#     for item in preds:
#         if item in essential:
#             right_es += 1
#             essential.remove(item)  # Removes from the left
#             continue
#
#         if item in optional:
#             right_op += 1
#             total_truth += 1
#             optional.remove(item)
#
#     total_right = right_es + right_op + right_ex
#     precision = total_right / total_tagged
#     recall = total_right / total_truth
#     f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
#
#     return precision, recall, f1
