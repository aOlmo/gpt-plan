import re
import os
import time
import pickle
import openai
import random
import threading

import pandas as pd
import numpy as np
from tqdm import tqdm


############################ Threading ##############################

class myThreadEngine(threading.Thread):
    def __init__(self, threadID, gpt3_engine, n_examples, max_sents, domain_examples, domain_examples_ids):
        threading.Thread.__init__(self)
        self.threadId = threadID
        self.gpt3_engine = gpt3_engine
        self.n_examples = n_examples
        self.max_sents = max_sents
        self.domain_examples = domain_examples
        self.domain_examples_ids = domain_examples_ids
        self.results = {"precision": [0, 0], "recall": [0, 0], "f1": [0, 0]}

    def send_query_gpt3(self, query):
        max_token_err_flag = False
        try:
            response = openai.Completion.create(
                engine=self.gpt3_engine,
                prompt=query,
                temperature=gpt3_temp,
                max_tokens=gpt3_max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
        except:
            max_token_err_flag = True
        text_response = response["choices"][0]["text"] if not max_token_err_flag else ""

        return text_response, max_token_err_flag

    def run(self):
        for domain_name in DOMAINS:
            out_file = open("data/{}_{}.out".format(self.gpt3_engine, domain_name), "a+")
            out_file.write(str(self.domain_examples_ids[domain_name]) + ": {} EXAMPLES\n".format(self.n_examples))
            domain = DOMAINS[domain_name]

            # precision, recall, f1: [actions, objects]
            train_samples_str = self.domain_examples[domain_name]

            cnt = 0
            pbar = tqdm(domain)
            # pbar = tqdm(domain)
            for i, test_sample in enumerate(pbar):
                if i in self.domain_examples_ids[domain_name][1:]: continue
                cnt += 1

                query = train_samples_str.strip()

                test_data = get_data(test_sample, 200)
                text_str_test, _ = get_query_strs(test_data)

                query += tags[0] + text_str_test + tags[1]
                query = query.strip()

                test_true_dict = get_test_dict(test_data)

                # ----- Send query to GPT3 and check correct output -----
                gpt3_response, err_flag = self.send_query_gpt3(query)
                if err_flag or not count_unfinished_responses and tags[0].strip() not in gpt3_response:
                    if err_flag:
                        pbar.set_postfix({"max_tokens_error": True})
                    else:
                        print("[-]: Tag not found, continuing ...")
                        # print(gpt3_response)
                    cnt -= 1
                    continue
                # -------------------------------------------------------

                # Get just the actions
                gpt3_acts_text = gpt3_response.split(tags[0].strip())[0]
                pred_acts, pred_objs = get_acts_objs(gpt3_acts_text)

                prec_a, rec_a, f1_a, true_objs = compute_f1_acts(test_true_dict, pred_acts, test_data)
                prec_o, rec_o, f1_o = compute_f1_objs(true_objs, pred_objs)

                self.results["precision"][0] += prec_a
                self.results["recall"][0] += rec_a
                self.results["f1"][0] += f1_a

                self.results["precision"][1] += prec_o
                self.results["recall"][1] += rec_o
                self.results["f1"][1] += f1_o

                out_file.write("\n{}: {:.4f}-{:.4f}-{:.4f}_{:.4f}-{:.4f}-{:.4f}\n{}\n".format(
                    i, prec_a, rec_a, f1_a, prec_o, rec_o, f1_o, gpt3_acts_text.strip()
                ))

                pbar.set_postfix({"f1_act": self.results["f1"][0] / cnt, "f1_obj": self.results["f1"][1] / cnt})

            ########### Averages ###########
            print("ENGINE: {} | DOMAIN: {} | N_EXAMPLES: {}\n{}".format(self.gpt3_engine, domain_name, self.n_examples, "-" * 28))
            print("[+]: AVERAGES over {} runs".format(cnt))
            for i, name in enumerate(["acts", "objs"]):
                for op in ["precision", "recall", "f1"]:
                    self.results[op][i] /= cnt
                    self.results[op][i] = round(self.results[op][i], 4)

                print("[{}-exs-{}]: Precision: {:.4f} | Recall: {:.4f} | F1: {:.4f}".format(
                    name, self.n_examples, self.results["precision"][i], self.results["recall"][i], self.results["f1"][i]
                ))

            prec, rec, f1 = self.results["precision"], self.results["recall"], self.results["f1"]
            x = [list(DOMAINS.keys()).index(domain_name), ENGINES.index(self.gpt3_engine),
                 cnt, self.n_examples, self.max_sents, prec[0], rec[0], f1[0], prec[1], rec[1], f1[1]]

            ########### Save data ###########
            print("[+]: Saving data \n\n")
            cols = ["domain", "engine", "runs", "examples", "max_sents", "prec_acts", "rec_acts", "f1_acts",
                    "prec_objs", "rec_objs", "f1_objs"]
            new_data = pd.DataFrame(np.array(x).reshape(1, -1), columns=cols)
            df = pd.read_csv(results_file).append(new_data) if os.path.exists(results_file) else new_data
            df.to_csv(results_file, index=False)
            #################################
            out_file.write("\n\n")



#####################################################################
############################### Utils ###############################
def get_acts_objs(acts_text):
    acts = [act.split("(")[0].strip() for act in acts_text.split("),") if act.split("(")[0].strip() != ""]
    objs_list = re.findall(r'\((.*?)\)', acts_text)

    objs = []
    for obj in objs_list:
        objs += obj.split(",")

    return acts, objs


def compute_f1_acts(true_dict, preds, test_data):
    true_objs = []
    type = "acts"
    essential = true_dict["essential"][type].copy()
    optional = true_dict["optional"][type].copy()
    exclusive = true_dict["exclusive"][type].copy()
    words = test_data["words"]

    total_tagged = len(preds) if len(preds) > 0 else 1
    total_truth = len(essential) + len(exclusive)
    right_es, right_op, right_ex = 0, 0, 0
    for item in preds:
        if item in essential:
            right_es += 1
            true_objs += true_dict["essential"]["act_obj"][essential.index(item)][1]  # Add the corresponding objects
            essential.remove(item)  # Removes from the left

        elif item in optional:
            right_op += 1
            total_truth += 1
            true_objs += true_dict["optional"]["act_obj"][optional.index(item)][1]  # Add the corresponding objects
            optional.remove(item)

    for item_list in exclusive:
        item_list_w = [words[w_id] for w_id in item_list]
        intersect = set(item_list_w).intersection(preds)
        # There can only appear 1 exclusive action amongst the predictions
        if len(intersect) == 1:
            right_ex += 1
            i = item_list_w.index(list(intersect)[0])  # Find the object indices of the matched action
            act_objs = [words[w_id] for w_id in test_data["acts2objs"][item_list[i]]]
            true_objs += act_objs

    total_right = right_es + right_op + right_ex
    precision = total_right / total_tagged
    recall = total_right / total_truth
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

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
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

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
        if act_idx > last_w - 1: break
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


def calc_avg_num_sents():
    for domain_name in DOMAINS:
        domain = DOMAINS[domain_name]
        ct = 0
        for i in domain:
            ct += len(i["sents"])
            si = 0
            for s in i["sents"]:
                si += len(s)
        print("AVG {} {} sents {}".format(domain_name, ct / len(domain), si / len(i["sents"])))

#######################################################################

def get_repr_examples(DOMAINS, max_sents, n_examples, rand=False):
    # Essential, exclusive, optional
    examples_ids = {"win": [], "cook": [], "wiki": []}
    examples_str = {"win": "", "cook": "", "wiki": ""}

    examples_remaining = n_examples
    if not rand:
        for d_name in DOMAINS:
            domain = DOMAINS[d_name]

            if n_examples == 1:
                examples_ids[d_name].append(random.randint(0, len(domain) - 1))
                continue

            # Max , id
            maxs = {"es": [0, 0], "ex": [0, 0], "op": [0, 0]}

            for i, sample in enumerate(tqdm(domain)):
                es, ex, op = 0, 0, 0
                for act in sample["acts"]:
                    es += 1 if act["act_type"] == 1 else 0
                    ex += 1 if act["act_type"] == 3 else 0
                    op += 1 if act["act_type"] == 2 else 0

                total_acts = es + ex + op
                cur_maxs = {"es": es / total_acts, "ex": ex / total_acts, "op": op / total_acts}
                for act_type in maxs:
                    max = maxs[act_type]
                    cur_max = cur_maxs[act_type]
                    if max[0] < cur_max:
                        max[0] = cur_max
                        max[1] = i

            for act_type in maxs:
                max, i = maxs[act_type][0], maxs[act_type][1]
                # print("{}-{}: max: {:.2}, ith: {}".format(d_name, act_type, max, i))
                examples_ids[d_name].append(i)
        examples_remaining = n_examples - 3

    if examples_remaining >= 1:
        for d_name in DOMAINS:
            domain = DOMAINS[d_name]
            new_example = random.randint(0, len(domain) - 1)
            while new_example in examples_ids[d_name]:
                new_example = random.randint(0, len(domain) - 1)
            examples_ids[d_name].append(new_example)
        examples_remaining -= 1

    # Get the corresponding TEXT and ACTION strings from the selected examples
    for d_name in DOMAINS:
        domain = DOMAINS[d_name]
        if n_examples == 2:
            examples_ids[d_name].pop(0)  # Manual remove of the essential max
        for i, ith_sample in enumerate(examples_ids[d_name]):
            data_sample = get_data(domain[ith_sample], max_sents)
            text_str, acts_str = get_query_strs(data_sample)
            examples_str[d_name] += tags[0] + text_str + tags[1] + acts_str

    return examples_str, examples_ids


if __name__ == '__main__':
    wiki = pickle.load(open("EASDRL/data/wikihow_labeled_text_data.pkl", "rb"))
    win = pickle.load(open("EASDRL/data/win2k_labeled_text_data.pkl", "rb"))
    cook = pickle.load(open("EASDRL/data/cooking_labeled_text_data.pkl", "rb"))
    _ = pickle.load(open("EASDRL/data/cooking_dependency.pkl", "rb"))

    # ================= Params =================
    random.seed(42)
    ENGINES = ["davinci", "curie", "babbage", "ada"]
    DOMAINS = {"win": win, "cook": cook}
    MAX_SENTS = 100

    gpt3_temp = 0  # Set to 0 for reproducibility
    gpt3_max_tokens = 100
    selected_engines = ["babbage", "ada"]

    results_file = "data.csv"
    openai.api_key = os.environ["OPENAI_API_KEY"]
    n_examples_list = [1, 2]  # 1: Random, 2: Excl+Opt 3: Es+Ex+Op 4: Random +prev
    count_unfinished_responses = True
    tags = ["\n\nTEXT: \n", "\nACTIONS: \n"]
    # ==========================================

    for n_examples in n_examples_list:
        max_sents = 10 if n_examples == 4 else MAX_SENTS
        max_sents = 15 if n_examples == 3 else max_sents
        domain_examples, domain_examples_ids = get_repr_examples(DOMAINS, max_sents, n_examples)
        for i, gpt3_engine in enumerate(selected_engines):
            thread_name = "{}_{}".format(gpt3_engine, n_examples)
            print("[+]: Executing {}".format(thread_name))
            thread = myThreadEngine(i, gpt3_engine, n_examples, max_sents, domain_examples, domain_examples_ids)
            thread.start()

#############################################################################
# def old_compute_f1_objs(true_dict, preds):
#     type = "objs"
#     essential = true_dict["essential"][type].copy()
#     optional = true_dict["optional"][type].copy()
#     words = test_data["words"]
#
#     essential = [item for sublist in essential for item in sublist]
#     optional = [item for sublist in optional for item in sublist]
#     exclusive = []
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
