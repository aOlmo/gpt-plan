import os
import re
import numpy as np
from pathlib import Path
from tarski.io import PDDLReader

nd = {"a": "Blue", "b": "Orange", "c": "Red", "d": "Yellow", "e": "White", "f": "Magenta"}

def plan_to_text():
    def treat_on(atom):
        terms = atom.subterms
        return f"{nd[terms[0].name]} on {nd[terms[1].name]}"

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
        PLAN += f'{act_name} {f"{on_from}".join(objs)}'

        if i == cost - 2:
            PLAN += " and "
        elif i < cost - 1:
            PLAN += ", "

    TEMPLATE = \
        f"""
        We have blocks {", ".join(BLOCKS[:-1])} and {BLOCKS[-1]}.
        Block {INIT}.\nOur goal is to have {GOAL}.
        
        In order, the plan is to {PLAN}.
        """

    return TEMPLATE.replace("-", " ").replace("ontable", "on table")

# NOTE: We are assuming:
#       (1) Actions in the text we have them on the domain beforehand
#       (2) The 'put' action is assumed to be 'put down'
#       (3) We know the object names
#       (4) Objects order are placed in the same order that appear in the sentence
def text_to_plan(actions):
    text = """
    Pick up the blue block from on top of the yellow block
    Put down the blue block on the table
    Pick up the yellow block from the table
    Stack the yellow block on top of the blue block
    Pick up the red block from the table
    Stack the red block on top of the yellow block
    """

    actions_params_dict = dict(actions.items())
    raw_actions = list(actions.keys())
    actions = [x.replace("-", " ") for x in actions.keys()]

    object_names = [x.lower() for x in nd.values()]
    lines = [line.strip() for line in text.lower().strip().split("\n")]
    for line in lines:
        action_list = [action in line for action in actions]
        assert sum(action_list) == 1
        action = raw_actions[np.where(action_list)[0][0]]
        n_params = len(actions_params_dict[action].parameters.vars())
        params = [x for x in object_names if re.search(x, line)]  # TODO: this should be in order

        action = "({} {})".format(action, " ".join(params[:n_params+1]))
        print(action)

    #TODO: Use VAL here



if __name__ == '__main__':
    domain = './blocksworld.pddl'
    instance = './instances/instance-{}.pddl'
    plan_out = "sas_plan"

    for i in range(1, 10):
        cur_instance = instance.format(i)
        reader = PDDLReader(raise_on_error=True)
        reader.parse_domain(domain)
        problem = reader.parse_instance(cur_instance)

        text_to_plan(reader.parser.problem.actions)
        exit()

        cmd = f"~/soft/downward/fast-downward.py {domain} {cur_instance} --search \"astar(lmcut())\" > /dev/null 2>&1"
        os.system(cmd)

        plan_file = Path(plan_out).read_text()
        lang = problem.language
        print(plan_to_text())



##############################
# print(lang.sorts)
# print(lang.predicates)
# print(lang.functions)
