# static_data.py

applications = {
    "github_copilot": r"githubcopilot",
    "leena": r"leena",
    "microsoft_copilot": r"copilot",
    "multion": r"multion",
    "notion": r"notion",
    "postman": r"postman",
    "slack": r"slack",
    "jasper": r"jasper",
}

llm_mapping = {
    "github_copilot": "GPT-3.5",
    "microsoft_copilot": "GPT-3.5",
    "leena": "GPT-3.5",
    "multion": "GPT-3.5",
    "notion": "GPT-3.5",
    "postman": "GPT-4",
    "slack": "Claude-3.5-sonnet",
    "jasper": "Claude-3.5-sonnet",
}

risk_ratings = {
    "gpt-3.5": {
        "overall_rating": 77,
        "prompt_injection": 68,
        "jailbreak": 55,
        "bias": 23,
        "hallucination": 49,
        "data_poisoning": 71,
        "data_leakage": 29,
    },
    "gpt-4-mini": {
        "overall_rating": 63,
        "prompt_injection": 54,
        "jailbreak": 45,
        "bias": 31,
        "hallucination": 61,
        "data_poisoning": 46,
        "data_leakage": 34,
    },
    "gpt-4": {
        "overall_rating": 34,
        "prompt_injection": 29,
        "jailbreak": 38,
        "bias": 15,
        "hallucination": 47,
        "data_poisoning": 32,
        "data_leakage": 28,
    },
    "claude-3.5-sonnet": {
        "overall_rating": 26,
        "prompt_injection": 29,
        "jailbreak": 25,
        "bias": 16,
        "hallucination": 33,
        "data_poisoning": 22,
        "data_leakage": 18,
    },
}
