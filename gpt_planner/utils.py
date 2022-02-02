import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

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
            presence_penalty=0)
    except:
        max_token_err_flag = True
        print("[-]: Failed GPT3 query execution")

    text_response = response["choices"][0]["text"] if not max_token_err_flag else ""
    return text_response.strip()


def validate_plan(domain, instance, plan_file):
    cmd = f"Validate {domain} {instance} {plan_file}"
    text = os.popen(cmd).read()
    return True if "successful" in text else False
