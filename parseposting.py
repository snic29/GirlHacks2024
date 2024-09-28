from openai import AzureOpenAI
import os

def call_openai_chat(prompt):
    client = AzureOpenAI(
        azure_endpoint = "https://oai-usnc-gpt01.openai.azure.com/",
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2023-03-15-preview"
    )
    completion = client.chat.completions.create(
        model = "gpt-35-turbo",
        messages = prompt,
        temperature = 0,
        top_p = 0.95,
        frequency_penalty = 0,
        presence_penalty = 0,
        stop = None
    )
    text = completion.choices[0].message.content
    return text

def getDesiredTraits(posting):
    openaimsg = [{"role": "user", "content": '''
                    Given this job posting, and the inferred company culture, extract the 10 most important qualities an applicant should have. Return as comma separated values.'''}] 
    openaimsg.append({"role": "user", "content": "Job Posting: {}, AI:".format(posting)})
    desiredSkills = call_openai_chat(openaimsg)
    return desiredSkills

#TODO: write function to go through all files in postings folder to extract skills

with open('postings/bofa.txt', 'r', encoding='utf-8') as file:
    posting = file.read()
    file.close()

print(getDesiredTraits(posting))