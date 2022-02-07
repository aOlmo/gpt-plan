import os
import openai
import numpy as np
from pathlib import Path

openai.api_key = os.environ["OPENAI_API_KEY"]
LETTERS_DICT = {"a": "blue", "b": "orange", "c": "red", "d": "yellow",
                "e": "white", "f": "magenta", "g": "black", "h": "cyan",
                "i": "green", "j": "violet", "k": "silver"}
LETTERS_DICT_GEN = {"b1": "blue", "b2": "orange", "b3": "red", "b4": "yellow"}


def treat_on(letters_dict, atom):
    terms = atom.subterms
    return f"the {letters_dict[terms[0].name]} block on top of the {letters_dict[terms[1].name]} block"


def instance_to_text_blocksworld(domain_type, problem, get_plan):
    """
    Function to make a blocksworld instance into human-readable format
    :param get_plan: Flag to return the plan as text as well
    :return:
    """

    # TODO: Get names from config file here
    LD = LETTERS_DICT if "ipc" == domain_type else LETTERS_DICT_GEN

    # ----------- INSTANCE TO TEXT ----------- #
    # TODO: Make this come from the config file directly
    data = {}
    for atom in problem.init.as_atoms():
        pred_name = atom.symbol.name
        if pred_name not in data:
            data[pred_name] = []

        if pred_name == "on":
            first, second = atom.subterms
            data["on"].append(f"the {LD[first.name]} block is on top of the {LD[second.name]} block")
        elif atom.subterms:
            data[pred_name].append(LD[atom.subterms[0].name])

    # We delete these for GPT-3
    INIT = ""
    del data['clear']
    del data['handempty']
    for obj in data:
        n_obj = len(data[obj])
        _and = " and " if len(data[obj]) > 1 else ""
        is_are = "are" if n_obj > 1 else "is"

        if obj == "on":
            string = ", ".join(data[obj][:-1]) + f"{_and}{data[obj][-1]}"
        else:
            string = "the " + ", ".join(
                data[obj][:-1]) + f"{_and}{data[obj][-1]} block{'s' if n_obj > 1 else ''}" + f" {is_are} {obj}"

        INIT += string.capitalize()
        INIT += ". "

    # ----------- GOAL TO TEXT ----------- #
    GOAL = ""
    try:
        n = len(problem.goal.subformulas)
        for i, atom in enumerate(problem.goal.subformulas):
            GOAL += treat_on(LD, atom)
            if i == n - 2:
                GOAL += " and "
            elif i < n - 1:
                GOAL += ", "
    except:
        GOAL += treat_on(LD, problem.goal)

    # ----------- PLAN TO TEXT ----------- #
    PLAN = ""
    plan_file = "sas_plan"
    if get_plan:
        PLAN = "\n"
        with open(plan_file) as f:
            plan = [line.rstrip() for line in f][:-1]

        for action in plan:
            action = action.strip("(").strip(")")
            act_name, objs = action.split(" ")[0], action.split(" ")[1:]
            objs = [LD[x] for x in objs]

            on_from = "from" if "unstack" in act_name else "on top of"
            if len(objs) == 2:
                PLAN += f'{act_name.capitalize()} the {objs[0]} block {on_from} the {objs[1]} block'
            elif len(objs) == 1:
                PLAN += f'{act_name.capitalize()} the {objs[0]} block'

            PLAN += "\n"

    # ----------- FILL TEMPLATE ----------- #
    text = f"{INIT.strip()}\nMy goal is to have {GOAL}.\nMy plan is as follows\n\n[PLAN]{PLAN}"
    text = text.replace("-", " ").replace("ontable", "on the table")

    return text


def get_ordered_objects(object_names, line):
    objs = []
    pos = []
    for obj in object_names:
        if obj in line:
            objs.append(obj)
            pos.append(line.index(obj))

    sorted_zipped_lists = sorted(zip(pos, objs))
    return [el for _, el in sorted_zipped_lists]


def text_to_plan_blocksworld(domain_type, text, action_set, plan_file):
    """
    Converts blocksworld plan in plain text to PDDL plan
    NOTE: We are assuming:
        (1) Actions in the text we have them on the domain
        (2) The 'put' action is assumed to be 'put down'
        (3) We know the object names
        (4) Objects order are placed in the same order that appear in the sentence

    :param text: Blocksworld text to convert
    :param action_set: Set of possible actions
    :param plan_file: File to store PDDL plan
    :return:
    """

    # ----------- GET DICTIONARIES ----------- #
    LD = LETTERS_DICT if "ipc" == domain_type else LETTERS_DICT_GEN  # Letters Dictionary
    BD = {v: k for k, v in LD.items()}  # Blocks Dictionary

    # ----------- GET RAW AND TEXT-FORMATTED ACTIONS AND OBJECTS ----------- #
    actions_params_dict = dict(action_set.items())
    raw_actions = list(action_set.keys())
    text_actions = [x.replace("-", " ") for x in raw_actions]

    text = text.lower().strip()
    for raw_action, text_action in zip(raw_actions, text_actions):
        text = text.replace(text_action, raw_action)

    object_names = [x.lower() for x in LD.values()]

    # ----------- GET PLAN FROM TEXT ----------- #
    plan = ""
    lines = [line.strip() for line in text.split("\n")]
    for line in lines:
        # Extracting actions
        action_list = [action in line.split(" ") for action in raw_actions]
        if sum(action_list) == 0: continue
        action = raw_actions[np.where(action_list)[0][0]]

        # Extracting Objects
        n_objs = len(actions_params_dict[action].parameters.vars())
        objs = get_ordered_objects(object_names, line)
        if len(objs) != n_objs: continue
        objs = [BD[x] for x in objs]

        action = "({} {})".format(action, " ".join(objs[:n_objs + 1]))
        plan += f"{action}\n"

    print(f"[+]: Saving plan in {plan_file}")
    file = open(plan_file, "wt")
    file.write(plan)
    file.close()

    return plan


def gen_blocksworld_problems(objects, n):
    ORIG = os.getcwd()
    CMD = "./blocksworld 4 {}"
    INSTANCE_FILE = "../../instances/generated/instance-{}.pddl"

    os.chdir("pddlgenerators/blocksworld/")

    set = {}
    c = 0
    for obj in objects:
        cmd_exec = CMD.format(obj)
        for i in range(n):
            with open(INSTANCE_FILE.format(c), "w+") as fd:
                pddl = os.popen(cmd_exec).read()
                if pddl in set:
                    print("[+]: Same instance, skipping...")
                    continue
                fd.write(pddl)
            c += 1

    print(f"[+]: A total of {c} instances have been generated")
    os.chdir(ORIG)


def send_query_gpt3(query, engine, max_tokens):
    max_token_err_flag = False
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=query,
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop="[STATEMENT]")
    except:
        max_token_err_flag = True
        print("[-]: Failed GPT3 query execution")

    text_response = response["choices"][0]["text"] if not max_token_err_flag else ""
    return text_response.strip()


def validate_plan(domain, instance, plan_file):
    cmd = f"Validate {domain} {instance} {plan_file}"
    response = os.popen(cmd).read()
    return True if "Plan valid" in response else False


def compute_plan(domain, instance, out_file):
    cmd = f"~/soft/downward/fast-downward.py {domain} {instance} --search \"astar(lmcut())\" > /dev/null 2>&1"
    os.system(cmd)

    if not os.path.exists(out_file):
        return ""

    return Path(out_file).read_text()
