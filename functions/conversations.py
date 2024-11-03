from functions.response_reader.github_copilot import extract_github_response, parse_response
from functions.response_reader.multion import extract_multion_streaming_response, parse_streaming_response
from functions.response_reader.postman import extract_postman_interaction
from functions.response_reader.pseudo import extract_pseudo_interaction

def extract_response_bodies(file_content, app_name):
    if app_name == "github_copilot":
        response_sections = extract_github_response(file_content)
        parsed_responses = [parse_response(section) for section in response_sections]
        return parsed_responses
    elif app_name == "multion":
        response_sections = extract_multion_streaming_response(file_content)
        parsed_responses = [parse_streaming_response(section) for section in response_sections]
        return parsed_responses
    elif app_name == "postman":
        parsed_responses = extract_postman_interaction(file_content)
        return parsed_responses
    elif app_name == "slack" or app_name == "jasper" :
        parsed_responses = extract_pseudo_interaction(file_content)
        return parsed_responses
    return "please try again after sometime"