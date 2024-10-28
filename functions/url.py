import re


def extract_and_map_urls(file_content,applications):
    request_urls = re.findall(r"Request URL:\s*(https?://\S+)", file_content)
    matched_apps = set()
    for url in request_urls:
        for app_name, pattern in applications.items():
            if re.search(pattern, url, re.IGNORECASE):
                matched_apps.add(app_name)
                break
    return request_urls, matched_apps