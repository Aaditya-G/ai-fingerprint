import re

def extract_multion_streaming_response(file_content):
    stream_matches = re.findall(
        r"Request URL:\s*https://multion-vercel-git-main-multion.vercel.app/api/.*?Response Body:\s*(data:.*?data:\s*\[DONE\])",
        file_content, re.DOTALL
    )
    return stream_matches

def parse_streaming_response(response_body):
    conversation = []
    matches = re.findall(r"data:\s*{\s*\"content\":\s*\"(.*?)\"}", response_body)
    for content in matches:
        conversation.append(content)
    return " ".join(conversation)
