import os
import time
import pickle
import openai
import random
import re


# TODO: Make shorter sentences
# TODO: Put Exclusive actions like (act1() or act2() or act3())
# TODO: Make data already in CSV format for better postprocessing

def get_acts_objs(acts_text):
    acts = [act.split("(")[0].strip() for act in acts_text.split("),") if act.split("(")[0].strip() != ""]
    objs_list = re.findall(r'\((.*?)\)', acts_text)

    objs = []
    for obj in objs_list:
        objs += obj.split(",")

    return acts, objs


def compute_f1(true_dict, preds, type):
    essential = true_dict["essential"][type].copy()
    optional = true_dict["optional"][type].copy()
    exclusive = true_dict["exclusive"][type].copy()
    words = test_data["words"]

    # Flatten the data for objects
    if type == "objs":
        essential = [item for sublist in essential for item in sublist]
        optional = [item for sublist in optional for item in sublist]
        exclusive = []

    total_tagged = len(preds)
    total_truth = len(essential) + len(exclusive)

    right_es, right_op, right_ex = 0, 0, 0
    for item in preds:
        if item in essential:
            right_es += 1
            essential.remove(item)  # Removes from the left
            continue

        if item in optional:
            right_op += 1
            total_truth += 1
            optional.remove(item)

    if type == "acts":
        for item_list in exclusive:
            item_list_w = [words[w_id] for w_id in item_list]
            right_ex += 1 if len(set(item_list_w).intersection(preds)) == 1 else 0

    total_right = right_es + right_op + right_ex
    precision = total_right / total_tagged
    recall = total_right / total_truth
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1


def get_data(sample):
    # Action | (Objs) | Type
    data = {
        "data_id": [],
        "data_str": [],
        "related": {},
        "acts2objs": {},
        "sents": sample["sents"],
        "words": sample["words"],
        "word2sent": sample["word2sent"]
    }

    data_id = data["data_id"]
    data_str = data["data_str"]
    related = data["related"]
    acts2objs = data["acts2objs"]
    ws = sample["words"]
    for act_dict in sample["acts"]:
        act_idx = act_dict['act_idx']
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
    # ---------------- Send GPT3 query --------------
    print("[+]: Sending query...")
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
    print("[+]: {:.2f}s elapsed".format(time.time() - start))
    text_response = response["choices"][0]["text"]
    # -----------------------------------------------

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
    for (a1, a2) in test_dict["exclusive"]["acts"]:
        test_dict["exclusive"]["objs"].append([acts2objs[a1], acts2objs[a2]])
        # test_dict["exclusive"]["act_obj"][a1] = acts2objs[a1]
        # test_dict["exclusive"]["act_obj"][a2] = acts2objs[a2]

    types = list(test_dict.keys())
    for (act, objs, type), (act_id, objs_id, _) in zip(data["data_str"], data["data_id"]):
        es_op_ex = test_dict[types[type - 1]]
        if types[type - 1] != "exclusive":
            es_op_ex["act_obj"].append([act, objs])
            es_op_ex["acts"].append(act)
            es_op_ex["objs"].append(objs)

    return test_dict


wiki = pickle.load(open("EASDRL/data/wikihow_labeled_text_data.pkl", "rb"))
win = pickle.load(open("EASDRL/data/win2k_labeled_text_data.pkl", "rb"))
cook = pickle.load(open("EASDRL/data/cooking_labeled_text_data.pkl", "rb"))
_ = pickle.load(open("EASDRL/data/cooking_dependency.pkl", "rb"))

# precision, recall, f1: [actions, objects]
results = {
    "precision": [0, 0],
    "recall": [0, 0],
    "f1": [0, 0]
}
# ================= Params =================
random.seed(42)
gpt3_engine = "babbage"  # davinci, curie, babbage, ada
gpt3_temp = 0.0  # Set to 0 for reproducibility
gpt3_max_tokens = 150
openai.api_key = os.environ["OPENAI_API_KEY"]
n_examples = 2  # The amount of text cannot go over 2048
tags = ["\n\nTEXT: \n", "\nACTIONS: \n"]
n_runs = 10
init_max_acts = 20
domain = cook
cnt = n_runs
# ==========================================


for i in range(n_runs):
    # Randomly sample text sequences from the domain
    samples = random.sample(domain, n_examples + 1)
    # train_samples = domain[1:n_examples + 1]
    # test_sample = domain[0]  # domain[n_examples:n_examples + 1]
    train_samples = samples[:n_examples]
    test_sample = samples[n_examples: n_examples+1][0]

    query = ""
    for sample in train_samples:
        data_sample = get_data(sample)
        text_str, acts_str = get_query_strs(data_sample)
        query += tags[0] + text_str + tags[1] + acts_str

    test_data = get_data(test_sample)
    text_str_test, _ = get_query_strs(test_data)

    query += tags[0] + text_str_test + tags[1]
    query = query.strip()

    test_true_dict = get_test_dict(test_data)

    # ----- Send query to GPT3 and check correct output -----
    gpt3_response = send_query_gpt3(query)
    # if tags[0].strip() not in gpt3_response:
    #     print("[-]: Tag not found in response, continuing...")
    #     print(gpt3_response)
    #     cnt -= 1
    #     continue
    # -------------------------------------------------------

    # Get just the actions
    gpt3_acts_text = gpt3_response.split(tags[0].strip())[0]
    pred_acts, pred_objs = get_acts_objs(gpt3_acts_text)

    for i, (type, preds) in enumerate(zip(["acts", "objs"], [pred_acts, pred_objs])):
        prec, rec, f1 = compute_f1(test_true_dict, preds, type)

        results["precision"][i] += prec
        results["recall"][i] += rec
        results["f1"][i] += f1

        print("[{}-{}]: Precision: {:.2f} | Recall: {:.2f} | F1: {:.2f}".format(
            i, type, prec, rec, f1
        ))

print("\n\n[+]: Computing averages over {} runs\n".format(cnt))
for i, name in enumerate(["acts", "objs"]):
    avg_precision = results["precision"][i] / cnt
    avg_recall = results["recall"][i] / cnt
    avg_f1 = results["f1"][i] / cnt

    print("[{}-{}]: Precision: {:.4f} | Recall: {:.4f} | F1: {:.4f}".format(
        "Raw", name, avg_precision, avg_recall, avg_f1
    ))

###############################################
# Exclusive objs
# for i, sublist in enumerate(exclusive):
#     for j, subsub in enumerate(sublist):
#         exclusive[i][j] = [words[i] for i in subsub]
#     ...
#     ...
#     elif type == "objs":
#         max_right = 0
#         for excl in exclusive:
#             for pairs in excl:
#                 a1_objs, a2_objs = pairs[0], pairs[1]
#                 max_right = max(len(set(a1_objs).intersection(preds)), len(set(a2_objs).intersection(preds)))
###############################################
