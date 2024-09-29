import os
import platform
import sys
import json
import argparse
import openai
from openai import AzureOpenAI

#from azure.identity import DefaultAzureCredential, get_bearer_token_provider

os_type=platform.system()
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
    

def call_openai_chat(model,prompt):
    try:
        client = AzureOpenAI(
            azure_endpoint=model["endpoint"],
            api_key=model["key"],
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

    
def evalDocument(inputDocument, model, prompt):
    #prompt : ''' Given this job posting, and the inferred company culture, extract the 10 most important qualities an applicant should have. Return as comma separated values.'''
    #file : postings/bofa.txt
    #model : "Azure OpenAI GPT-4 turbo", "Azure OpenAI GPT-4o", "Azure OpenAI GPT 3.5 Turbo"
    
    
    openaimsg = [{"role": "user", "content": prompt}] 
    openaimsg.append({"role": "user", "content": "HR Document: {}, AI:".format(inputDocument)})
    relevantSkills = call_openai_chat(config[model],openaimsg)

    return relevantSkills


def main():

    parser = argparse.ArgumentParser(description="Evaluate Resume  / Job Posting based on Prompt")  
    parser.add_argument("-file", required=True, help="Path to the Resume/Posting.")  
    parser.add_argument("-prompt", required=True, help="Prompt")  
    parser.add_argument("-model", required=True, help="Azure OpenAI Model.")
      
    args = parser.parse_args()  # Parse command-line arguments  

    try: 
        with open(args.file, 'r', encoding='utf-8') as file:
            inputDocument = file.read()
        file.close()
    except FileNotFoundError:
        print(args.file + "  file not found\n")
        sys.exit(5)
    
    
    if "key" not in config[args.model]:
        if os.getenv("AZURE_OPENAI_API_KEY") is not None:
            config[args.model]["key"]=os.getenv("AZURE_OPENAI_API_KEY")
        else:
            print("API key missing: Set environment variable \"AZURE_OPENAI_API_KEY\" with key value for access to " + args.model + "\n")
            sys.exit(7)
        
    print(evalDocument(inputDocument, args.model, args.prompt))
    return 
    
#Execute main
if __name__ == "__main__":
    main()