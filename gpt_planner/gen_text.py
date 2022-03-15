import os
import numpy as np
import yaml

from utils import *
from tarski.io import PDDLReader

np.random.seed(42)

N_MAX = 30
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
    engine = 'davinci'
    verbose = 1
    n_examples = 1

    config_file = './configs/t4_plan_generalization.yaml'
    with open(config_file, 'r') as file:
        DATA = yaml.safe_load(file)

    domain_name = DATA['domain']  # ipc/generated
    plan_file = "sas_plan"
    gpt3_plan_file = "gpt_sas_plan"

    domain_pddl = f'./instances/{DATA["file"]}'
    instance_folder = f'./instances/{domain_name}/'
    instance = f'./instances/{domain_name}/instance-{{}}.pddl'

    # Make callbacks
    # TODO: Change eval() for a more secure option
    for callback in DATA['callbacks']:
        print(f"Executing callback {callback}")
        eval(callback)

    n_files = min(N_MAX, len(os.listdir(instance_folder)))

    query = ""
    cur_instance = ""
    correct_plans = 0
    for start in range(1, n_files - n_examples):
        query = INTRO
        for i in range(start, start + n_examples + 1):
            last_plan = True if i == start + n_examples else False
            get_plan = not last_plan
            # --------------- Read Instance --------------- #
            cur_instance = instance.format(i)
            reader = PDDLReader(raise_on_error=True)
            reader.parse_domain(domain_pddl)
            problem = reader.parse_instance(cur_instance)
            lang = problem.language
            print(f"Instance {cur_instance}")
            # --------------------------------------------- #

            # ------------ Put plan and instance into text ------------ #
            query += "\n[STATEMENT]\n"
            plan = compute_plan(domain_pddl, cur_instance, plan_file)
            query += instance_to_text_blocksworld(problem, get_plan, DATA)
            # --------------------------------------------------------- #

        # Querying GPT-3
        gpt3_response = send_query_gpt3(query, engine, 120)

        # Do text_to_plan procedure
        gpt3_plan = text_to_plan_blocksworld(gpt3_response, problem.actions, gpt3_plan_file, DATA)

        if verbose:
            print(query)
            print("--------- GPT3 response ---------")
            print(gpt3_response)
            print("--------- Extracted plan ---------")
            print(gpt3_plan)
            print("--------- GT plan ---------")
            print(plan)

        # Apply VAL
        correct = int(validate_plan(domain_pddl, cur_instance, gpt3_plan_file))
        if correct:
            validate_plan(domain_pddl, cur_instance, gpt3_plan_file)
            print("CORRECT PLAN BY GPT3!")
        correct_plans += correct

    print(f"[+]: The number of correct plans is {correct_plans}/{n_files - n_examples}={correct_plans / (n_files - n_examples) * 100}%")
    os.remove(plan_file)
    os.remove(gpt3_plan_file)
