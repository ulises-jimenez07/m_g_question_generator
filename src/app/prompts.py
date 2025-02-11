"""This module contains prompts used for interacting with a language model."""

SYSTEM_PROMPT = """\
***System Instructions: ***

You are a Human Resources expert, in charge of extracting information from CV's
and resumes, and then generating questions about a candidate's past experience.

When generating questions, the questions have to be relevant to the
instructed prompt and as detailed as possible. Focus less on hypothetical cases,
the questions must be centered around the candidate's past experience instead.

Begin!
"""

EXTRACT_PROMPT = """\
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

GEN_EXP_PROMPT = """\
Generate a question that asks the candidate to introduce themselves and talk
about their previous experience at {company},
the question must be framed around the following domain: {domain}
"""

GEN_STACK_PROMPT = """\
Generate a question that asks the candidate about how they solved a particular
challenge as a {role} using the following tool: {tool}.
The question must ask for specifics in terms of implementation and preference.
"""

GEN_INDUSTRY_PROMPT = """\
Generate a question that asks the candidate about how they would apply {domain}
knowledge in the {industry} industry.
"""

GEN_DATA_PROMPT = """\
Generate a single question that asks the candidate about how they would apply
Exploratory Data Analysis as a {role} at {company}.
"""

GEN_GENAI_PROMPT = """\
Generate first a question that asks the candidate about general knowledge on
Generative AI. Then, generate a second question on common troubleshooting.
"""

GEN_CONSULTING_PROMPT = """\
Generate two questions that asks the candidate about how they have applied the
following soft skills: {skills} at {company}. These two questions must focus on a
consultative environment and can use any of the following tasks as a reference:
- working in cross-functional teams,
- creating visualizations for clarity purposes
- presenting to key stakeholders,
- preferences on working with other team members.
"""
