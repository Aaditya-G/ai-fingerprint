import re 

def extract_pseudo_interaction(file_content):

    user_pattern = r'Request Body: user : "conversation" : "(.*?)"'
    response_pattern = r'Response Body : "conversation" : "data" : "(.*?)"'

    user_matches = re.findall(user_pattern, file_content)
    response_matches = re.findall(response_pattern, file_content)

    interactions = []

    total_interactions = max(len(user_matches), len(response_matches))
    
    for i in range(total_interactions):
        interaction = {}

        if i < len(user_matches):
            interaction['user'] = user_matches[i]
        else:
            interaction['user'] = None

        if i < len(response_matches):
            interaction['response'] = response_matches[i]
        else:
            interaction['response'] = None 

        interactions.append(interaction)

    return interactions