import os
import platform
import sys
import json
import openai
from openai import AzureOpenAI

os_type = platform.system()
if os_type == 'Linux':
    delimiter="/"
elif os_type=='Windows':
    delimiter="\\"
    
try:
    with open("scripts" + delimiter + "config.json",'r') as config_file:
        config=json.load(config_file)
    config_file.close()
except FileNotFoundError:
    print("config.json not found\n")
    sys.exit(6)

if "key" not in config["azure_openai_gpt-4_turbo"]:
    if os.getenv("AZURE_OPENAI_API_KEY") is not None:
        config["azure_openai_gpt-4_turbo"]["key"]=os.getenv("AZURE_OPENAI_API_KEY")
    else:
        print("API key missing: Set environment variable \"AZURE_OPENAI_API_KEY\" with key value for access to \"azure_openai_gpt-4_turbo\"\n")
        sys.exit(7)

def call_openai_chat(model, prompt):
    try:
        client = AzureOpenAI(
        azure_endpoint = model["endpoint"],
        api_key = model["key"],
        api_version=model["api_version"]
        )
        completion = client.chat.completions.create(
            model = model["engine"],
            messages = prompt,
            temperature = 0,
            top_p = 0.95,
            frequency_penalty = 0,
            presence_penalty = 0,
            stop = None
        )
        text = completion.choices[0].message.content
    
    except openai.AuthenticationError as e:
        print(f"Error Accessing OpenAI: {e}.Check your key.")
        sys.exit(2)
    except Exception as e:
        print(f"Error Accessing OpenAI: {e}")

    return text

def getDesiredTraits(posting):
    openaimsg = [{"role": "user", "content": '''
                    Given this job posting, and the inferred company culture, extract the 10 most important qualities an applicant should have. Only return a list of comma separated values. No other text.'''}] 
    openaimsg.append({"role": "user", "content": "Job Posting: {}".format(posting)})
    desiredSkills = call_openai_chat(config["azure_openai_gpt-4_turbo"], openaimsg)
    return desiredSkills

def getResumeTraits(resume):
    openaimsg = [{"role": "user", "content": '''
                    Given this resume, extract all the important skills and qualities the individual has. Only return a list of comma separated values. No other text.'''}] 
    openaimsg.append({"role": "user", "content": "Resume: {}".format(resume)})
    candidateSkills = call_openai_chat(openaimsg)
    return candidateSkills

def main():
    try:
        with open('postings/merck.txt', 'r', encoding='utf-8') as file:
            posting = file.read()
            file.close()
    except FileNotFoundError:
        print("Test File not Found")
        sys.ext(5)
    try:
        with open('resumes/jake.txt', 'r', encoding='utf-8') as file:
            resume = file.read()
            file.close()
    except FileNotFoundError:
        print("Test File not Found")
        sys.ext(5)

    print(getDesiredTraits(posting))
    print(getResumeTraits(resume))
    return

if __name__ == "__main__":
    main()