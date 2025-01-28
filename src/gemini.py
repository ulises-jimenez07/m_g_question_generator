"""Get a Gemini instance."""

from typing import List, Optional, Union

from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Tool,
    Part
)

def get_gemini(
    *,
    temperature: Optional[float] = 0.2,
    top_p: Optional[float] = 1,
    top_k: Optional[int] = 32,
    candidate_count: Optional[int] = 1,
    max_output_tokens: Optional[int] = 8192,
    stop_sequences: Optional[List[str]] = None,
    tools: Optional[List[Tool]] = None,
    system_instruction: Optional[Union[Part, str]] = None
):
    """
    Creates a Gemini instance with access to the following parameters:

    Args:
        - temperature (Optional[float]): Controls the randomness of the
            generated text. Higher temperature leads to more diverse
            and creative responses, while lower temperature leads to more
            predictable and safe responses. A good default is 0.2.
        - top_p (Optional[float]): Implements nucleus sampling, where the
            probability mass is concentrated on a subset of tokens with the
            highest probabilities. Only consider tokens whose cumulative
            probability exceeds `top_p`. A value between 0.1 and 1.0 is typical.
        - top_k (Optional[int]): Controls the vocabulary size considered for
            generation. Only the `top_k` most probable tokens will be
            considered. Can be used for faster generation with smaller
            vocabularies.
        - candidate_count (Optional[int]): The number of candidate responses to
            generate before selecting one. Defaults to 1.
        - max_output_tokens (Optional[int]): The maximum number of tokens
            (words and punctuation) to generate in the response.
            Defaults to 8192.
        - stop_sequences (Optional[List[str]]): A list of sequences that
            will cause generation to stop if encountered in
            the generated text.
        - tools (Optional[List[Tool]]): A list of tools to use
            in conjunction with the generative model.
        - system_instruction (Optional[Union[Part, str]]): Either a Part
            or string that provides the overall system prompt.

    Returns:
        A GenerativeModel Gemini instance.

    """
    return GenerativeModel(
        model_name = "gemini-1.5-flash-002",
        generation_config = GenerationConfig(
            temperature = temperature,
            top_p = top_p,
            top_k = top_k,
            candidate_count = candidate_count,
            max_output_tokens = max_output_tokens,
            stop_sequences = stop_sequences
        ),
        safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
        tools = tools,
        system_instruction=system_instruction
    )
