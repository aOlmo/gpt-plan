"""
1. Parse grounded domain
2. generate a plan
3. take subset of actions
4.
"""
from model_parser.parser_new import parse_model
from model_parser.writer_new import ModelWriter
from model_parser.constants import *
import os
import random
class executor():
    def __init__(self,domain,problem):
        self.pr_domain, self.pr_problem = self.ground_domain(domain,problem)
        self.model = parse_model(self.pr_domain,self.pr_problem)
        self.plan,self.init_state,self.final_state,self.all_preds,self.not_true_preds,self.goal_preds = [None]*6
    def one_plan_subset_instance(self):
        self.plan = self.get_plan(self.pr_domain,self.pr_problem)
        self.init_state = self.get_sets(self.model[INSTANCE][INIT][PREDICATES])
        # print(self.model[INSTANCE][INIT][PREDICATES])
        # for act in self.model[DOMAIN]:
        #     print(act==self.plan[0])
        #     print(self.model[DOMAIN][act][ADDS])
        #     print(self.model[DOMAIN][act][DELS])
        self.final_state = self.get_final_state()
        self.all_preds = self.get_sets(self.model[PREDICATES])
        self.not_true_preds = self.all_preds.difference(self.final_state)
        self.goal_preds =  self.get_sets(self.model[INSTANCE][GOAL])


    def get_plan(self,domain,problem):
        CMD_FD = f"~/RADAR-X/planner/FAST-DOWNWARD/fast-downward.py {domain} {problem} --search \"astar(lmcut())\" >/dev/null 2>&1"
        os.system(CMD_FD)
        #USE SAS PLAN to get actions
        plan = []
        with open('sas_plan') as f:
            for line in f:
                if ';' not in line:
                    plan.append((line.strip()[1:-1].strip()).upper())
        subset = random.choice(list(range(len(plan))))
        return plan[:subset]
    def get_sets(self,list_of_preds):
        return set([i[0] for i in list_of_preds])

    def get_final_state(self,):
        initial_state = self.init_state

        for act in self.plan:
            act_adds = self.get_sets(self.model[DOMAIN][act][ADDS])
            act_dels = self.get_sets(self.model[DOMAIN][act][DELS])
            initial_state = initial_state.union(act_adds)
            initial_state = initial_state.difference(act_dels)

        return initial_state



    def ground_domain(self,domain,problem):
        CMD_PR2 = f"~/RADAR-X/planner/PR2/pr2plan -d {domain}  -i {problem} -o blank_obs.dat >/dev/null 2>&1"
        os.system(CMD_PR2)
        pr_domain = 'pr-domain.pddl'
        pr_problem = 'pr-problem.pddl'
        self.remove_explain(pr_domain, pr_problem)
        return pr_domain, pr_problem

    def remove_explain(self,domain, problem):
        try:
            cmd = 'cat {0} | grep -v "EXPLAIN" > pr-problem.pddl.tmp && mv pr-problem.pddl.tmp {0}'.format(problem)
            os.system(cmd)
            cmd = 'cat {0} | grep -v "EXPLAIN" > pr-domain.pddl.tmp && mv pr-domain.pddl.tmp {0}'.format(domain)
            os.system(cmd)
        except:
            raise Exception('[ERROR] Removing "EXPLAIN" from pr-domain and pr-problem files.')
if __name__=="__main__":
    domain = 'instances/ipc_domain.pddl'
    problem = 'instances/instance-1.pddl'
    exec = executor(domain,problem)
    for i in range(5):
        print("\n")
        exec.one_plan_subset_instance()
        print("PLAN: ", exec.plan)
        print("INITIAL STATE: ", exec.init_state)
        print("After Plan Execution (A.P.E.) STATE: ", exec.final_state)
        print("GOAL STATE: ", exec.goal_preds)
        print("NOT TRUE PREDS: ", exec.not_true_preds)