import re
import json

def extract_github_response(file_content):
    matches = re.findall(r"Response Body:\s*(.+?)(?:data:\s*{\s*\"type\":\s*\"complete\"|Request URL:)", file_content, re.DOTALL)
    return matches

def parse_response(response_body):
    conversation = []
    matches = re.findall(r"data:\s*({\"type\":\"content\",\"body\":\"(.*?)\"})", response_body)
    for match in matches:
        message = json.loads(match[0])
        conversation.append(message["body"])
    return " ".join(conversation)
