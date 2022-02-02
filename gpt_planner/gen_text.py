import os
import numpy as np

from utils import *
from pathlib import Path
from tarski.io import PDDLReader

ND = {"a": "blue", "b": "orange", "c": "red", "d": "yellow", "e": "white", "f": "magenta", "g": "black", "h": "cyan",
      "i": "green", "j": "violet"}
ND_B = {"b1": "blue", "b2": "orange", "b3": "red", "b4": "yellow"}

#TODO-A: Make this better
ND= ND_B

DN = {v: k for k, v in ND.items()}

def instance_to_text(get_plan=True):
    def treat_on(atom):
        terms = atom.subterms
        return f"the {ND[terms[0].name]} block on top of the {ND[terms[1].name]} block"

    # BLOCKS = [ND[x.name] for x in list(lang.constants())]
    data = {}
    for atom in problem.init.as_atoms():
        pred_name = atom.symbol.name
        if pred_name not in data:
            data[pred_name] = []

        if pred_name == "on":
            first, second = atom.subterms
            data["on"].append(f"the {ND[first.name]} block is on top of the {ND[second.name]} block")
        elif atom.subterms:
            data[pred_name].append(ND[atom.subterms[0].name])

    # We delete these for GPT-3
    del data['clear']
    del data['handempty']
    INIT = ""
    n = len(data)
    for i, obj in enumerate(data):
        n_obj = len(data[obj])
        if obj == "on":
            _and = " and " if len(data[obj]) > 1 else ""
            string = ", ".join(data[obj][:-1]) + f"{_and}{data[obj][-1]}"
            INIT += string.capitalize()
        else:
            _and = " and " if len(data[obj]) > 1 else ""
            is_are = "are" if n_obj > 1 else "is"
            string = "the " + ", ".join(data[obj][:-1]) + f"{_and}{data[obj][-1]} block{'s' if n_obj > 1 else ''}" + f" {is_are} {obj}"
            INIT += string.capitalize()
        INIT += ". "

    GOAL = ""
    try:
        n = len(problem.goal.subformulas)
        for i, atom in enumerate(problem.goal.subformulas):
            GOAL += treat_on(atom)
            if i == n - 2:
                GOAL += " and "
            elif i < n - 1:
                GOAL += ", "
    except:
        GOAL += treat_on(problem.goal)

    plan_file = "sas_plan"
    PLAN = ""
    if get_plan:
        PLAN = "\n\n"
        with open(plan_file) as f:
            plan = [line.rstrip() for line in f][:-1]

        for i, action in enumerate(plan):
            action = action.strip("(").strip(")")
            act_name, objs = action.split(" ")[0], action.split(" ")[1:]
            objs = [ND[x] for x in objs]

            on_from = "from" if "unstack" in act_name else "on top of"
            if len(objs) == 2:
                PLAN += f'{act_name.capitalize()} the {objs[0]} block {on_from} the {objs[1]} block'
            elif len(objs) == 1:
                PLAN += f'{act_name.capitalize()} the {objs[0]} block'

            PLAN += "\n"
        # PLAN += "End of plan\n\n"
    TEMPLATE = f"{INIT.strip()}\nMy goal is to have {GOAL}.\nMy plan is as follows{PLAN}"

    return TEMPLATE.replace("-", " ").replace("ontable", "on the table")


# NOTE: We are assuming:
#       (1) Actions in the text we have them on the domain
#       (2) The 'put' action is assumed to be 'put down'
#       (3) We know the object names
#       (4) Objects order are placed in the same order that appear in the sentence
def text_to_plan(text, action_set, plan_file):
    def get_ordered_objects(object_names, line):
        objs = []
        pos = []
        for obj in object_names:
            if obj in line:
                objs.append(obj)
                pos.append(line.index(obj))

        sorted_zipped_lists = sorted(zip(pos, objs))
        return [el for _, el in sorted_zipped_lists]


    actions_params_dict = dict(action_set.items())
    raw_actions = list(action_set.keys())
    text_actions = [x.replace("-", " ") for x in raw_actions]

    text = text.lower().strip()
    for action, text_action in zip(raw_actions, text_actions):
        text = text.replace(text_action, action)

    object_names = [x.lower() for x in ND.values()]
    lines = [line.strip() for line in text.split("\n")]

    plan = ""
    for line in lines:
        action_list = [action in line.split(" ") for action in raw_actions]
        if sum(action_list) == 0: continue
        action = raw_actions[np.where(action_list)[0][0]]
        n_objs = len(actions_params_dict[action].parameters.vars())

        objs = get_ordered_objects(object_names, line)
        objs = [DN[x] for x in objs]

        action = "({} {})".format(action, " ".join(objs[:n_objs + 1]))
        plan += f"{action}\n"

    print(f"[+]: Saving plan in {plan_file}")
    file = open(plan_file, "wt")
    file.write(plan)
    file.close()

    return plan


def compute_plan(domain, instance, file):
    cmd = f"~/soft/downward/fast-downward.py {domain} {instance} --search \"astar(lmcut())\" > /dev/null 2>&1"
    os.system(cmd)
    return Path(file).read_text()



INTRO = """
I am playing with a set of blocks where I need to arrange the blocks into stacks. Here are the actions I can do 

Pick up a block
Unstack a block from on top of another block
Stack a block on top of another block

I have the following restrictions on my actions.
I can only pick up or unstack one block at a time.
I can only pick up a block if the block is on the table and there are no other blocks on top of it.
I can only unstack a block from on top of another block if the block I am unstacking was really on top of the other block.
I can only unstack a block from on top of another block if the block I am unstacking had no other block on top of it.
I can only stack a block on top of another block if I had previously picked up or unstacked the block being stacked.
I can only stack a block on top of another block if the block onto which I am stacking the block has no other blocks on top of it.
"""
if __name__ == '__main__':

    np.random.seed(42)
    domain = './instances/generated_domain.pddl'
    instance = './instances/generated/instance-{}.pddl'
    plan_file = "sas_plan"
    gpt3_plan_file = "gpt_sas_plan"

    query = INTRO
    n_examples = 1
    cur_instance = ""

    # Generate N blocksworld problems
    gen_blocksworld_problems([4, 5, 6, 7], 30)

    N = 20
    verbose = False
    correct_plans = 0
    #TODO-A: Do this with random replacement and more difficult plans
    for start in np.random.randint(1, 20, N):
        for i in range(start, start+n_examples+1):
            last_plan = True if i == start + n_examples else False
            ## Read Instance ##
            cur_instance = instance.format(i)
            print(f"Instance {cur_instance}")
            reader = PDDLReader(raise_on_error=True)
            reader.parse_domain(domain)
            problem = reader.parse_instance(cur_instance)
            lang = problem.language
            # ---------------- #

            # ------------ Put plan and instance into text ------------ #
            plan = compute_plan(domain, cur_instance, plan_file)
            query += instance_to_text(not last_plan) + "\n"
            # --------------------------------------------------------- #

        # Querying GPT-3

        gpt3_response = send_query_gpt3(query, 'davinci', 120)

        # Do text_to_plan procedure
        gpt3_plan = text_to_plan(gpt3_response, problem.actions, gpt3_plan_file)

        if verbose:
            print(query)
            print("\n--------- GPT3 response ---------")
            print(gpt3_response)
            print("\n--------- Extracted plan ---------")
            print(gpt3_plan)
            print(ND)

        # Apply VAL
        correct_plans += int(validate_plan(domain, cur_instance, gpt3_plan_file))

    print(f"[+]: The number of correct plans is {correct_plans}/{N}={correct_plans/N*100}%")

