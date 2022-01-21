import os
import re
import numpy as np
from pathlib import Path
from tarski.io import PDDLReader

nd = {"a": "blue", "b": "orange", "c": "red", "d": "yellow", "e": "white", "f": "magenta"}

def plan_to_text():
    def treat_on(atom):
        terms = atom.subterms
        return f"the {nd[terms[0].name]} block on top of the {nd[terms[1].name]} block"

    BLOCKS = [nd[x.name] for x in list(lang.constants())]

    data = {}
    for atom in problem.init.as_atoms():
        pred_name = atom.symbol.name
        if pred_name not in data:
            data[pred_name] = []

        if pred_name == "on":
            first, second = atom.subterms
            data["on"].append(f"{nd[first.name]} is on {nd[second.name]}")
        elif atom.subterms:
            data[pred_name].append(nd[atom.subterms[0].name])

    n = len(data)
    INIT = ""
    for i, obj in enumerate(data):
        n_obj = len(data[obj])
        if obj == "on":
            a = " and " if len(data[obj]) > 1 else ""
            INIT += ", ".join(data[obj][:-1]) + f"{a}{data[obj][-1]}"
        else:
            if n_obj >= 1:
                a = " and " if len(data[obj]) > 1 else ""
                is_are = "are" if n_obj > 1 else "is"
                INIT += ", ".join(data[obj][:-1]) + f"{a}{data[obj][-1]}" + f" {is_are} {obj}"
            else:
                INIT += f"we have {obj}"
        if i < n - 1: INIT += " and "

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
    with open(plan_file) as f:
        plan = [line.rstrip() for line in f][:-1]

    cost = len(plan)
    for i, action in enumerate(plan):
        action = action.strip("(").strip(")")
        act_name, objs = action.split(" ")[0], action.split(" ")[1:]
        objs = [nd[x] for x in objs]

        on_from = " from " if "unstack" in act_name else " on "
        PLAN += f'{act_name} the {f"{on_from}".join(objs)} block' #TODO: Continue treating this 'on'

        print(PLAN)
        if i == cost - 2:
            PLAN += " and "
        elif i < cost - 1:
            PLAN += ", "

    TEMPLATE = \
        f"There is a {', '.join(BLOCKS[:-1])} and {BLOCKS[-1]} block on the table.\nMy goal is to have {GOAL}.\nMy plan is as follows \n {PLAN}."

    return TEMPLATE.replace("-", " ").replace("ontable", "on table")

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

    object_names = [x.lower() for x in nd.values()]
    lines = [line.strip() for line in text.lower().strip().split("\n")]
    plan = []
    for line in lines:
        action_list = [action in line for action in actions]
        assert sum(action_list) == 1
        action = raw_actions[np.where(action_list)[0][0]]
        n_objs = len(actions_params_dict[action].parameters.vars())

        objs = get_ordered_objects(object_names, line)

        action = "({} {})".format(action, " ".join(objs[:n_objs+1]))
        plan.append(action)

    return plan

TEXT = """
    Pick up the blue block from on top of the yellow block
    Put down the blue block on the table
    Pick up the yellow block from the table
    Stack the yellow block on top of the blue block
    Pick up the red block from the table
    Stack the red block on top of the yellow block
    """

INTRO = """
    I am playing with a set of blocks where I need to arrange the blocks into stacks. \
    I can only pick up one block at a time and I can only pick up a block if there are no other blocks on top of it.
    """

if __name__ == '__main__':
    domain = './blocksworld.pddl'
    instance = './instances/instance-{}.pddl'
    plan_out = "sas_plan"

    for i in range(1, 2):
        cur_instance = instance.format(i)
        reader = PDDLReader(raise_on_error=True)
        reader.parse_domain(domain)
        problem = reader.parse_instance(cur_instance)

        cmd = f"~/soft/downward/fast-downward.py {domain} {cur_instance} --search \"astar(lmcut())\" > /dev/null 2>&1"
        os.system(cmd)

        plan_file = Path(plan_out).read_text()
        lang = problem.language
        print(plan_to_text())


        # plan = text_to_plan(TEXT, problem.actions)
        # validate_plan(plan, problem)

##############################
# print(lang.sorts)
# print(lang.predicates)
# print(lang.functions)
