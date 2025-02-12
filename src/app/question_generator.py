"""Meet & Greet Question Generator"""

import json
from typing import (
    Dict,
    Optional,
)

import vertexai
from gemini import (
    GeminiConfig,
    get_gemini,
)
from gemini_schema import response_schema
from logging_utils import logger
from prompts import (
    EXTRACT_JSON_PROMPT,
    EXTRACTION_SYSTEM_PROMPT,
    GENERATE_CONSULTING_PROMPT,
    GENERATE_DATA_PROMPT,
    GENERATE_EXPERIENCE_PROMPT,
    GENERATE_GENAI_PROMPT,
    GENERATE_INDUSTRY_PROMPT,
    GENERATE_STACK_PROMPT,
    INQUIRY_SYSTEM_PROMPT,
    TOOL_SELECTION_PROMPT,
)
from vertexai.preview.generative_models import (
    GenerationConfig,
    Part,
)

vertexai.init(project="gsd-ai-mx-ulises", location="us-central1")


INDUSTRY = "retail"


class SystemContext:
    """Handles system context."""

    def get_system_context(self, mode: Optional[str] = None) -> str:
        """System model prompt."""

        assert mode in [None, "extraction", "inquiry"]
        if mode == "extraction":
            return EXTRACTION_SYSTEM_PROMPT
        if mode == "inquiry":
            return INQUIRY_SYSTEM_PROMPT

        return None


class GeminiModel:
    """Handles Gemini model interactions."""

    def __init__(self, system_context: SystemContext):
        self.system_context = system_context

    def call_model(
        self,
        max_output_tokens: Optional[int] = 1024,
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
            system_instruction=self.system_context.get_system_context(**kwargs),
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

    def __init__(self, model: GeminiModel, pdf_path: str):
        self.model = model
        self.pdf_path = pdf_path

    def extract_pdf(self):
        """PDF info extraction."""
        prompt = EXTRACT_JSON_PROMPT
        if self.pdf_path.startswith("gs://"):
            pdf_file = Part.from_uri(
                uri=self.pdf_path,
                mime_type="application/pdf",
            )
        else:
            try:
                with open(self.pdf_path, "rb") as f:
                    pdf_file = Part.from_data(data=f.read(), mime_type="application/pdf")
            except FileNotFoundError:
                logger.error(f"File not found: {self.pdf_path}")
                return None
            except PermissionError:
                logger.error(f"Permission error accessing file: {self.pdf_path}")
                return None
            except OSError as e:  # Catching a more specific exception.
                logger.error(f"OS error reading file: {e}")
                return None
        contents = [pdf_file, prompt]
        config = GenerationConfig(response_mime_type="application/json", response_schema=response_schema)
        return self.model.generate_content(
            self.model.call_model(mode="extraction"), contents, generation_config=config
        )

    def parse_extracted_data(self, extracted_text):
        """Parses extracted JSON data."""
        json_extracted = json.loads(extracted_text)
        return json_extracted


class QuestionGenerator:
    """Generates interview questions."""

    def __init__(self, model: GeminiModel, pdf_extractor: PdfExtractor, domain: str):  # Added domain parameter
        self.model = model
        self.pdf_extractor = pdf_extractor
        self.domain = domain  # Store the domain

    def generate_single_question(self, prompt):
        """Generates a single question."""
        logger.debug(f"Prompt: {prompt}")
        return self.model.generate_content(self.model.call_model(mode="inquiry"), prompt)

    def select_tool(self, prompt):
        """Generates a single question."""
        logger.debug(f"Prompt: {prompt}")
        return self.model.generate_content(self.model.call_model(), prompt)

    def generate_questions(self) -> Dict[str, str]:
        """Generates all interview questions."""
        logger.info("Extracting info from PDF...")
        extracted_text = self.pdf_extractor.extract_pdf()

        if extracted_text is None:  # added null check.
            return {}

        json_extracted = self.pdf_extractor.parse_extracted_data(extracted_text)
        json_formatted_str = json.dumps(json_extracted, indent=2)
        logger.info(f"Extracted JSON: {json_formatted_str}")

        logger.info("Generating questions...")
        # config = GeminiConfig(
        #     temperature=0.5,
        #     top_p = 1.0,
        #     top_k= 32,
        #     max_output_tokens=128,
        #     system_instruction=self.set_system_context(
        #         mode="inquiry"
        #         )
        # )
        # model = self.call_system_model(config)

        # Initialize dict for storing questions
        questions = {}
        questions["experience"] = self.generate_single_question(
            GENERATE_EXPERIENCE_PROMPT.format(
                company=json_extracted["current_company"], domain=self.domain
            )  # Use self.domain
        )

        # tool = random.choice(json_extracted["tech_stack"])
        logger.info("Selecting tool for questioning...")
        tool = self.generate_single_question(
            TOOL_SELECTION_PROMPT.format(
                tools=json_extracted["tech_stack"], role=json_extracted["current_role"], domain=self.domain
            )
        )
        questions["stack"] = self.generate_single_question(
            GENERATE_STACK_PROMPT.format(role=json_extracted["current_role"], tool=tool)
        )

        if INDUSTRY:
            questions["industry"] = self.generate_single_question(
                GENERATE_INDUSTRY_PROMPT.format(domain=self.domain, industry=INDUSTRY)
            )

        questions["data"] = self.generate_single_question(
            GENERATE_DATA_PROMPT.format(role=json_extracted["current_role"], company=json_extracted["current_company"])
        )

        questions["genai"] = self.generate_single_question(GENERATE_GENAI_PROMPT)

        questions["consulting"] = self.generate_single_question(
            GENERATE_CONSULTING_PROMPT.format(
                skills=json_extracted["soft_skills"], company=json_extracted["current_company"]
            )
        )

        return questions
