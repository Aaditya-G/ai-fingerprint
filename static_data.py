# static_data.py

applications = {
    "github_copilot": r"githubcopilot",
    "grammarly": r"grammarly",
    "leena": r"leena",
    "microsoft_copilot": r"copilot",
    "multion": r"multion",
    "notion": r"notion",
    "postman": r"postman",
    "slack" : r"slack",
    "jasper" : r"jasper",
}

llm_mapping = {
    "github_copilot": "GPT-3.5",
    "microsoft_copilot": "GPT-3.5",
    "grammarly": "GPT-3.5",
    "leena": "GPT-3.5",
    "multion": "GPT-3.5",
    "notion": "GPT-3.5",
    "postman" : "GPT-4",
    "slack" : "Claude-3.5-sonnet",
    "jasper" : "Claude-3.5-sonnet"
}

risk_ratings = {
    "gpt-3.5": {
        "overall_rating": 47,
        "prompt_injection": 68,
        "jailbreak": 52,
        "bias": 22,
        "hallucination": 49,
        "data_poisoning": 71,
        "data_leakage": 37
    },
    "gpt-4-mini": {
        "overall_rating": 76,
        "prompt_injection": 54,
        "jailbreak": 58,
        "bias": 52,
        "hallucination": 77,
        "data_poisoning": 46,
        "data_leakage": 61
    },
    "gpt-4": {
        "overall_rating": 78,
        "prompt_injection": 72,
        "jailbreak": 64,
        "bias": 27,
        "hallucination": 68,
        "data_poisoning": 59,
        "data_leakage": 57
    },
    "claude-3.5-sonnet": {
        "overall_rating": 52,
        "prompt_injection": 48,
        "jailbreak": 53,
        "bias": 47,
        "hallucination": 51,
        "data_poisoning": 55,
        "data_leakage": 43
    }
}
