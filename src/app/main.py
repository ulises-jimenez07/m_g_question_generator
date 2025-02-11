"""
Gradio app for generating Meet & Greet questions based on a provided CV.
"""

import gradio as gr
from question_generator import (
    GeminiModel,
    PdfExtractor,
    QuestionGenerator,
    SystemContext,
)


def get_base_file() -> gr.File:
    return gr.File(
        file_count="single",
        label="CV in PDF format",
        file_types=[".pdf"],
        type="filepath",
        show_label=True,
    )


def get_base_markdown():
    return gr.Markdown(
        """
        ```





        ```
        """
    )


def clean():  # Removed unused arguments
    return (
        gr.File(file_count="single", label="CV in PDF format", value=None),
        gr.Markdown(
            """
        ```





        ```
        """
        ),
        gr.Dropdown(
            choices=["ML", "GenAI", "MLOps", "Conversational"],
            value=None,
            type="value",
            max_choices=1,
            label="Domain",
            info="Domain selection for question generation",
            interactive=True,
        ),
    )


def summarize_file(cv_file, ddn_domain) -> gr.Markdown:
    if cv_file is None:
        return gr.Markdown("No file uploaded.")

    if ddn_domain is None:
        return gr.Markdown("No domain selected.")

    system_context = SystemContext()
    model = GeminiModel(system_context)
    pdf_extractor = PdfExtractor(model, cv_file)
    q_generator = QuestionGenerator(model, pdf_extractor, ddn_domain)
    questions = q_generator.generate_questions()

    if questions:
        output_markdown = ""
        for question_type, question_text in questions.items():
            output_markdown += f"**Question {question_type}:** {question_text} \n\n"
        return gr.Markdown(output_markdown)

    return gr.Markdown("Error generating questions. Please check the logs.")  # Removed unnecessary else


if __name__ == "__main__":
    demo = gr.Blocks(theme=gr.themes.Soft())

    with demo:
        gr.Markdown(
            """
            # M&G Q-Gen
            Assistant for Meet & Greet question generation
            """
        )
        with gr.Row():
            with gr.Column():
                cv_file = get_base_file()
                with gr.Row():
                    ddn_domain = gr.Dropdown(
                        choices=["ML", "GenAI", "MLOps", "Conversational"],
                        value=None,
                        type="value",
                        max_choices=1,
                        label="Domain",
                        info="Domain selection for question generation",
                        interactive=True,
                    )

                with gr.Row():
                    btn_summarize = gr.Button(value="✨ Generate Questions!", interactive=True)
                    btn_clean = gr.Button(value="🗑️ Clean Up!", interactive=True)

            with gr.Column(visible=True) as summary_result:
                summary_markdown = get_base_markdown()
        # pylint: disable=E1101
        btn_summarize.click(fn=summarize_file, inputs=[cv_file, ddn_domain], outputs=[summary_markdown])
        # pylint: disable=E1101
        btn_clean.click(
            fn=clean,
            inputs=[],  # Removed unused inputs
            outputs=[
                cv_file,
                summary_markdown,
                ddn_domain,
            ],
        )

    demo.launch(debug=True, server_name="0.0.0.0", server_port=8080)
