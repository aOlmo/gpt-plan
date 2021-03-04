import os
import time
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
# TODO: Make data already in CSV format for better postprocessing + save outputs from
# TODO: Put params in config file
# ================= Params =================
random.seed(42)
gpt3_temp = 0.0  # Set to 0 for reproducibility
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
for _ in range(n_runs):
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
        engine="curie",
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

    # Get just the actions
    gpt3_acts_text = text_response.split(tags[0])[0]
    pred_acts, pred_objs = get_acts_objs(gpt3_acts_text)

    for i, (true_list, pred_list) in enumerate(zip([true_acts, true_objs], [pred_acts, pred_objs])):
        name = "acts" if i == 0 else "objs"
        for k in stemmers_data:
            stemmer = stemmers_data[k]["stemmer"]
            if stemmer is not None:
                true_list_stem = [stemmer.stem(w) for w in true_list]
                pred_list_stem = [stemmer.stem(w) for w in pred_list]
            else:
                true_list_stem, pred_list_stem = true_list, pred_list

            list_precision, list_recall, list_f1 = get_prec_rec_f1(true_list_stem, pred_list_stem)

            stemmers_data[k]["precision"][i] += list_precision
            stemmers_data[k]["recall"][i] += list_recall
            stemmers_data[k]["f1"][i] += list_f1

            print("[{}-{}-{}]: Precision: {:.2f} | Recall: {:.2f} | F1: {:.2f}".format(
                k, i, name, list_precision, list_recall, list_f1
            ))

print("\n\n[+]: Computing averages over {} runs\n".format(cnt))
for i, name in enumerate(["acts", "objs"]):
    for k in stemmers_data:
        avg_precision = stemmers_data[k]["precision"][i]/cnt
        avg_recall = stemmers_data[k]["recall"][i]/cnt
        avg_f1 = stemmers_data[k]["f1"][i]/cnt

        print("[{}-{}]: Precision: {:.4f} | Recall: {:.4f} | F1: {:.4f}".format(
            k, name, avg_precision, avg_recall, avg_f1
        ))