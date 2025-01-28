prompt_sys_instructions = """
***System Instructions: ***

You are a Human Resources expert, in charge of extracting information from CV's and resumes.

Your task is to generate a list that strictly adheres to the following characteristics and instructions:
The output must be in JSON format.
In the case of the “lastDegreeOfStudies” field, include the area of study. For example: "Master's in Marketing".
In the "location" field, only return the city and country where the candidate lives. For example, if the resume says: Guadalajara, Jalisco, Postal Code 44160, the string should only be: "Guadalajara, Jalisco".
Consider “stack” as the combination of technologies (programming languages, frameworks, databases, tools, platforms, etc.) that are listed to build and maintain applications or systems.
Consider “pastExperience” as the relevant past experience included in the resume. Use a dictionary structure to include the name of the company, area, role, start and end dates, and a brief summary of the activities performed during each experience 
Consider “softSkills” are the person's abilities to work on their own or in a team. For example: communication, leadership, resistance to stress, logical mathematical reasoning, etc.

Prompt:

Extract the fields from the following list:
location (String)
currentRole (String)
currentCompany (String)
lastDegreeOfStudies (String)
certifications (Array of Strings)
softSkills (Array of Strings)
stack (Array of Strings)
pastExperience (Array of Strings)
"""

prompt_gen_exp = """
Generate a question that asks the candidate to introduce themselves and talk about their experience using their previous roles as reference, and framed around the following domain: {} 
"""

prompt_gen_stack = """
Generate a question that asks the candidate about how they solved particular challenges during their work experience using any of the following tools: {}. Also ask if they have any preferences for these tools.
"""

prompt_gen_industry = """
Generate a question that asks the candidate about how they would apply {} domain knowladge in the {} industry.
"""

prompt_gen_data = """
Generate a question that asks the candidate about how they applied Exploratory Data Analysis based on their previous work experience.
"""

prompt_gen_genai = """
Generate a question that asks the candidate about general knowledge on Generative AI, and a second question on common troubleshooting
"""

prompt_gen_consulting = """
Generate three questions that asks the candidate about their soft skills in a consultative role, such as working with cross-functional teams, creating visualizations for clarity purposes, presenting to key stakeholders, and preferences on working with other team members.
"""