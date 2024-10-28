import os
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

input_folder = "logs"
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    with open(file_path, "r") as file:
        file_content = file.read()
    request_urls, matched_apps = extract_and_map_urls(file_content,applications)
    output_file_path = os.path.join(output_folder, f"{filename}_output.txt")
    with open(output_file_path, "w") as output_file:
        output_file.write("Request URLs:\n")
        for url in request_urls:
            output_file.write(f"{url}\n")
        output_file.write("\nMatched Applications:\n")
        if matched_apps:
            for app_name in matched_apps:
                output_file.write(f"{app_name}\n")
                responses = extract_response_bodies(file_content, app_name)
                output_file.write("\nResponse Conversations:\n")
                for response in responses:
                    output_file.write(f"{response}\n")
        else:
            output_file.write("None\n")

print("Processing complete. Check the output folder for results.")
