import os
import time
import pickle
import openai
import re

# TODO: Use threads for parallel execution
# TODO: Try to reduce complexity of the sent text
# ---------------- Specs -----------------
# Set to 0 for reproducibility
gpt3_temp = 0.0
gpt4_max_tokens = 200
openai.api_key = os.environ["OPENAI_API_KEY"]
# The amount of text that these generate cannot go over 2048 -- TODO: Randomize
n_examples = 2
tags = ["\n\nRECIPE: \n", "\nACTIONS: \n"]
# ----------------------------------------

a = pickle.load(open("EASDRL/data/wikihow_labeled_text_data.pkl", "rb"))
b = pickle.load(open("EASDRL/data/win2k_labeled_text_data.pkl", "rb"))
c = pickle.load(open("EASDRL/data/cooking_labeled_text_data.pkl", "rb"))
d = pickle.load(open("EASDRL/data/refined_cooking_data.pkl", "rb"))
e = pickle.load(open("EASDRL/data/cooking_dependency.pkl", "rb"))

# Generate the first N examples to give GPT3
query = ""
for i in range(n_examples):
    query += tags[0]
    for sent in c[i]["sents"]:
        query += " ".join(sent)+".\n"

    query += tags[1]
    for act_dict in c[i]["acts"]:
        objs = [c[i]["words"][wId] for wId in act_dict["obj_idxs"][0]]
        query += "{}({}), ".format(c[i]["words"][act_dict["act_idx"]].lower(), ",".join(objs))

    # Remove last comma
    # query = query[:-2]

# Remove everything after last ACTIONS tag and get the true actions
f_query = query[:query.rfind(tags[1])]+tags[1]
true_acts_text = query[query.rfind(tags[1])+len(tags[1]):]
true_acts_text.replace(",", "")

true_acts = [act.split("(")[0].strip() for act in true_acts_text.split("),")]

# ---------------- Send query --------------
print("[+]: Sending query...")
start = time.time()
response = openai.Completion.create(
  engine="davinci",
  prompt=f_query,
  temperature=gpt3_temp,
  max_tokens=gpt4_max_tokens,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print("[+]: {:.2}s elapsed".format(time.time()-start))
# -------------------------------------------

# Process response
# TODO: Make sure there
gpt3_acts_text = response["choices"][0]["text"]
test_acts = [act.split("(")[0].strip() for act in gpt3_acts_text.split("),")]
# for action in  gpt3_actions.split("),"):
print("ssfdsfd")


