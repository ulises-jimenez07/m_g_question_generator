"""Module provides a function to create a Gemini instance with specified configuration."""

from dataclasses import dataclass
from typing import (
    List,
    Optional,
    Union,
)

from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
    Tool,
)


@dataclass
class GeminiConfig:
    """Configuration for Gemini model.

    Attributes:
        temperature: Controls the randomness of the generated text.
            Higher temperature leads to more diverse and creative responses,
            while lower temperature leads to more predictable and safe responses.
            A good default is 0.2.
        top_p: Implements nucleus sampling, where the probability mass is
            concentrated on a subset of tokens with the highest probabilities.
            Only consider tokens whose cumulative probability exceeds `top_p`.
            A value between 0.1 and 1.0 is typical.
        top_k: Controls the vocabulary size considered for generation.
            Only the `top_k` most probable tokens will be considered.
            Can be used for faster generation with smaller vocabularies.
        candidate_count: The number of candidate responses to generate
            before selecting one. Defaults to 1.
        max_output_tokens: The maximum number of tokens
            (words and punctuation) to generate in the response.
            Defaults to 8192.
        stop_sequences: A list of sequences that will cause generation to stop
            if encountered in the generated text.
        tools: A list of tools to use in conjunction with the generative model.
        system_instruction: Either a Part or string that provides the overall
            system prompt.
    """

    temperature: Optional[float] = 0.2
    top_p: Optional[float] = 1
    top_k: Optional[int] = 32
    candidate_count: Optional[int] = 1
    max_output_tokens: Optional[int] = 8192
    stop_sequences: Optional[List[str]] = None
    tools: Optional[List[Tool]] = None
    system_instruction: Optional[Union[Part, str]] = None


def get_gemini(config: GeminiConfig):
    """Create a Gemini instance.

    Configure a Gemini instance with the provided parameters.

    Args:
        config: The configuration for the Gemini model.

    Returns:
        A GenerativeModel Gemini instance.
    """
    return GenerativeModel(
        model_name="gemini-1.5-flash-002",
        generation_config=GenerationConfig(
            temperature=config.temperature,
            top_p=config.top_p,
            top_k=config.top_k,
            candidate_count=config.candidate_count,
            max_output_tokens=config.max_output_tokens,
            stop_sequences=config.stop_sequences,
        ),
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
        tools=config.tools,
        system_instruction=config.system_instruction,
    )
