import os
import time
import nltk
import pickle
import openai
import random
import re
from nltk.stem import PorterStemmer, LancasterStemmer

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
lancaster_stem = LancasterStemmer()
porter_stem = PorterStemmer()
stemmer = porter_stem
# ==========================================

def get_acts_objs(acts_text):
    acts = [act.split("(")[0].strip() for act in acts_text.split("),") if act.split("(")[0].strip() != ""]
    objs_list = re.findall(r'\((.*?)\)', acts_text)

    objs = []
    for obj in objs_list:
        objs += obj.split(",")

    return acts, objs

a = pickle.load(open("EASDRL/data/wikihow_labeled_text_data.pkl", "rb"))
b = pickle.load(open("EASDRL/data/win2k_labeled_text_data.pkl", "rb"))
c = pickle.load(open("EASDRL/data/cooking_labeled_text_data.pkl", "rb"))
d = pickle.load(open("EASDRL/data/refined_cooking_data.pkl", "rb"))
e = pickle.load(open("EASDRL/data/cooking_dependency.pkl", "rb"))

c = a

t_prec = 0
t_rec = 0
t_f1 = 0
cnt = n_runs
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

    true_acts, true_objs = get_acts_objs(true_acts_text)
    true_acts_stem = [stemmer.stem(w) for w in true_acts]

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
        cnt -= 1
        continue

    gpt3_acts_text = text_response.split(tags[0])[0]
    pred_acts, pred_objs = get_acts_objs(gpt3_acts_text)
    pred_acts_stem = [stemmer.stem(w) for w in pred_acts]

    true_acts_cpy = true_acts_stem[:]
    totalTruth = len(true_acts_stem)
    totalTagged = len(pred_acts_stem)
    totalRight = 0
    # Check if the current action is in the list of gt actions, if it is, remove from the truth list
    for act in pred_acts_stem:
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
print("Avgs over {} runs:\nPrecision: {:.2f} | Recall: {:.2f} | F1: {:.2f}".format(cnt, t_prec, t_rec, t_f1))


