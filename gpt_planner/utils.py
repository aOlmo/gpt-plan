import os
import random
import openai
import numpy as np

from pathlib import Path

openai.api_key = os.environ["OPENAI_API_KEY"]


class Callbacks():
    def __init__(self, data):
        self.data = data
        self.instances_template = f"./instances/{data['domain']}/{data['instances_template']}"

    def t1_gen_goal_directed_instances(self, n_objs=[4, 5]):
        n = self.data['n_instances']
        ORIG = os.getcwd()
        CMD = "./blocksworld 4 {}"

        os.chdir("pddlgenerators/blocksworld/")
        instance_file = f"{ORIG}/{self.instances_template}"

        set = {}
        c = 0
        for obj in n_objs:
            cmd_exec = CMD.format(obj)
            for i in range(n):
                with open(instance_file.format(c), "w+") as fd:
                    pddl = os.popen(cmd_exec).read()
                    if pddl in set:
                        print("[+]: Same instance, skipping...")
                        continue
                    fd.write(pddl)
                c += 1

        print(f"[+]: A total of {c} instances have been generated")
        os.chdir(ORIG)

    def t4_gen_generalization_instances(self):
        def gen_instance(objs):
            text = "(define (problem BW-generalization-4)\n(:domain blocksworld-4ops)"
            text += "(:objects " + " ".join(objs) + ")\n"
            text += "(:init \n(handempty)\n"

            for obj in objs:
                text += f"(ontable {obj})\n"

            for obj in objs:
                text += f"(clear {obj})\n"

            text += ")\n(:goal\n(and\n"

            obj_tuples = list(zip(objs, objs[1:]))
            # obj_tuples.reverse() # TODO: this improves considerably Davinci t4

            for i in obj_tuples:
                text += f"(on {i[0]} {i[1]})\n"

            text += ")))"
            return text

        n = self.data['n_instances']
        objs = self.data['encoded_objects']
        encoded_objs = list(objs.keys())

        print("[+]: Making generalization instances for blocksworld")
        for c in range(n):
            n_objs = random.randint(3, len(objs))
            random.shuffle(encoded_objs)
            objs_instance = encoded_objs[:n_objs]
            instance = gen_instance(objs_instance)

            with open(self.instances_template.format(c), "w+") as fd:
                fd.write(instance)


def send_query_gpt3(query, engine, max_tokens, stop="[STATEMENT]"):
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
            stop=stop)
    except:
        max_token_err_flag = True
        print("[-]: Failed GPT3 query execution")

    text_response = response["choices"][0]["text"] if not max_token_err_flag else ""
    return text_response.strip()


def treat_on(letters_dict, atom):
    terms = atom.subterms
    return f"the {letters_dict[terms[0].name]} block on top of the {letters_dict[terms[1].name]} block"


def parse_problem(problem, data, shuffle):
    def parse(init_goal_preds, OBJS):
        TEXT = ""
        predicates = []

        init_goal_preds = list(init_goal_preds)
        for atom in init_goal_preds:
            objs = []
            for subterm in atom.subterms:
                objs.append(OBJS[subterm.name])
            predicates.append(data['predicates'][atom.symbol.name].format(*objs))

        if len(predicates) > 1:
            TEXT += ", ".join(predicates[:-1]) + f" and {predicates[-1]}"
        else:
            TEXT += predicates[0]
        return TEXT

    OBJS = data['encoded_objects']

    init_atoms = problem.init.as_atoms()
    goal_preds = problem.goal.subformulas if hasattr(problem.goal, 'subformulas') else [problem.goal]

    if shuffle:
        random.shuffle(init_atoms)
        random.shuffle(goal_preds)

    # ----------- INIT STATE TO TEXT ----------- #
    INIT = parse(init_atoms, OBJS)

    # ----------- GOAL TO TEXT ----------- #
    GOAL = parse(goal_preds, OBJS)

    return INIT, GOAL


def get_ordered_objects(object_names, line):
    objs = []
    pos = []
    for obj in object_names:
        if obj in line:
            objs.append(obj)
            pos.append(line.index(obj))

    sorted_zipped_lists = sorted(zip(pos, objs))
    return [el for _, el in sorted_zipped_lists]


def validate_plan(domain, instance, plan_file):
    cmd = f"Validate {domain} {instance} {plan_file}"
    response = os.popen(cmd).read()
    return True if "Plan valid" in response else False


def fill_template(INIT, GOAL, PLAN):
    text = ""
    if INIT != "":
        text += "\n[STATEMENT]\n"
        text += f"As initial conditions I have that {INIT.strip()}"
    if GOAL != "":
        text += f"\nMy goal is to have that {GOAL}."
    text += f"\n\nMy plan is as follows:\n\n[PLAN]{PLAN}"

    # TODO: Add this replacement to the yml file -- Use "Translations" dict in yml
    text = text.replace("-", " ").replace("ontable", "on the table")
    return text


def instance_to_text_blocksworld(problem, get_plan, data, shuffle=False):
    """
    Function to make a blocksworld instance into human-readable format
    :param get_plan: Flag to return the plan as text as well
    """

    OBJS = data['encoded_objects']

    # ----------- PARSE THE PROBLEM ----------- #
    INIT, GOAL = parse_problem(problem, data, shuffle)

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
            objs = [OBJS[obj] for obj in objs]
            PLAN += data['actions'][act_name].format(*objs) + "\n"

    return INIT, GOAL, PLAN


def text_to_plan_blocksworld(text, action_set, plan_file, data):
    """
    Converts blocksworld plan in plain text to PDDL plan
    ASSUMPTIONS:
        (1) Actions in the text we have them on the domain file
        (2) We know the object names
        (3) Objects order is given by the sentence

    :param text: Blocksworld text to convert
    :param action_set: Set of possible actions
    :param plan_file: File to store PDDL plan
    """

    # ----------- GET DICTIONARIES ----------- #
    LD = data['encoded_objects']  # Letters Dictionary
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
        action_list = [action in line.split() for action in raw_actions]
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

################################################################
#### Generate 2 instances each time
# for c in range(1, n, 2):
#     n_objs = random.randint(3, len(data))
#     random.shuffle(encoded_objs)
#     objs_i1 = encoded_objs[:n_objs]
#     objs_i2 = objs_i1.copy()
#     random.shuffle(objs_i2)
#
#     i1 = gen_instance(objs_i1)
#     i2 = gen_instance(objs_i2)
#
#     with open(INSTANCE_FILE.format(c), "w+") as fd:
#         fd.write(i1)
#     with open(INSTANCE_FILE.format(c+1), "w+") as fd:
#         fd.write(i2)
