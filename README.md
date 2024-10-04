# Project for GirlHacks 2024

# Inspiration
As CS college students, we understand the challenges of applying for internships in a competitive environment. We saw a need for a tool that could help applicants identify skill shortages in their resumes and highlight areas to focus on for improvement. Our aim is to use AI to assist students in enhancing their applications and transforming the hiring process, ultimately increasing their chances of becoming more desirable candidates for internships and jobs.

# What It Does
The app utilizes Azure OpenAI to identify critical skills from job candidates' resumes and desired traits from job postings. Its user-friendly interface enables experimentation with various prompts and models, paving the way for future capabilities that match candidates with job postings while offering tailored recommendations to enhance their success in pursuing desired positions.

# Build Process
Developed a Flask application in Python and deployed it on Azure Web Services. The integration of Azure OpenAI and three different large language models (LLMs) allows users to evaluate the effectiveness of submitted resumes.

# Challenges
- Establishing the cloud infrastructure, particularly setting up the web services resource in Azure.
- Integrating the Azure web service with our repository and performing redeployments.
- Addressing issues with the OpenAI library not being automatically included in the Linux Python image of Azure Web Services.
- Encountering time constraints during the initial deployment of the MySQL database in the cloud, which limited my ability to load reference datasets (skill sets, categories, etc.).
- Navigating my limited knowledge of advanced Retrieval-Augmented Generation (RAG) techniques, which will enhance this solution once mastered.

# Accomplishments
- Successful deployment of various cloud services.
- Efficient programmatic interaction with cloud services.
- Enhanced collaborative iteration thanks to the cloud environment created.
- The opportunity to work on a use case with the potential for significant impact on a large user base.

# Things Learned
- A new architectural pattern for applications requiring both syntactic and semantic search, and the relevant technologies (AI Search, embeddings, LLM models) to implement it.
- Alternative deployment options for cloud applications beyond traditional virtual machines and containers.
- Debugging techniques for Azure Web Application Services.

# What's next for Resume Remix
- Implementing a RAG-based solution that utilizes AI Search, embeddings, and LLM models.
- Deploying an API management solution to serve a larger client base.
- Establishing robust security controls covering identity and access management, logging and monitoring, infrastructure protection, and data protection.
- Automating Azure infrastructure deployments using Terraform.
- Evaluating models of different vendors and monitoring for bias over time.
- Extensive evaluations to ensure a fair and auditable AI solution consisent with the principles and laws that govern our society.
