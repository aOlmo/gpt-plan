import os
import time
import pickle
import openai
import random
import re

# TODO: Use threads for parallel execution
# TODO: Try to reduce complexity of the text sent
# ---------------- Specs -----------------
# Set to 0 for reproducibility
gpt3_temp = 0.5
gpt3_max_tokens = 200
openai.api_key = os.environ["OPENAI_API_KEY"]
n_examples = 2 # The amount of text cannot go over 2048
tags = ["\n\nRECIPE: \n", "\nACTIONS: \n"]
n_runs = 10
max_acts = 10
# ----------------------------------------

a = pickle.load(open("EASDRL/data/wikihow_labeled_text_data.pkl", "rb"))
b = pickle.load(open("EASDRL/data/win2k_labeled_text_data.pkl", "rb"))
c = pickle.load(open("EASDRL/data/cooking_labeled_text_data.pkl", "rb"))
d = pickle.load(open("EASDRL/data/refined_cooking_data.pkl", "rb"))
e = pickle.load(open("EASDRL/data/cooking_dependency.pkl", "rb"))

t_prec = 0
t_rec = 0
t_f1 = 0

for i in range(n_runs):
    query = ""
    samples = random.sample(c, n_examples+1)
    for sample in samples:
        query += tags[0]
        # Get the sentence number of the last action
        max_acts = min(max_acts, len(sample["acts"])-1)
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

    true_acts = [act.split("(")[0].strip() for act in true_acts_text.split("),") if act.split("(")[0].strip() != ""]
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

    # Process response
    if tags[0] not in text_response:
        print("[-]: Tag not found in response, continuing...")
        continue

    gpt3_acts_text = text_response.split(tags[0])[0]
    pred_acts = [act.split("(")[0].strip() for act in gpt3_acts_text.split("),") if act.split("(")[0].strip() != ""]

    true_acts_cpy = true_acts[:]
    totalTruth = len(true_acts)
    totalTagged = len(pred_acts)
    totalRight = 0
    # Check if the current action is in the list of gt actions, if it is, remove from the truth list
    for act in pred_acts:
        if act in true_acts_cpy:
            totalRight += 1
            true_acts_cpy.remove(act)

    precision = totalRight/totalTagged
    recall = totalRight/totalTruth
    f1 = 2*precision*recall/(precision+recall) if (precision+recall) > 0 else 0
    print("[{}]: Precision: {:.2f} | Recall: {:.2f} | F1: {:.2f}\n".format(i, precision, recall, f1))

    t_prec += precision
    t_rec += recall
    t_f1 += f1

t_prec /= n_runs
t_rec /= n_runs
t_f1 /= n_runs
print("Avgs over {} runs:\nPrecision: {:.2f} | Recall: {:.2f} | F1: {:.2f}".format(n_runs, t_prec, t_rec, t_f1))


