import requests
import traceback

import gradio as gr


import traceback
import requests
import json
from datetime import datetime

def process_log_file(file_obj):
    try:
        if file_obj is None:
            return "No file uploaded", "Please upload a file first.", [], None

        # Read and parse JSON content
        file_content = file_obj.decode("utf-8")
        log_data = json.loads(file_content)
        
        # Validate JSON structure
        required_fields = ["file_name", "time", "type", "logs"]
        if not all(field in log_data for field in required_fields):
            raise ValueError("Invalid log file format. Missing required fields.")

        # Process each application's logs
        api_url = "https://f0cc-35-185-180-76.ngrok-free.app/predict"
        headers = {"Content-Type": "application/json"}
        
        all_results = []
        for app_log in log_data["logs"]:
            app_name = app_log.get("app_name", "Unknown App")
            log_text = app_log.get("log", "")
            
            if log_text:
                # Send the entire log as one text
                payload = {"texts": [log_text]}
                response = requests.post(api_url, headers=headers, json=payload)
                response.raise_for_status()
                
                result = response.json()
                prediction = result.get("predictions", ["Unknown"])[0]
                
                all_results.append({
                    "app_name": app_name,
                    "model": prediction,
                    "log_length": len(log_text)
                })
        
        # Prepare outputs
        llm_detected = "### LLM Detection Results\n\n"
        for result in all_results:
            llm_detected += f"**{result['app_name']}**:\n"
            llm_detected += f"- Detected Model: {result['model']}\n"
            llm_detected += f"- Log Length: {result['log_length']} characters\n\n"
        
        # Prepare detailed analysis
        detailed_output = (
            f"File Analysis Results\n"
            f"File Name: {log_data['file_name']}\n"
            f"Log Type: {log_data['type']}\n"
            f"Analysis Time: {log_data['time']}\n\n"
        )
        
        for result in all_results:
            detailed_output += f"\nApplication: {result['app_name']}\n"
            detailed_output += f"Detected Model: {result['model']}\n"
            detailed_output += f"Log Size: {result['log_length']} characters\n"
            detailed_output += "-" * 50 + "\n"
        
        # Prepare summary table
        risk_output = [
            ["Analysis Time", log_data['time']],
            ["File Name", log_data['file_name']],
            ["Log Type", log_data['type']],
            ["Total Applications", str(len(log_data['logs']))],
        ]
        
        # Add results for each app
        for result in all_results:
            risk_output.append([
                f"{result['app_name']} Analysis",
                f"Model: {result['model']}"
            ])

        # Return None for file_input to clear it
        return llm_detected, detailed_output, risk_output, None

    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON format: {str(e)}"
        return error_msg, error_msg, [["Error", error_msg]], None
    except requests.exceptions.RequestException as e:
        error_msg = f"API Request Failed: {str(e)}"
        return error_msg, error_msg, [["Error", error_msg]], None
    except Exception as e:
        traceback.print_exc()
        error_msg = f"Analysis failed. Error: {str(e)}"
        return error_msg, error_msg, [["Error", str(e)]], None

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
            Analyze your log file for LLM fingerprinting, Or [Request app support for dynamic fingerprinting](https://forms.gle/FdydyXRP43EiBoVq9)
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                # File upload components
                file_input = gr.File(
                    label="Upload Log File (TXT, LOG, JSON)",
                    file_types=[".txt", ".log", ".json"],
                    type="binary",
                    interactive=True,
                    visible=True,
                )
                upload_button = gr.Button(
                    value="🔍 Analyze Uploaded File", variant="primary", size="lg"
                )

                # LLM Detection section
                with gr.Group(visible=True):
                    gr.Markdown("### 🔍 LLM Detection Results")
                    llm_detection = gr.Markdown(
                        value="Awaiting file upload...", elem_classes="llm-detection"
                    )

                # Risk Rating section
                with gr.Group(visible=True):
                    gr.Markdown("### 📊 Analysis Summary")
                    risk_rating_output = gr.Dataframe(
                        headers=["Category", "Details"],
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
                        show_copy_button=True,
                    )

        # Handle file upload analysis
        upload_button.click(
            fn=process_log_file,
            inputs=[file_input],
            outputs=[llm_detection, analysis_output, risk_rating_output, file_input],
        )

    return app


if __name__ == "__main__":
    app = create_interface()
    app.launch(share=False, debug=True)
