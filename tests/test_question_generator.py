"""Module test_question_generator: Tests for the question generation functionality."""

import json
from unittest.mock import (
    MagicMock,
    patch,
)

import pytest

from app.question_generator import (
    GeminiModel,
    PdfExtractor,
    QuestionGenerator,
)

# Mock Gemini API response and extracted data
MOCK_EXTRACTED_TEXT = """
{
  "current_company": "Example Corp",
  "current_role": "Software Engineer",
  "tech_stack": ["Python", "Java", "AWS"],
  "soft_skills": ["Communication", "Teamwork"]
}
"""

MOCK_GENERATED_QUESTION = "This is a mock generated question."


@pytest.fixture
def mock_gemini_model():
    mock_model = MagicMock(spec=GeminiModel)
    mock_model.generate_content.return_value = MOCK_GENERATED_QUESTION
    return mock_model


@pytest.fixture
def mock_pdf_extractor():
    mock_extractor = MagicMock(spec=PdfExtractor)
    mock_extractor.extract_pdf.return_value = MOCK_EXTRACTED_TEXT
    mock_extractor.parse_extracted_data.return_value = json.loads(MOCK_EXTRACTED_TEXT)
    return mock_extractor


def test_generate_single_question(mock_gemini_model):
    question_generator = QuestionGenerator(mock_gemini_model, MagicMock(), "ML")  # Domain doesn't matter for this test
    question = question_generator.generate_single_question("Test prompt")
    mock_gemini_model.generate_content.assert_called_once_with(mock_gemini_model.call_model(), "Test prompt")
    assert question == MOCK_GENERATED_QUESTION


def test_extract_pdf_file_not_found(mock_gemini_model):
    mock_extractor = PdfExtractor(mock_gemini_model, "non_existent_file.pdf")
    with patch("app.question_generator.logger.error") as mock_logger_error:
        result = mock_extractor.extract_pdf()
        mock_logger_error.assert_called_once_with("File not found: non_existent_file.pdf")
    assert result is None


def test_extract_pdf_permission_error(mock_gemini_model):
    mock_extractor = PdfExtractor(mock_gemini_model, "non_existent_file.pdf")
    with (
        patch("app.question_generator.logger.error") as mock_logger_error,
        patch("builtins.open", side_effect=PermissionError),
    ):
        result = mock_extractor.extract_pdf()
        mock_logger_error.assert_called_once_with("Permission error accessing file: non_existent_file.pdf")
    assert result is None


def test_extract_pdf_os_error(mock_gemini_model):
    mock_extractor = PdfExtractor(mock_gemini_model, "non_existent_file.pdf")
    with (
        patch("app.question_generator.logger.error") as mock_logger_error,
        patch("builtins.open", side_effect=OSError("OS Error")),
    ):
        result = mock_extractor.extract_pdf()
        mock_logger_error.assert_called_once_with("OS error reading file: OS Error")
    assert result is None


def test_generate_questions_no_extracted_text(mock_gemini_model, mock_pdf_extractor):
    mock_pdf_extractor.extract_pdf.return_value = None  # Simulate failure to extract text
    question_generator = QuestionGenerator(mock_gemini_model, mock_pdf_extractor, "ML")
    questions = question_generator.generate_questions()
    assert not questions
