import os
import numpy as np

from utils import *
from tarski.io import PDDLReader
np.random.seed(42)

N = 20
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
    DOMAIN_TYPE = "generated"  # ipc/generated

    # Generate N blocksworld problems
    if DOMAIN_TYPE == "generated": gen_blocksworld_problems([4, 5], N+10)

    domain = f'./instances/{DOMAIN_TYPE}_domain.pddl'
    instance = f'./instances/{DOMAIN_TYPE}/instance-{{}}.pddl'
    plan_file = "sas_plan"
    gpt3_plan_file = "gpt_sas_plan"
    engine = 'davinci'

    n_examples = 1
    cur_instance = ""

    verbose = 1
    correct_plans = 0

    query = ""
    for start in range(1, N-n_examples):
        query = INTRO
        for i in range(start, start+n_examples+1):
            last_plan = True if i == start + n_examples else False
            # --------------- Read Instance --------------- #
            cur_instance = instance.format(i)
            reader = PDDLReader(raise_on_error=True)
            reader.parse_domain(domain)
            problem = reader.parse_instance(cur_instance)
            lang = problem.language
            print(f"Instance {cur_instance}")
            # --------------------------------------------- #

            # ------------ Put plan and instance into text ------------ #
            query += "\n[STATEMENT]\n"
            plan = compute_plan(domain, cur_instance, plan_file)
            query += instance_to_text_blocksworld(DOMAIN_TYPE, problem, not last_plan)
            # --------------------------------------------------------- #

        # Querying GPT-3
        gpt3_response = send_query_gpt3(query, engine, 120)

        # Do text_to_plan procedure
        gpt3_plan = text_to_plan_blocksworld(DOMAIN_TYPE, gpt3_response, problem.actions, gpt3_plan_file)

        if verbose:
            print(query)
            print("--------- GPT3 response ---------")
            print(gpt3_response)
            print("--------- Extracted plan ---------")
            print(gpt3_plan)
            print("--------- GT plan ---------")
            print(plan)

        # Apply VAL
        correct = int(validate_plan(domain, cur_instance, gpt3_plan_file))
        if correct:
            validate_plan(domain, cur_instance, gpt3_plan_file)
            print("CORRECT PLAN BY GPT3!")
        correct_plans += correct

    print(f"[+]: The number of correct plans is {correct_plans}/{N}={correct_plans/N*100}%")
