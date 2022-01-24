import os
import re
import numpy as np
from pathlib import Path
from tarski.io import PDDLReader

ND = {"a": "blue", "b": "orange", "c": "red", "d": "yellow", "e": "white", "f": "magenta"}
DN = {v: k for k, v in ND.items()}

def plan_to_text(get_plan=True):
    def treat_on(atom):
        terms = atom.subterms
        return f"the {ND[terms[0].name]} block on top of the {ND[terms[1].name]} block"

    BLOCKS = [ND[x.name] for x in list(lang.constants())]

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
    n = len(problem.goal.subformulas)
    for i, atom in enumerate(problem.goal.subformulas):
        GOAL += treat_on(atom)
        if i == n - 2:
            GOAL += " and "
        elif i < n - 1:
            GOAL += ", "

    plan_file = "sas_plan"
    PLAN = ""
    if get_plan:
        PLAN = "\n\n"
        with open(plan_file) as f:
            plan = [line.rstrip() for line in f][:-1]

        cost = len(plan)
        for i, action in enumerate(plan):
            action = action.strip("(").strip(")")
            act_name, objs = action.split(" ")[0], action.split(" ")[1:]
            objs = [ND[x] for x in objs]

            on_from = "from" if "unstack" in act_name else "on top of"
            if len(objs) == 2:
                PLAN += f'{act_name.capitalize()} the {objs[0]} block {on_from} the {objs[1]} block'
            elif len(objs) == 1:
                PLAN += f'{act_name.capitalize()} the {objs[0]} block'

            if i == cost - 2:
                PLAN += " and "
            elif i < cost - 1:
                PLAN += "\n"
        PLAN += ".\nEnd of plan.\n\n"
    TEMPLATE = f"{INIT.strip()}\nMy goal is to have {GOAL}.\nMy plan is as follows{PLAN}"

    return TEMPLATE.replace("-", " ").replace("ontable", "on the table")


# NOTE: We are assuming:
#       (1) Actions in the text we have them on the domain
#       (2) The 'put' action is assumed to be 'put down'
#       (3) We know the object names
#       (4) Objects order are placed in the same order that appear in the sentence
def text_to_plan(text, action_set):
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
    actions = [x.replace("-", " ") for x in action_set.keys()]

    object_names = [x.lower() for x in ND.values()]
    lines = [line.strip() for line in text.lower().strip().split("\n")]

    plan = ""
    for line in lines:
        action_list = [action in line for action in actions]
        assert sum(action_list) == 1
        action = raw_actions[np.where(action_list)[0][0]]
        n_objs = len(actions_params_dict[action].parameters.vars())

        objs = get_ordered_objects(object_names, line)
        objs = [DN[x] for x in objs]

        action = "({} {})".format(action, " ".join(objs[:n_objs + 1]))
        plan += f"{action}\n"

    return plan


TEXT = """
Pick up the orange block
Stack the orange block on top of the blue block
Pick up the red block
Stack the red block on top of the orange block
Pick up the yellow block 
Stack the yellow block on top of the red block.
    """

INTRO = """
    I am playing with a set of blocks where I need to arrange the blocks into stacks. \
    I can only pick up one block at a time and I can only pick up a block if there are no other blocks on top of it.
    """

if __name__ == '__main__':
    domain = './blocksworld.pddl'
    instance = './instances/instance-{}.pddl'
    plan_out = "sas_plan"

    n_examples = 3
    query = ""
    for i in [2]:#range(1, 2+n_examples):
        cur_instance = instance.format(i)
        print(f"Instance {cur_instance}")
        reader = PDDLReader(raise_on_error=True)
        reader.parse_domain(domain)
        problem = reader.parse_instance(cur_instance)

        # plan = text_to_plan(TEXT, problem.actions)
        # print(plan)

        cmd = f"~/soft/downward/fast-downward.py {domain} {cur_instance} --search \"astar(lmcut())\" > /dev/null 2>&1"
        os.system(cmd)

        plan_file = Path(plan_out).read_text()
        lang = problem.language
        last_plan = False if i == n_examples+1 else True
        query += plan_to_text(last_plan)
        query += "===================\n"

    print("== Query ==")
    print(query)

        # plan = text_to_plan(TEXT, problem.actions)
        # validate_plan(plan, problem)

##############################
# print(lang.sorts)
# print(lang.predicates)
# print(lang.functions)
