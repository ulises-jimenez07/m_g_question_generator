"""Meet & Greet Question Generator"""

import json
import random
from typing import Optional

import logger
import response_schema
import vertexai
from gemini import get_gemini
from prompts import (
    extract_prompt,
    gen_consulting_prompt,
    gen_data_prompt,
    gen_exp_prompt,
    gen_genai_prompt,
    gen_industry_prompt,
    gen_stack_prompt,
    system_prompt,
)
from vertexai.preview.generative_models import (
    GenerationConfig,
    Part,
)

vertexai.init(project="gsd-ai-mx-ulises", location="us-central1")

DOMAIN = "MLOPS"
INDUSTRY = None


class QuestionGenerator:
    """QuestionGenerator class.

    Attributes:
            resume_schema: Function calling tool.
    """

    def __init__(self, use_ds=False):
        self.resume_schema = [response_schema]
        self.use_ds = use_ds

    def call_system_model(
        self,
        max_output_tokens: Optional[int] = 3000,
        temperature: Optional[float] = 0.5,
        top_p: Optional[float] = 1,
        top_k: Optional[int] = 40,
        **kwargs,
    ):
        """
        Makes a Gemini model call with system context.

        Args:
            max_output_tokens: The maximum number of tokens to generate.
            temperature: Controls the randomness of the generated text.
            top_p: Implements nucleus sampling.
            top_k: Controls the vocabulary size considered for generation.

        Returns:
            A call to a Gemini model using GenAI API.
        """
        return get_gemini(
            system_instruction=self.get_system_context(),
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens,
            **kwargs,
        )

    def get_system_context(self) -> str:
        """System model prompt."""
        return system_prompt

    def extract_pdf(self, model):
        """PDF info extraction."""

        prompt = extract_prompt
        pdf_file = Part.from_uri(
            uri="gs://mg-questions-bucket/cv_test/cv_1.pdf",
            mime_type="application/pdf",
        )
        contents = [pdf_file, prompt]
        config = GenerationConfig(response_mime_type="application/json", response_schema=response_schema)

        response = model.generate_content(contents, generation_config=config)
        return response.text

    def generate_single_question(self, model, prompt):
        logger.debug(f"Prompt: {prompt}")
        response = model.generate_content(prompt)
        return response.text

    def generate_questions(self):
        logger.info("Initializing Gemini model...")
        model = self.call_system_model()

        logger.info("Extracting info from PDF...")
        extracted_text = self.extract_pdf(model=model)
        json_extracted = json.loads(extracted_text)
        json_formatted_str = json.dumps(json_extracted, indent=2)
        logger.info(f"Extracted JSON: {json_formatted_str}")

        questions = {}
        # Introductory previous experience question
        questions["experience"] = self.generate_single_question(
            model, gen_exp_prompt.format(company=json_extracted["current_company"], domain=DOMAIN)
        )

        # Stack question -  TODO: Implement more precise stack tool selection
        tool = random.choice(json_extracted["tech_stack"])
        questions["stack"] = self.generate_single_question(
            model, gen_stack_prompt.format(role=json_extracted["current_role"], tool=tool)
        )

        # (Optional) Industry-specific question
        if INDUSTRY:
            questions["industry"] = self.generate_single_question(
                model, gen_industry_prompt.format(domain=DOMAIN, industry=INDUSTRY)
            )

        # EDA question
        questions["data"] = self.generate_single_question(
            model,
            gen_data_prompt.format(role=json_extracted["current_role"], company=json_extracted["current_company"]),
        )

        # GenAI question
        questions["genai"] = self.generate_single_question(model, gen_genai_prompt)

        # Consulting question
        questions["consulting"] = self.generate_single_question(
            model,
            gen_consulting_prompt.format(
                skills=json_extracted["soft_skills"], company=json_extracted["current_company"]
            ),
        )

        return questions


if __name__ == "__main__":
    q_generator = QuestionGenerator()
    questions = q_generator.generate_questions()
    print("Generated questions: \n")
    for question_type, question_text in questions.items():  # Iterate using .items()
        print(f"Question {question_type}: {question_text} \n")
