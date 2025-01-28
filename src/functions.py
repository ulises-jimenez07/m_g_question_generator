"""Function Call declarations"""

format_llm_func = {
    "name": "format_llm",
    "description": "Returns information from PDF resume.",
    "parameters": {
        "type": "object",
        "required": [
            "location",
            "current_role",
            "current_company",
            "last_degree_studies",
            "certifications",
            "soft_skills",
            "tech_stack",
            "past_experience"
        ],
        "properties": {
            "location": {
                "type": "string",
                "example": "Guadalajara, Jalisco",
                "description": "REQUIRED! The three-letter IATA code of the departure city airport."
            },
            "departure_date_earliest": {
                "type": "string",
                "format": "date",
                "description": "REQUIRED! Earliest date of departure. This date must be in the future."
            },
            "departure_date_latest": {
                "type": "string",
                "format": "date",
                "description": "Latest date of departure. This date must be later than departure_date_earliest. This date must be in the future."
            },
            "length_of_stay_min": {
                "type": "integer",
                "description": "The minimum number of days to travel"
            },
            "length_of_stay_max": {
                "type": "integer",
                "description": "The maximum number of days to travel."
            },
            "max_budget":{
                "type": "integer",
                "example": 500,
                "description": "Max Budget specified by user. A user may say less than [number]. Default value is null."
            },
            "max_number_of_stops": {
                "type": "integer",
                "description": "The maximum number of connections before reaching the final destination."
            },
            "destination_cities_airport_codes": {
                "type": "array",
                "description": "List of IATA codes that are 3 characters. Provide at least 6 cities. Required to be valid airport codes and never an empty list!",
                "items": {
                    "type": "string",
                    "description": "REQUIRED! The three-letter IATA code of the destination city. THESE MUST BE VALID 3 CHARACTER AIRPORT CODES!!"
                }
            }
        }
	}
}