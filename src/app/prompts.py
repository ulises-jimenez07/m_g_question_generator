"""This module contains prompts used for interacting with the language model."""

EXTRACTION_SYSTEM_PROMPT = """\
***System Instructions: ***

You are a Human Resources expert, in charge of extracting information from CV's
and resumes.

Begin!
"""

INQUIRY_SYSTEM_PROMPT = """\
***System Instructions: ***

You are a Human Resources expert that generates questions about a candidate's
past experience.

When generating questions, the questions have to be relevant to the 
instructed prompt and as detailed as possible. 
Pay attetion to the prompt, some questions must be centered around the 
candidate's past experience. Other questions focus on hypothetical cases.

Begin!
"""

EXTRACT_JSON_PROMPT = """\
Extract the fields from the following list:

location (String)
current_role (String)
current_company (String)
last_degree_Studies (String)
certifications (Array of Strings)
soft_skills (Array of Strings)
tech_stack (Array of Strings)
past_experience (Array of Strings)
"""

TOOL_SELECTION_PROMPT = """\
Analyze a provided list of tech stack tools. Then select one from the list that
matches a provided role and can be used to solve specific tasks in a particular
provided domain.
Do not select coding languages and IDEs.
Do not select a tool from the list that matches exactly the domain.
Avoid selecting entire cloud platforms or code repository websites.
Focus on libraries and specific products.
The output must be only the selected tool, no explanation is needed.

**
Example:
- tools: [Java, Github, Azure, Airflow, Hive]
- role: Data Engineer
- domain: [Data]

Selected tool: Airflow**
**

The provided parameters are:
- tools: {tools}
- role: {role}
- domain: {domain}

Selected tool: 
"""

GENERATE_EXPERIENCE_PROMPT = """\
Generate a question that asks the candidate to introduce themselves and talk
about their previous experience at {company}.
The question must be framed around the following domain: {domain}.
"""

GENERATE_STACK_PROMPT = """\
Generate a question that asks the candidate about how they solved a particular 
challenge as a {role} using the following tool: {tool}.
The question must ask for specifics in terms of implementation and preference.
"""

GENERATE_INDUSTRY_PROMPT = """\
Generate a question that asks the candidate about how they would apply {domain} 
knowledge in the {industry} industry. 
Do not use any past experience in for this question, this is strictly an open
hypothetical question.
"""
GENERATE_DATA_PROMPT = """\
Generate a single question that asks the candidate about how they would apply 
Exploratory Data Analysis as a {role} at {company}.
"""

GENERATE_GENAI_PROMPT = """\
Generate first a question that asks the candidate about general knowledge on 
Generative AI. Then generate another question on simple troubleshooting.
Do not use any past experience in for this question, this is strictly an open
hypothetical question.
"""

GENERATE_CONSULTING_PROMPT = """\
Generate two questions that asks the candidate about how they have applied any
of the following soft skills: {skills} at {company}. These two questions must
focus on a consultative environment and can use any of the following tasks as
a reference:
- working in cross-functional teams, 
- creating visualizations for clarity purposes,
- presenting to key stakeholders, 
- preferences on working with other team members.
"""
