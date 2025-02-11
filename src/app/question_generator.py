"""Meet & Greet Question Generator"""

import json
from typing import Optional, Dict

import vertexai
from src.app import logger
from src.app.gemini import (
    GeminiConfig,
    get_gemini,
)
from src.app.gemini_schema import response_schema
from src.app.prompts import (
    EXTRACTION_SYSTEM_PROMPT,
    INQUIRY_SYSTEM_PROMPT,
    EXTRACT_JSON_PROMPT,
    TOOL_SELECTION_PROMPT,
    GENERATE_EXPERIENCE_PROMPT,
    GENERATE_STACK_PROMPT,
    GENERATE_DATA_PROMPT,
    GENERATE_INDUSTRY_PROMPT,
    GENERATE_GENAI_PROMPT,
    GENERATE_CONSULTING_PROMPT
)
from vertexai.preview.generative_models import (
    GenerationConfig,
    Part,
)

vertexai.init(project="gsd-ai-mx-ulises", location="us-central1")

DOMAIN = "MLOPS"
INDUSTRY = "retail"


class QuestionGenerator:
    """QuestionGenerator class.

    Attributes:
            resume_schema: Function calling tool.
    """

    def __init__(self, use_ds=False):
        self.resume_schema = [response_schema]
        self.use_ds = use_ds

    def call_system_model(self, config: GeminiConfig):
        """
        Makes a Gemini model call with system context.

        Args:
            system_instruction: provides a context for the task at hand.
            max_output_tokens: The maximum number of tokens to generate.
            temperature: Controls the randomness of the generated text.
            top_p: Implements nucleus sampling.
            top_k: Controls the vocabulary size considered for generation.

        Returns:
            A call to a Gemini model using Vertex SDK.
        """

        return get_gemini(
            config=config,
        )


    def set_system_context(self, mode="extraction") -> str:
        """System model prompt.

        Args:
            mode: indicates if system instruction is meant for
            extraction from PDF file or question generation.
            Only "extraction" or "inquiry" values are allowed.

        Returns:
            Chat model context to use system instructions.
        """
        assert mode in ["extraction", "inquiry"]
        if mode=="extraction":
            return EXTRACTION_SYSTEM_PROMPT
        elif mode=="inquiry":
            return INQUIRY_SYSTEM_PROMPT


    def extract_pdf(self) -> str:
        """PDF info extraction.
        
        Args:
            model: model used to generate text response
            for PDF extraction.

        Returns:
            Generated response text in JSON format.
        """

        logger.debug("Initializing Gemini model...")
        config = GeminiConfig(
            temperature=0.2,
            top_p = 0.8,
            top_k= 32,
            max_output_tokens=1024,
            system_instruction=self.set_system_context(
                mode="extraction",
            )
        )
        model = self.call_system_model(config)

        prompt = EXTRACT_JSON_PROMPT
        pdf_file = Part.from_uri(
            uri="gs://mg-questions-bucket/cv_test/cv_1.pdf",
            mime_type="application/pdf",
        )
        contents = [pdf_file, prompt]

        response = model.generate_content(
            contents,
            generation_config=GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        return response.text
    

    def get_response_text(self, model, prompt):
        """Get response from prompting model.
        
        Args:
            model: model used to generate text response
            based on standard prompt.

        Returns:
            Generated response text
        """
        logger.info(f"Prompt: {prompt}")
        response = model.generate_content(prompt)
        return response.text

    def generate_questions(self) -> Dict[str, str]:
        """Get generated questions.

        Returns:
            Dictionary with generated questions for 
            each category. 
        """

        logger.info("Extracting info from PDF...")
        extracted_text = self.extract_pdf()
        logger.info(f"Extracted string: {extracted_text}")
        json_extracted = json.loads(extracted_text)
        json_formatted_str = json.dumps(json_extracted, indent=2)
        logger.info(f"Extracted JSON: {json_formatted_str}")

        logger.info("Generating questions...")
        logger.debug("Initializing Gemini model...")
        config = GeminiConfig(
            temperature=0.5,
            top_p = 1.0,
            top_k= 32,
            max_output_tokens=128,
            system_instruction=self.set_system_context(
                mode="inquiry"
                )
        )
        model = self.call_system_model(config)

        # Initialize dict for storing questions
        questions = {}
        # Introductory previous experience question
        questions["experience"] = self.get_response_text(
            model, 
            GENERATE_EXPERIENCE_PROMPT.format(
                company=json_extracted["current_company"],
                domain=DOMAIN
                )
            )
        
        # Stack question
        logger.info("Selecting tool for questioning...")
        tool = self.get_response_text(
            model,
            TOOL_SELECTION_PROMPT.format(
                tools=json_extracted["tech_stack"],
                role=json_extracted["current_role"],
                domain=DOMAIN
            )
        )
        questions["stack"] = self.get_response_text(
            model, 
            GENERATE_STACK_PROMPT.format(
                role=json_extracted["current_role"],
                tool=tool
            )
        )
        
        # (Optional) Industry-specific question
        if INDUSTRY:
            questions["industry"] = self.get_response_text(
                model, 
                GENERATE_INDUSTRY_PROMPT.format(
                    domain=DOMAIN,
                    industry=INDUSTRY
                    )
                )
            
        # EDA question
        questions["data"] = self.get_response_text(
            model, 
            GENERATE_DATA_PROMPT.format(
                role=json_extracted["current_role"],
                company=json_extracted["current_company"]
                )
            )
        
        # GenAI question
        questions["genai"] = self.get_response_text(
            model,
            GENERATE_GENAI_PROMPT
            )
        
        # Consulting question
        questions["consulting"] = self.get_response_text(
            model, 
            GENERATE_CONSULTING_PROMPT.format(
                skills=json_extracted["soft_skills"],
                company=json_extracted["current_company"]
                )
            )        

        return questions


if __name__ == "__main__":
    q_generator = QuestionGenerator()
    questions = q_generator.generate_questions()
    print("Generated questions: \n")
    for question_type, question_text in questions.items():  # Iterate using .items()
        print(f"Question {question_type}: {question_text} \n")
