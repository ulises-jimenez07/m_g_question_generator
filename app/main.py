import gradio as gr 
# from google.cloud import storage


def get_base_file() -> gr.File:
    return gr.File(file_count = "single",
                   label = "CV in PDF format",
                   file_types = [".pdf"],
                   type = "filepath",
                   show_label = True,
                   )

def get_base_markdown() -> None:
    return gr.Markdown(
        f"""
        ```

        



        ```
        """
        )


def clean() -> None:
    return (
        gr.File(file_count="single", 
                label="CV in PDF format",
                ),
        gr.Markdown(
        f"""
        ```

        



        ```
        """
        )
    )


def summarize_file(cv_file) -> gr.Markdown:
    # TODO:
    # storage_client = storage.Client()
    # bucket = storage_client.bucket(bucket_name)
    # blob = bucket.blob(destination_blob_name)
    # blob.upload_from_filename(file.name)

    gr.Info(f"File processed successfully!")
    return gr.Markdown(
                f"""
                It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
                """
            )


if __name__ == '__main__':
    demo = gr.Blocks(theme=gr.themes.Soft())
    
    with demo:
        gr.Markdown(
            f"""
            # M&G Q-Gen
            Assistant for Meet & Greet question generation
            """
        )
        with gr.Row():
            with gr.Column():
                cv_file = get_base_file()
                with gr.Row():
                    ddn_domain = gr.Dropdown(
                        choices = ["ML", "GenAI", "MLOps", "Conversational"],
                        value = None,
                        type = "value",
                        max_choices = 1,
                        label = "Domain",
                        info = "Domain selection for question generation",
                        # show_label = True,
                        interactive = True,
                    )

                with gr.Row():
                    btn_summarize = gr.Button(value="✨ Generate Questions!", interactive=True)
                    btn_clean = gr.Button(value="🗑️ Clean Up!", interactive=True)
        
            with gr.Column(visible=True) as summary_result:
                summary_markdown = get_base_markdown()

        btn_summarize.click(
            fn=summarize_file,
            inputs=[cv_file],
            outputs=[summary_markdown]
        )

        btn_clean.click(
            fn=clean,
            inputs=[],
            outputs=[
                cv_file,
                summary_markdown
            ]
        )

    demo.launch(debug=True, server_name="0.0.0.0", server_port=8080)