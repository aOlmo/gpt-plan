import os
import time
import pickle
import openai
import random
import re

# TODO: Make shorter sentences
# TODO: Put Exclusive actions like (act1() or act2() or act3())
# TODO: We can still finetune further making sure we include all actions from last sentence
# TODO: Make data already in CSV format for better postprocessing
# TODO: Put params in config file

def get_acts_objs(acts_text):
    acts = [act.split("(")[0].strip() for act in acts_text.split("),") if act.split("(")[0].strip() != ""]
    objs_list = re.findall(r'\((.*?)\)', acts_text)

    objs = []
    for obj in objs_list:
        objs += obj.split(",")

    return acts, objs


def get_prec_rec_f1(true_list, pred_list, true_list_excl):
    true_list_cpy = true_list[:]
    totalTruth = len(true_list)+len(true_list_excl)  # Add the Exclusive actions too
    totalTagged = len(pred_list)
    totalRight = 0

    # Check if the current action is in the list of gt actions, if it is, remove from the truth list
    for act in pred_list:
        if act in true_list_cpy:
            totalRight += 1
            true_list_cpy.remove(act)

    # Count how many exclusive actions are in the predicted list
    # and count as good only if one of them appears in the list
    for excl_acts in true_list_excl:
        c = 0
        for act in excl_acts:
            if act in pred_list:
                c += 1
        if c == 1:
            totalRight += 1

    precision = totalRight / totalTagged
    recall = totalRight / totalTruth
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1

def get_data(sample):
    # Action | (Objs) | Type
    data = {
        "data_id": [],
        "data_str": [],
        "related": {},
        "sents": sample["sents"],
        "words": sample["words"],
        "word2sent": sample["word2sent"]
    }

    data_id = data["data_id"]
    data_str = data["data_str"]
    related = data["related"]
    ws = sample["words"]
    for act_dict in sample["acts"]:
        related[act_dict['act_idx']] = act_dict["related_acts"]
        data_id.append([act_dict['act_idx'], act_dict['obj_idxs'], act_dict['act_type']])

        act_w, objs_w = ws[act_dict['act_idx']].lower(), [ws[obj].lower() for obj in act_dict['obj_idxs'][0]]
        data_str.append([act_w, objs_w, act_dict['act_type']])

    return data

def get_query_strs(data):
    text_str = ""
    for s in data["sents"]:
        text_str += " ".join(s)+".\n"

    acts_str = ""
    for (act, objs, id) in data["data_str"]:
        acts_str += "{}({}), ".format(act, ",".join(objs))

    acts_str = acts_str[:-2] # remove last comma
    return text_str, acts_str

# ================= Params =================
random.seed(42)
gpt3_engine = "curie"
gpt3_temp = 0.0  # Set to 0 for reproducibility
gpt3_max_tokens = 150
openai.api_key = os.environ["OPENAI_API_KEY"]
n_examples = 2  # The amount of text cannot go over 2048
tags = ["\n\nTEXT: \n", "\nACTIONS: \n"]
n_runs = 40
init_max_acts = 20
# ==========================================

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
domain = cook
cnt = n_runs
for _ in range(n_runs):
    # Randomly sample text sequences from the domain
    samples = random.sample(domain, n_examples+1)
    train_samples = domain[:n_examples]
    test_sample = domain[n_examples:n_examples+1]

    query = ""
    for sample in train_samples:
        data_sample = get_data(sample)
        text_str, acts_str = get_query_strs(data_sample)
        query += tags[0]+text_str+tags[1]+acts_str

    test_data = get_data(test_sample[0])
    text_str_test, _ = get_query_strs(test_data)

    query += tags[0]+text_str_test+tags[1]
    query = query.strip()

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

    # Process response and discard if GPT3 did not finish the generation
    if tags[0] not in text_response:
        print("[-]: Tag not found in response, continuing...")
        print(text_response)
        cnt -= 1
        continue

    # Get just the actions
    gpt3_acts_text = text_response.split(tags[0])[0]
    pred_acts, pred_objs = get_acts_objs(gpt3_acts_text)

    # for i, (true_list, pred_list, true_list_excl) in enumerate(zip([true_acts, true_objs], [pred_acts, pred_objs], [list(true_acts_excl), []])):
    #     name = "acts" if i == 0 else "objs"
    #
    #     list_precision, list_recall, list_f1 = get_prec_rec_f1(true_list, pred_list, true_list_excl)
    #
    #     results["precision"][i] += list_precision
    #     results["recall"][i] += list_recall
    #     results["f1"][i] += list_f1
    #
    #     print("[{}-{}]: Precision: {:.2f} | Recall: {:.2f} | F1: {:.2f}".format(
    #         i, name, list_precision, list_recall, list_f1
    #     ))

print("\n\n[+]: Computing averages over {} runs\n".format(cnt))
for i, name in enumerate(["acts", "objs"]):
    avg_precision = results["precision"][i] / cnt
    avg_recall = results["recall"][i] / cnt
    avg_f1 = results["f1"][i] / cnt

    print("[{}-{}]: Precision: {:.4f} | Recall: {:.4f} | F1: {:.4f}".format(
        "Raw", name, avg_precision, avg_recall, avg_f1
    ))
