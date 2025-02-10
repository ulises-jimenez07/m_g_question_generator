"""Function Call declarations."""

response_schema = {
    "type": "object",
    "required": [
        "location",
        "current_role",
        "current_company",
        "last_degree_studies",
        "soft_skills",
        "tech_stack",
        "past_experience"
    ],
    "properties": {
        "location": {
            "type": "string",
            "example": "Guadalajara, Jalisco, Mexico",
            "description": "REQUIRED! The candidate location formatted as 'city, state, country'."
        },
        "current_role": {
            "type": "string",
            "example": "Cloud AI Engineer",
            "description": "REQUIRED! The current or latest role the candidate has held in a working environment."
        },
        "current_company": {
            "type": "string",
            "example": "Google",
            "description": "REQUIRED! The current or latest company the candidate has worked at."
        },
        "last_degree_studies": {
            "type": "string",
            "description": "REQUIRED! The degree of the latest studies completed by the candidate, including area of study."
        },
        "certifications": {
            "type": "array",
            "description": "List of certifications held by the candidate.",
            "items": {
                "type": "string",
                "example": "Professional Machine Learning Engineer, Google Cloud",
                "description": "The certification held by the candidate and the company that validates the accreditation."
            }
        },
        "soft_skills":{
            "type": "array",
            "description": "List of candidate's soft skills.",
            "items": {
                "type": "string",
                "example": "team work",
                "description": "A candidate's ability to work on their own or in a team."
            }
        },
        "tech_stack": {
            "type": "array",
            "description": "List of technologies in which the candidate is proficient.",
            "items": {
                "type": "string",
                "example": "Python",
                "description": "A technologies (programming languages, frameworks, databases, tools, platforms, etc.) that is used to build and maintain applications or systems."
            }
        },
        "past_experience": {
            "type": "array",
            # Consider “pastExperience” as the relevant 
            # past experience included in the resume. Use a dictionary structure to include the name of the company, 
            # area, role, start and end dates, and a brief summary of the activities performed during each experience 
            "description": "List of activities performed by the candidate during their last work experience. Provide at least 2.",
            "items": {
                "type": "string",
                "description": "REQUIRED! Actions performed by the candidate."
            }
        }
    }
}