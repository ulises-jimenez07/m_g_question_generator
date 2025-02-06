"""Meet & Greet Question Generator"""

import random
import json
from typing import Callable, Dict, List, Optional

from vertexai.preview.generative_models import (
    Part,
    GenerationConfig,
    # ResponseBlockedError,
)
import vertexai
vertexai.init(project="gsd-ai-mx-ulises", location="us-central1")

DOMAIN = "MLOPS"
INDUSTRY = None

from src import logger
from src.gemini import get_gemini
from src.gemini_schema import response_schema
from src.prompts import (
    system_prompt,
    extract_prompt,
    gen_exp_prompt,
    gen_stack_prompt,
    gen_industry_prompt,
    gen_data_prompt,
    gen_genai_prompt,
    gen_consulting_prompt,
)

class QuestionGenerator:
    """QuestionGenerator class.

    Attributes:
            resume_schema: Function calling tool.
    """
    def __init__(self):
        self.resume_schema = [response_schema]


    def call_system_model(self,
                        #   prompt: str,
                          max_output_tokens: Optional[int]=3000,
                          temperature: Optional[float]=0.5,
                          top_p: Optional[float]=1,
                          top_k: Optional[int]=40,
                          **kwargs,
                          ):
        """
            Makes a Gemini model call with system context.

            Args:
                self: The instance of the class containing this method.
                prompt str: A string that provides
                    the query prompt.
                max_output_tokens (Optional[int]): The maximum number of tokens
                    (words and punctuation) to generate in the response.
                    Defaults to 8192.
                temperature (Optional[float]): Controls the randomness of the
                    generated text. Higher temperature leads to more diverse
                    and creative responses, while lower temperature leads to
                    more predictable and safe responses. A good default is 0.2.
                top_p (Optional[float]): Implements nucleus sampling, where the
                    probability mass is focused on a subset of tokens with the
                    highest probabilities. Only consider tokens whose cumulative
                    probability exceeds `top_p`. A value between 0.1 and 1.0 is
                    typical.
                top_k (Optional[int]): Controls the vocabulary size considered 
                    for generation. Only the `top_k` most probable tokens will
                    be considered. Can be used for faster generation with 
                    smaller vocabularies.

            Returns:
                A call to a Gemini model using GenAI API.
        """
        return get_gemini(
            # prompt=prompt,
            # system_instruction=self.get_÷system_context(),
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens,
            # tools=self.resume_schema,
            **kwargs,
            )


    def get_system_context(self) -> str:
        """System model prompt.

        Returns:
            Chat model context to use as the first message of the chat model.
        """
        # context = system_prompt.format(
        #     curr_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        #     destinations=destinations
        # )
        # return context
        return system_prompt


    def extract_pdf(self, model):
        """PDF info extraction.

        Returns:
            Chat model context to use as the first message of the chat model.
        """

        prompt = extract_prompt
        pdf_file = Part.from_uri(
            uri="gs://mg-questions-bucket/cv_test/cv_1.pdf",
            mime_type="application/pdf",
            )
        contents = [pdf_file, prompt]
        config = GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema
            )
        
        response = model.generate_content(
            contents,
            generation_config=config
            )
        return response.text
    

    def generate_single_question(self, model, prompt):
        logger.info("Prompt: ", prompt)
        response = model.generate_content(prompt)
        return response.text


    def generate_questions(self):

        logger.info("Initializing Gemini model...")
        model = self.call_system_model()

        logger.info("Extracting info from PDF...")
        extracted_text = self.extract_pdf(
            model=model
            )
        json_extracted = json.loads(extracted_text)
        logger.info("extracted text: ", extracted_text)
        print("extracted text: ", extracted_text)

        questions = {}
        # Introductory previous experience question
        questions["experience"] = self.generate_single_question(
            model, 
            gen_exp_prompt.format(domain=DOMAIN)
            )
        
        # Stack question
        tool = random.choice(json_extracted["tech_stack"])
        questions["stack"] = self.generate_single_question(
            model, 
            gen_stack_prompt.format(tool=tool)
            )
        
        # (Optional) Industry-specific question
        if INDUSTRY:
            questions["industry"] = self.generate_single_question(
                model, 
                gen_industry_prompt.format(
                    domain=DOMAIN,
                    industry=INDUSTRY
                    )
                )
            
        # EDA question
        questions["data"] = self.generate_single_question(
            model, 
            gen_data_prompt.format(company=json_extracted["current_company"])
            )
        
        # EDA question
        questions["genai"] = self.generate_single_question(
            model, 
            gen_genai_prompt.format(company=json_extracted["current_company"])
            )
        
        # Consulting question
        questions["consulting"] = self.generate_single_question(
            model, 
            gen_consulting_prompt.format(company=json_extracted["current_company"])
            )        

        return questions


if __name__ == "__main__":
    q_generator = QuestionGenerator()
    questions = q_generator.generate_questions()
    print("Generated questions: \n")
    for k in questions.keys():
        print(f"Question {k}: {questions[k]} \n")
