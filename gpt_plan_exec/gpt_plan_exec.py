
"""
We need to have:
1. Domain
2. Initial State
3. Plan
4. Resulting State

We translate 1,2,3,4,2,3 to natural language for GPT-3 and then get the response.
We then translate the response back into PDDL and check if the response exists in 4
"""


import os
import numpy as np
import utils
from utils import *
from tarski.io import PDDLReader
np.random.seed(42)


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
N=20
if __name__=="__main__":
    #Generate blocksworld problems
    DOMAIN_TYPE = "ipc"
    #gen_blocksworld_problems([4,5],N+10)
    domain = f'./instances/ipc_domain.pddl'
    instance = f'./instances/instance-{{}}.pddl'
    plan_file = "sas_plan"
    gpt3_plan_file = "gpt_sas_plan"
    engine = 'davinci'

    n_examples = 1
    cur_instance = ""

    verbose = 1
    correct_answers = 0

    query = ""
    for start in range(1,N-n_examples):
        query=INTRO
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
            try:
                goal = ''.join((treat_on(utils.LETTERS_DICT,atom))[0] for atom in problem.goal.subformulas)
            except:
                goal = ''.join((treat_on(utils.LETTERS_DICT,atom))[0])
            inst_text,answer = instance_to_text_blocksworld(DOMAIN_TYPE, problem, not last_plan)

            query+=inst_text
            # --------------------------------------------------------- #
        # print("QUERY------------\n",query)
        # print(answer)
        # Querying GPT-3
        gpt3_response = send_query_gpt3(query, engine, 120)

        # Do text_to_plan procedure
        # gpt3_plan = text_to_plan_blocksworld(DOMAIN_TYPE, gpt3_response, problem.actions, gpt3_plan_file)

        if verbose:
            print(query)
            print("--------- GPT3 response ---------")
            print(gpt3_response)
            print("--------- Correct response ---------")
            print(answer)

    #     # Apply VAL
    #     correct = int(validate_plan(domain, cur_instance, gpt3_plan_file))
    #     if correct:
    #         validate_plan(domain, cur_instance, gpt3_plan_file)
    #         print("CORRECT PLAN BY GPT3!")
    #     correct_plans += correct
    #
    # print(f"[+]: The number of correct plans is {correct_plans}/{N}={correct_plans/N*100}%")

    
