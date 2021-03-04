import os
import time
import nltk
import pickle
import openai
import random
import re
from nltk.stem import PorterStemmer, LancasterStemmer

def get_acts_objs(acts_text):
    acts = [act.split("(")[0].strip() for act in acts_text.split("),") if act.split("(")[0].strip() != ""]
    objs_list = re.findall(r'\((.*?)\)', acts_text)

    objs = []
    for obj in objs_list:
        objs += obj.split(",")

    return acts, objs

def get_prec_rec_f1(true_list, pred_list):
    true_list_cpy = true_list[:]
    totalTruth = len(true_list)
    totalTagged = len(pred_list)
    totalRight = 0

    # Check if the current action is in the list of gt actions, if it is, remove from the truth list
    for act in pred_list:
        if act in true_list_cpy:
            totalRight += 1
            true_list_cpy.remove(act)

    precision = totalRight / totalTagged
    recall = totalRight / totalTruth
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1

# TODO: Use threads for parallel execution
# TODO: We can still finetune further making sure we include all actions from last sentence
# TODO: Make Lancaster, Porter and none in same execution
# ================= Params =================
random.seed(42)
gpt3_temp = 0.0 # Set to 0 for reproducibility
gpt3_max_tokens = 150
openai.api_key = os.environ["OPENAI_API_KEY"]
n_examples = 2  # The amount of text cannot go over 2048
tags = ["\n\nTEXT: \n", "\nACTIONS: \n"]
n_runs = 10
max_acts = 10
# ==========================================

wiki = pickle.load(open("EASDRL/data/wikihow_labeled_text_data.pkl", "rb"))
win = pickle.load(open("EASDRL/data/win2k_labeled_text_data.pkl", "rb"))
cook = pickle.load(open("EASDRL/data/cooking_labeled_text_data.pkl", "rb"))
_ = pickle.load(open("EASDRL/data/cooking_dependency.pkl", "rb"))

# precision, recall, f1: [actions, objects]
stemmers_data = {
    "Raw": {
        "stemmer": None,
        "precision": [0, 0],
        "recall": [0, 0],
        "f1": [0, 0]
    },
    "Porter": {
        "stemmer": PorterStemmer(),
        "precision": [0, 0],
        "recall": [0, 0],
        "f1": [0, 0]
    },
    "Lancaster": {
        "stemmer": LancasterStemmer(),
        "precision": [0, 0],
        "recall": [0, 0],
        "f1": [0, 0]
    }
}

domain = cook
cnt = n_runs
for i in range(n_runs):
    query = ""
    # Randomly sample text sequences from the domain
    samples = random.sample(domain, n_examples+1)
    for sample in samples:
        query += tags[0]
        # Restrict the amount of actions if needed
        max_acts = min(max_acts, len(sample["acts"])-1)
        # Get the number of sentences based on the amount of actions
        max_n_sents = sample["word2sent"][sample["acts"][max_acts]["act_idx"]]+1
        for sent in sample["sents"][:max_n_sents]:
            query += " ".join(sent)+".\n"

        query += tags[1]
        for act_dict in sample["acts"][:max_acts]:
            objs = [sample["words"][wId] for wId in act_dict["obj_idxs"][0]]
            query += "{}({}), ".format(sample["words"][act_dict["act_idx"]].lower(), ",".join(objs))

    # Remove everything after last ACTIONS tag and get the true actions
    f_query = query[:query.rfind(tags[1])]+tags[1]
    true_acts_text = query[query.rfind(tags[1])+len(tags[1]):]
    true_acts_text.replace(",", "")

    true_acts, true_objs = get_acts_objs(true_acts_text)

    # ---------------- Send GPT3 query --------------
    print("[+]: Sending query...")
    start = time.time()
    response = openai.Completion.create(
        engine="davinci",
        prompt=f_query,
        temperature=gpt3_temp,
        max_tokens=gpt3_max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print("[+]: {:.2f}s elapsed".format(time.time()-start))
    text_response = response["choices"][0]["text"]
    # -----------------------------------------------

    # Process response and discard if GPT3 did not finish the generation
    if tags[0] not in text_response:
        print("[-]: Tag not found in response, continuing...")
        print(text_response)
        cnt -= 1
        continue

    gpt3_acts_text = text_response.split(tags[0])[0]
    pred_acts, pred_objs = get_acts_objs(gpt3_acts_text)

    for k in stemmers_data:
        stemmer = stemmers_data[k]["stemmer"]
        if stemmer is not None:
            true_acts_stem = [stemmer.stem(w) for w in true_acts]
            pred_acts_stem = [stemmer.stem(w) for w in pred_acts]
            true_objs_stem = [stemmer.stem(w) for w in true_objs]
            pred_objs_stem = [stemmer.stem(w) for w in pred_objs]
        else:
            true_acts_stem, pred_acts_stem = true_acts, pred_acts
            true_objs_stem, pred_objs_stem = true_objs, pred_objs

        acts_precision, acts_recall, acts_f1 = get_prec_rec_f1(true_acts_stem, pred_acts_stem)
        objs_precision, objs_recall, objs_f1 = get_prec_rec_f1(true_objs_stem, pred_objs_stem)

        stemmers_data[k]["precision"][0] += acts_precision
        stemmers_data[k]["recall"][0] += acts_recall
        stemmers_data[k]["f1"][0] += acts_f1

        stemmers_data[k]["precision"][1] += objs_precision
        stemmers_data[k]["recall"][1] += objs_recall
        stemmers_data[k]["f1"][1] += objs_f1

        print("[{}-{}-acts]: "
              "Precision: {:.2f} | Recall: {:.2f} | F1: {:.2f}".format(k, i, acts_precision, acts_recall, acts_f1))
        print("[{}-{}-objs]: "
              "Precision: {:.2f} | Recall: {:.2f} | F1: {:.2f}".format(k, i, objs_precision, objs_recall, objs_f1))

for k in stemmers_data:
    avg_precision = stemmers_data[k]["precision"][0]/cnt
    avg_recall = stemmers_data[k]["recall"][0]/cnt
    avg_f1 = stemmers_data[k]["f1"][0]/cnt

    print("[{}-acts] Avg over {} runs: Precision: {:.4f} | Recall: {:.4f} | F1: {:.4f}".format(
        k, cnt, avg_precision, avg_recall, avg_f1))

    avg_precision = stemmers_data[k]["precision"][1] / cnt
    avg_recall = stemmers_data[k]["recall"][1] / cnt
    avg_f1 = stemmers_data[k]["f1"][1] / cnt

    print("[{}-objs] Avg over {} runs: Precision: {:.4f} | Recall: {:.4f} | F1: {:.4f}".format(
        k, cnt, avg_precision, avg_recall, avg_f1))