import os
import numpy as np
import yaml
from gpt_plan_exec import executor

from utils import *
from tarski.io import PDDLReader

np.random.seed(42)

N_MAX = 61
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


class ReasoningTasks():
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

    def __init__(self, engine):
        # TODO: Possibly add config file here
        self.engine = engine
        self.verbose = 0
        self.n_examples = 1
        self.max_gpt_response_length = 500

        self.plan_file = "sas_plan"
        self.gpt3_plan_file = "gpt_sas_plan"

    # -------------------------------------- UTILS -------------------------------------- #
    def compute_plan(self, domain, instance, timeout=30):
        fast_downward_path = os.getenv("FAST_DOWNWARD")
        cmd = f"timeout {timeout}s {fast_downward_path}/fast-downward.py {domain} {instance} --search \"astar(lmcut())\" > /dev/null 2>&1"
        os.system(cmd)

        if not os.path.exists(self.plan_file):
            return ""
        return Path(self.plan_file).read_text()

    def read_config(self, config_file):
        with open(config_file, 'r') as file:
            self.data = yaml.safe_load(file)

    def get_problem(self, instance, domain):
        reader = PDDLReader(raise_on_error=True)
        reader.parse_domain(domain)
        return reader.parse_instance(instance)

    def get_executor(self, instance, domain):
        cur_dir = os.getcwd()
        os.chdir("../gpt_plan_exec/")
        exec = executor(domain, instance)
        os.chdir(cur_dir)
        return exec

    # -------------------------------------- TASKS -------------------------------------- #
    def t1_t4(self, config_file, task):
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
                cur_instance = instance.format(i)
                print(f"Instance {cur_instance}")
                # --------------- Read Instance --------------- #
                problem = self.get_problem(cur_instance, domain_pddl)
                # --------------------------------------------- #
                # ------------ Put plan and instance into text ------------ #
                plan = self.compute_plan(domain_pddl, cur_instance)
                query += fill_template(*instance_to_text_blocksworld(problem, get_plan, self.data))
                # --------------------------------------------------------- #

            # Querying GPT-3
            gpt3_response = send_query_gpt3(query, self.engine, self.max_gpt_response_length)

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

    def t2_paraphrasing(self, config_file):
        def convert_state_to_text(state):
            text_list = []
            for i in state:
                pred = i.split('_')
                objs = [self.data["encoded_objects"][j] for j in pred[1:]]
                text_list.append(self.data['predicates'][pred[0]].format(*objs))

            state_text = text_list[0]
            if len(text_list) > 1:
                state_text = ", ".join(text_list[:-1]) + f" and {text_list[-1]}"

            return state_text

        def paraphrase_goal(exec):
            exec.complete_plan_execution()
            goal_state, full_state = list(exec.goal_state), list(exec.final_state)
            random.shuffle(goal_state)

            return convert_state_to_text(goal_state), convert_state_to_text(full_state)

        gen_blocksworld_problems(N_MAX, [4, 5])

        self.read_config(config_file)

        domain_name = self.data['domain']
        domain = f'./instances/{self.data["file"]}'
        instance = f'./instances/{domain_name}/instance-{{}}.pddl'


        skipped = 0
        corrects = {"Random": 0, "Full->Specific": 0, "Specific->Full": 0}
        for i in range(1, N_MAX):
            cur_instance = instance.format(i)
            exec = self.get_executor(cur_instance, domain)

            problem = self.get_problem(cur_instance, domain)
            gt_plan = self.compute_plan(domain, cur_instance)
            if gt_plan == "":
                print(f"[-]: Timeout or error gathering Ground Truth plan for {cur_instance}. Continuing...")
                skipped += 1
                continue

            goal_random, goal_full = paraphrase_goal(exec)
            try:
                init_specific, goal_specific, plan_specific = instance_to_text_blocksworld(problem, True, self.data)
                init_specific_shuffled, goal_specific_shuffled, _ = instance_to_text_blocksworld(problem, True, self.data, shuffle=True)
            except:
                print(f"[-]: Excess amount of objects for instance {cur_instance}. Continuing...")
                skipped += 1
                continue

            # =============== Random =============== #
            query = INTRO
            query += fill_template(init_specific, goal_specific, plan_specific)
            query += fill_template(init_specific_shuffled, goal_specific_shuffled, "")

            gpt3_response = send_query_gpt3(query, self.engine, self.max_gpt_response_length)
            gpt3_plan = text_to_plan_blocksworld(gpt3_response, problem.actions, self.gpt3_plan_file, self.data)

            corrects["Random"] += int(validate_plan(domain, cur_instance, self.gpt3_plan_file))

            # =============== Full->Specific and Specific->Full =============== #
            descriptions = list(corrects.keys())[1:]
            for goal_1, goal_2, descr in zip([goal_specific, goal_full], [goal_full, goal_specific], descriptions):
                query = INTRO
                query += fill_template(init_specific, goal_1, plan_specific)
                query += fill_template(init_specific_shuffled, goal_2, "")

                gpt3_response = send_query_gpt3(query, self.engine, self.max_gpt_response_length)
                gpt3_plan = text_to_plan_blocksworld(gpt3_response, problem.actions, self.gpt3_plan_file, self.data)

                corrects[descr] += int(validate_plan(domain, cur_instance, self.gpt3_plan_file))

                if self.verbose:
                    print(query)
                    print("--------- GPT3 response ---------")
                    print(gpt3_response)
                    print("--------- Extracted plan ---------")
                    print(gpt3_plan)
                    print("--------- GT plan ---------")
                    print(gt_plan)

            os.remove(self.plan_file)
            os.remove(self.gpt3_plan_file)

            exec_plans = i - skipped
            print("Results")
            for k in corrects:
                print(f"{k} {corrects[k]}/{exec_plans} = {round(corrects[k]/exec_plans*100, 2)}%")


if __name__ == '__main__':
    tasks_obj = ReasoningTasks('curie')
    config_file = './configs/t2_paraphrasing.yaml'
    # tasks_obj.t1_t4(config_file, "t4")
    tasks_obj.t2_paraphrasing(config_file)

#######################
# if correct:
#     validate_plan(domain_pddl, cur_instance, gpt3_plan_file)
#     print("CORRECT PLAN BY GPT3!")
