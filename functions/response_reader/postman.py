import re

def extract_postman_interaction(file_content):
    query_pattern = r'"query":"(.*?)",'
    success_response_pattern = r'"actions":\[\{"name":"REPLY_IN_CHAT","content":"(.*?)"\}'
    failure_response_pattern = r'"result":"failure".*?"message":"(.*?)"'

    query_matches = re.findall(query_pattern, file_content)

    success_response_matches = re.findall(success_response_pattern, file_content)

    failure_response_matches = re.findall(failure_response_pattern, file_content, re.DOTALL)

    interactions = []

    total_interactions = max(len(query_matches), len(success_response_matches), len(failure_response_matches))
    
    for i in range(total_interactions):
        interaction = {}

        if i < len(query_matches):
            interaction['user'] = query_matches[i]
        else:
            interaction['user'] = None

        if i < len(success_response_matches):
            interaction['response'] = success_response_matches[i]
        elif i < len(failure_response_matches):
            interaction['response'] = failure_response_matches[i-len(success_response_matches)]
        else:
            interaction['response'] = None 

        interactions.append(interaction)

    return interactions