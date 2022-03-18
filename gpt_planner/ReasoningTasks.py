import os
import numpy as np
import yaml
from gpt_plan_exec import executor

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

"""
Tasks:
T1. Goal-directed reasoning
T2. Paraphrasing of goals
T3. Plan subset completion
T4. Plan generalization
T5. Optimality
T6. Replanning
T7. Plan execution
"""


def do_t2_paraphrasing():
    cur_dir = os.getcwd()
    os.chdir("../gpt_plan_exec/")
    domain = 'instances/ipc_domain.pddl'
    problem = 'instances/ipc/instance-1.pddl'
    exec = executor(domain, problem)

    os.chdir(cur_dir)

    exec.random_prefix_execution()
    print("PLAN: ", exec.plan)
    print("INITIAL STATE: ", exec.init_state)
    print("After Plan Execution (A.P.E.) STATE: ", exec.final_state)
    print("GOAL STATE: ", exec.goal_state)
    print("NOT TRUE PREDS: ", exec.not_true_preds)


class ReasoningTasks():

    def __init__(self):
        self.engine = 'davinci'
        self.verbose = 1
        self.n_examples = 1

        self.plan_file = "sas_plan"
        self.gpt3_plan_file = "gpt_sas_plan"

    def read_config(self, config_file):
        with open(config_file, 'r') as file:
            self.data = yaml.safe_load(file)

    def do_t1_t4(self, config_file, task):

        self.read_config(config_file)

        if task == "t1":
            gen_blocksworld_problems(N_MAX, [4, 5])  # Generate N blocksworld problems
        elif task == "t4":
            gen_generalization_examples_blocksworld(N_MAX, self.data)

        domain_name = self.data['domain']
        domain_pddl = f'./instances/{self.data["file"]}'
        instance_folder = f'./instances/{domain_name}/'
        instance = f'./instances/{domain_name}/instance-{{}}.pddl'
        n_files = min(N_MAX, len(os.listdir(instance_folder)))

        correct_plans = 0
        for start in range(1, n_files - self.n_examples):
            query = INTRO
            for i in range(start, start + self.n_examples + 1):
                last_plan = True if i == start + self.n_examples else False
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
                plan = compute_plan(domain_pddl, cur_instance, self.plan_file)
                query += instance_to_text_blocksworld(problem, get_plan, self.data)
                # --------------------------------------------------------- #

            # Querying GPT-3
            gpt3_response = send_query_gpt3(query, self.engine, 120)

            # Do text_to_plan procedure
            gpt3_plan = text_to_plan_blocksworld(gpt3_response, problem.actions, self.gpt3_plan_file, self.data)

            if self.verbose:
                print(query)
                print("--------- GPT3 response ---------")
                print(gpt3_response)
                print("--------- Extracted plan ---------")
                print(gpt3_plan)
                print("--------- GT plan ---------")
                print(plan)

            # Apply VAL
            correct = int(validate_plan(domain_pddl, cur_instance, self.gpt3_plan_file))
            correct_plans += correct

        print(f"[+]: The number of correct plans is "
              f"{correct_plans}/{n_files - self.n_examples}={correct_plans / (n_files - self.n_examples) * 100}%")
        os.remove(self.plan_file)
        os.remove(self.gpt3_plan_file)


if __name__ == '__main__':
    tasks_obj = ReasoningTasks()
    config_file = './configs/t1_goal_directed_reasoning.yaml'
    # tasks_obj.do_t1_t4(config_file, "t1")
    do_t2_paraphrasing()

#######################
# if correct:
#     validate_plan(domain_pddl, cur_instance, gpt3_plan_file)
#     print("CORRECT PLAN BY GPT3!")
