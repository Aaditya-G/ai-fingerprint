import traceback
import gradio as gr
from functions.conversations import extract_response_bodies
from functions.url import extract_and_map_urls
from static_data import applications, llm_mapping, risk_ratings

def process_log_file(file_obj):
    try:
        if file_obj is None:
            return "No file uploaded", "Please upload a file first.", []

        file_content = file_obj.decode('utf-8')
        request_urls, matched_apps = extract_and_map_urls(file_content, applications)
        
        if matched_apps:
            first_app = next(iter(matched_apps))
            llm_detected = f'LLM Detected : {llm_mapping.get(first_app, "No LLM detected")}'
            conversations = extract_response_bodies(file_content, first_app)
            risk_details = risk_ratings.get(llm_mapping.get(first_app).lower(), None)
            if risk_details:
                # Convert risk_details directly to list of lists for DataFrame
                risk_output = [[key, value] for key, value in risk_details.items()]
            else:
                risk_output = [["No Data", f"No specific risk rating available for {llm_detected}"]]
        else:
            llm_detected = "Sorry, We do not support this application currently"
            conversations = ["No responses found"]
            risk_output = [["Status", "Risk Rating not available"]]

        urls_output = "Request URLs:\n" + "\n".join(request_urls) if request_urls else "No URLs found"
        detailed_output = f"{urls_output}\n\nConversations:\n{str(conversations)}"
        
        return llm_detected, detailed_output, risk_output

    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}", f"Analysis failed. Error details: {str(e)}", [["Error", str(e)]]

def create_interface():
    with gr.Blocks(theme=gr.themes.Base(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
    )) as app:
        gr.Markdown(
            """
            # Dynamic Fingerprinting on Logs
            Upload your log file for analysis and LLM detection
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                # Left column
                file_input = gr.File(
                    label="Upload Log File",
                    file_types=[".txt", ".log"],
                    type="binary"
                )
                
                # LLM Detection section
                with gr.Group(visible=True):
                    gr.Markdown("### 🔍 LLM Detection Results")
                    llm_detection = gr.Markdown(
                        value="Awaiting file upload...",
                        elem_classes="llm-detection"
                    )
                
                upload_button = gr.Button(
                    value="🔍 Analyze File",
                    variant="primary",
                    size="lg"
                )
                
                # Risk Rating section
                with gr.Group(visible=True):
                    gr.Markdown("### 📊 Risk Assessment")
                    risk_rating_output = gr.Dataframe(
                        headers=["Category", "Rating"],
                        datatype=["str", "str"],
                        wrap=True,
                        value=[["Awaiting", "file upload..."]]
                    )
            
            with gr.Column(scale=1):
                # Right column
                with gr.Group(visible=True):
                    gr.Markdown("### 📝 Detailed Analysis")
                    analysis_output = gr.Textbox(
                        label="Analysis Results",
                        lines=25,
                        max_lines=30,
                        show_copy_button=True
                    )

        upload_button.click(
            fn=process_log_file,
            inputs=[file_input],
            outputs=[llm_detection, analysis_output, risk_rating_output]
        )

    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch(share=True, debug=True)
    