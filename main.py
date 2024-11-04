import traceback
import os
import gradio as gr
from functions.conversations import extract_response_bodies
from functions.url import extract_and_map_urls
from static_data import applications, llm_mapping, risk_ratings


def process_log_file(file_obj):
    try:
        if file_obj is None:
            return "No file uploaded", "Please upload a file first.", [], None

        file_content = file_obj.decode("utf-8")
        request_urls, matched_apps = extract_and_map_urls(file_content, applications)

        if matched_apps:
            first_app = next(iter(matched_apps))
            llm_detected = (
                f'LLM Detected : {llm_mapping.get(first_app, "No LLM detected")}'
            )
            conversations = extract_response_bodies(file_content, first_app)
            risk_details = risk_ratings.get(llm_mapping.get(first_app).lower(), None)
            if risk_details:
                risk_output = [[key, value] for key, value in risk_details.items()]
            else:
                risk_output = [
                    ["No Data", f"No specific risk rating available for {llm_detected}"]
                ]
        else:
            llm_detected = "Sorry, We do not support this application currently"
            conversations = ["No responses found"]
            risk_output = [["Status", "Risk Rating not available"]]

        urls_output = (
            "Request URLs:\n" + "\n".join(request_urls)
            if request_urls
            else "No URLs found"
        )
        detailed_output = f"{urls_output}\n\nConversations:\n{str(conversations)}"

        # Return None for file_input to clear it
        return llm_detected, detailed_output, risk_output, None

    except Exception as e:
        traceback.print_exc()
        return (
            f"Error: {str(e)}",
            f"Analysis failed. Error details: {str(e)}",
            [["Error", str(e)]],
            None,
        )


def load_predefined_log(app_name):
    try:
        log_file_path = f"logs/{app_name}_logs.txt"
        if os.path.exists(log_file_path):
            with open(log_file_path, "rb") as f:
                content = f.read()
                # Process the content directly instead of returning the file
                return process_log_file(content)
        else:
            return (
                "No file found",
                "Selected log file not found.",
                [["Error", "File not found"]],
                None,
            )
    except Exception as e:
        traceback.print_exc()
        return (
            f"Error: {str(e)}",
            f"Failed to load log. Error details: {str(e)}",
            [["Error", str(e)]],
            None,
        )


def create_interface():
    with gr.Blocks(
        theme=gr.themes.Base(
            primary_hue="blue",
            secondary_hue="slate",
            neutral_hue="slate",
        )
    ) as app:
        gr.Markdown(
            """
            # Dynamic Fingerprinting on Logs
            Analyze your log file for LLM detection, Or [Request app support for dynamic fingerprinting](https://forms.gle/FdydyXRP43EiBoVq9)
            """
        )

        # Add mode selection radio button
        mode = gr.Radio(
            choices=["Upload File", "Select Predefined Log"],
            label="Choose Input Mode",
            value="Upload File",
        )

        with gr.Row():
            with gr.Column(scale=1):
                # File upload components
                with gr.Group() as upload_group:
                    file_input = gr.File(
                        label="Upload Log File",
                        file_types=[".txt", ".log"],
                        type="binary",
                        interactive=True,  # Make it interactive by default
                        visible=True,
                    )
                    upload_button = gr.Button(
                        value="🔍 Analyze Uploaded File", variant="primary", size="lg"
                    )

                # Dropdown components
                with gr.Group(visible=False) as dropdown_group:
                    app_dropdown = gr.Dropdown(
                        label="Select Pre-Added Log",
                        choices=list(applications.keys()),
                        value=None,
                    )
                    load_button = gr.Button(
                        value="Load & Analyze Selected Log",
                        variant="primary",
                        size="lg",
                    )

                # LLM Detection section
                with gr.Group(visible=True):
                    gr.Markdown("### 🔍 LLM Detection Results")
                    llm_detection = gr.Markdown(
                        value="Awaiting file upload...", elem_classes="llm-detection"
                    )

                # Risk Rating section
                with gr.Group(visible=True):
                    gr.Markdown("### 📊 Risk Assessment")
                    risk_rating_output = gr.Dataframe(
                        headers=["Category", "Rating"],
                        datatype=["str", "str"],
                        wrap=True,
                        value=[["Awaiting", "file upload..."]],
                    )

            with gr.Column(scale=1):
                # Right column
                with gr.Group(visible=True):
                    gr.Markdown("### 📝 Detailed Analysis")
                    analysis_output = gr.Textbox(
                        label="Analysis Results",
                        lines=25,
                        max_lines=30,
                        show_copy_button=True,
                    )

        # Handle visibility toggling
        def toggle_visibility(choice):
            return (
                gr.update(visible=(choice == "Upload File")),  # For upload_group
                gr.update(
                    visible=(choice == "Select Predefined Log")
                ),  # For dropdown_group
            )

        mode.change(
            fn=toggle_visibility, inputs=[mode], outputs=[upload_group, dropdown_group]
        )

        # Handle file upload analysis
        upload_button.click(
            fn=process_log_file,
            inputs=[file_input],
            outputs=[llm_detection, analysis_output, risk_rating_output, file_input],
        )

        # Handle predefined log analysis
        load_button.click(
            fn=load_predefined_log,
            inputs=[app_dropdown],
            outputs=[llm_detection, analysis_output, risk_rating_output, file_input],
        )

    return app


if __name__ == "__main__":
    app = create_interface()
    app.launch(share=False, debug=True)
