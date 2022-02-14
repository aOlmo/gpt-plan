
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
import yaml

import utils
from utils import *
from tarski.io import PDDLReader
from executor import *
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

def plan_execution(exec, DATA):
    """
    We need
        i. Initial State
       ii. Plan subset
      iii. Resulting state
    If prompt:
        Give Initial State, Plan Subset, a question regarding a pred in the resulting state and the answer
    else:
        Give Initial State, Plan Subset, a question regarding a pred in the resulting state
    :return:
    """
    initial_state = exec.init_state
    exec.random_prefix_execution()
    plan_prefix = exec.plan[:exec.prefix]
    resulting_state = exec.final_state
    for i in initial_state:
        pred = i.split('_')
        #Specific to blocksworld
        if pred[0]=="clear" or pred[0]=="handempty":
            continue



def generate_plan_subset():
    """
    We need
        i. Initial State
       ii. Plan subset
      iii. Resulting state
    If prompt:
        Give Initial State, Plan Subset and Resulting State as Goal State
    else:
        Give Initial State and Resulting State as Goal State.
    :return:
    """
    initial_state = exec.init_state
    exec.random_prefix_execution()
    plan_prefix = exec.plan[:exec.prefix]
    resulting_state = exec.final_state

def replanning_harder_easier():
    """

    :return:
    """
    exec.replanning()
    initial_state = exec.replanning_init
    plan_prefix = exec.plan[:exec.prefix]
    goal_state = exec.goal_state

N=20
if __name__=="__main__":
    with open('config.yaml', 'r') as file:
        DATA = yaml.safe_load(file)
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
            exec = executor(domain,cur_instance)
            """
            1. Executing Plans
            2. Generating a subset of a plan
            3. Replanning
            """
            print(f"Instance {cur_instance}")
            # --------------------------------------------- #

            # ------------ Put plan and instance into text ------------ #
            query += "\n[STATEMENT]\n"
            # inst_text,answer = instance_to_text_blocksworld(DOMAIN_TYPE, problem, not last_plan)
            # query+=inst_text
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

    
