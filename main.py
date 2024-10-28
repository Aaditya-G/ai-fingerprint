import traceback
import gradio as gr
from functions.conversations import extract_response_bodies
from functions.url import extract_and_map_urls

applications = {
    "github_copilot": r"githubcopilot",
    "grammarly": r"grammarly",
    "leena": r"leena",
    "microsoft_copilot": r"copilot",
    "multion": r"multion",
    "notion": r"notion",
    "postman": r"postman"
}

llm_mapping = {
    "github_copilot": "GPT-3.5",
    "microsoft_copilot": "GPT-3.5",
    "grammarly": "GPT-3.5",
    "leena": "GPT-3.5",
    "multion": "GPT-3.5",
    "notion": "GPT-3.5",
    "postman": "GPT-3.5"
}

def process_log_file(file_obj):
    try:
        if file_obj is None:
            return "No file uploaded", "Please upload a file first."

        file_content = file_obj.decode('utf-8')
        request_urls, matched_apps = extract_and_map_urls(file_content, applications)
        
        if matched_apps:
            first_app = next(iter(matched_apps))
            llm_detected = llm_mapping.get(first_app, "No LLM detected")
            conversations = extract_response_bodies(file_content, first_app)
        else:
            llm_detected = "No LLM detected"
            conversations = ["No responses found"]

        urls_output = "Request URLs:\n" + "\n".join(request_urls) if request_urls else "No URLs found"
        detailed_output = f"{urls_output}\n\nConversations:\n{str(conversations)}"
        
        return llm_detected, detailed_output

    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}", f"Analysis failed. Error details: {str(e)}"

with gr.Blocks(theme=gr.themes.Default()) as app:
    gr.Markdown("# Dynamic Fingerpritning on Logs")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
                label="Upload Log File",
                file_types=[".txt", ".log"],
                type="binary"
            )
            
            llm_detection = gr.Markdown(
                value="LLM Detection Status",
                label="Detection Result"
            )
            
            upload_button = gr.Button(
                value="Analyze File",
                variant="primary"
            )
        
        with gr.Column(scale=1):
            analysis_output = gr.Textbox(
                label="Detailed Analysis",
                lines=20,
                max_lines=30,
                show_copy_button=True
            )

    upload_button.click(
        fn=process_log_file,
        inputs=[file_input],
        outputs=[llm_detection, analysis_output]
    )

if __name__ == "__main__":
    app.launch(share=True, debug=True)