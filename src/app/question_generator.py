"""Meet & Greet Question Generator"""

import json
import random
from typing import Optional

import vertexai
from gemini import (
    GeminiConfig,
    get_gemini,
)
from gemini_schema import response_schema
from logging_utils import logger
from prompts import (
    EXTRACT_PROMPT,
    GEN_CONSULTING_PROMPT,
    GEN_DATA_PROMPT,
    GEN_EXP_PROMPT,
    GEN_GENAI_PROMPT,
    GEN_INDUSTRY_PROMPT,
    GEN_STACK_PROMPT,
    SYSTEM_PROMPT,
)
from vertexai.preview.generative_models import (
    GenerationConfig,
    Part,
)

vertexai.init(project="gsd-ai-mx-ulises", location="us-central1")

DOMAIN = "MLOPS"
INDUSTRY = None


class SystemContext:
    """Handles system context."""

    def get_system_context(self) -> str:
        """System model prompt."""
        return SYSTEM_PROMPT


class GeminiModel:
    """Handles Gemini model interactions."""

    def __init__(self, system_context: SystemContext):
        self.system_context = system_context

    def call_model(
        self,
        max_output_tokens: Optional[int] = 3000,
        temperature: Optional[float] = 0.5,
        top_p: Optional[float] = 1,
        top_k: Optional[int] = 40,
        **kwargs,
    ):
        """Makes a Gemini model call."""
        config = GeminiConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens,
            system_instruction=self.system_context.get_system_context(),
            **kwargs,
        )
        return get_gemini(config)

    def generate_content(self, model, prompt, generation_config=None):
        """Generates content using the Gemini model."""
        if generation_config:
            response = model.generate_content(prompt, generation_config=generation_config)
        else:
            response = model.generate_content(prompt)
        return response.text


class PdfExtractor:
    """Extracts information from a PDF."""

    def __init__(self, model: GeminiModel):
        self.model = model

    def extract_pdf(self):
        """PDF info extraction."""
        prompt = EXTRACT_PROMPT
        pdf_file = Part.from_uri(
            uri="gs://mg-questions-bucket/cv_test/cv_1.pdf",
            mime_type="application/pdf",
        )
        contents = [pdf_file, prompt]
        config = GenerationConfig(response_mime_type="application/json", response_schema=response_schema)
        return self.model.generate_content(self.model.call_model(), contents, generation_config=config)

    def parse_extracted_data(self, extracted_text):
        """Parses extracted JSON data."""
        json_extracted = json.loads(extracted_text)
        return json_extracted


class QuestionGenerator:
    """Generates interview questions."""

    def __init__(self, model: GeminiModel, pdf_extractor: PdfExtractor):
        self.model = model
        self.pdf_extractor = pdf_extractor

    def generate_single_question(self, prompt):
        """Generates a single question."""
        logger.debug(f"Prompt: {prompt}")
        return self.model.generate_content(self.model.call_model(), prompt)

    def generate_questions(self):
        """Generates all interview questions."""
        logger.info("Extracting info from PDF...")
        extracted_text = self.pdf_extractor.extract_pdf()
        json_extracted = self.pdf_extractor.parse_extracted_data(extracted_text)
        json_formatted_str = json.dumps(json_extracted, indent=2)
        logger.info(f"Extracted JSON: {json_formatted_str}")

        questions = {}
        questions["experience"] = self.generate_single_question(
            GEN_EXP_PROMPT.format(company=json_extracted["current_company"], domain=DOMAIN)
        )

        tool = random.choice(json_extracted["tech_stack"])
        questions["stack"] = self.generate_single_question(
            GEN_STACK_PROMPT.format(role=json_extracted["current_role"], tool=tool)
        )

        if INDUSTRY:
            questions["industry"] = self.generate_single_question(
                GEN_INDUSTRY_PROMPT.format(domain=DOMAIN, industry=INDUSTRY)
            )

        questions["data"] = self.generate_single_question(
            GEN_DATA_PROMPT.format(role=json_extracted["current_role"], company=json_extracted["current_company"])
        )

        questions["genai"] = self.generate_single_question(GEN_GENAI_PROMPT)

        questions["consulting"] = self.generate_single_question(
            GEN_CONSULTING_PROMPT.format(
                skills=json_extracted["soft_skills"], company=json_extracted["current_company"]
            )
        )

        return questions


if __name__ == "__main__":
    system_context = SystemContext()
    model = GeminiModel(system_context)
    pdf_extractor = PdfExtractor(model)
    q_generator = QuestionGenerator(model, pdf_extractor)
    questions = q_generator.generate_questions()
    print("Generated questions: \n")
    for question_type, question_text in questions.items():
        print(f"Question {question_type}: {question_text} \n")
