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
                    Given this job posting, and the inferred company culture, extract the 10 most important qualities an applicant should have. Only return a list of comma separated values. No other text.'''}] 
    openaimsg.append({"role": "user", "content": "Job Posting: {}".format(posting)})
    desiredSkills = call_openai_chat(openaimsg)
    return desiredSkills

def getResumeTraits(resume):
    openaimsg = [{"role": "user", "content": '''
                    Given this resume, extract all the important skills and qualities the individual has. Only return a list of comma separated values. No other text.'''}] 
    openaimsg.append({"role": "user", "content": "Resume: {}".format(resume)})
    candidateSkills = call_openai_chat(openaimsg)
    return candidateSkills



if __name__ == "__main__":  
    with open('postings/merck.txt', 'r', encoding='utf-8') as file:
        posting = file.read()
        file.close()

    with open('resumes/jake.txt', 'r', encoding='utf-8') as file:
        resume = file.read()
        file.close()

    desired_skills = getDesiredTraits(posting).split(",")
    print("Desired Skills: ", desired_skills, "\n")
    candidate_skills = getResumeTraits(resume).split(",")
    print("Candidate Skills: ", candidate_skills, "\n")

