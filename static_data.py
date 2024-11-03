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
        "safety": 72,
        "reliability": 53,
        "bias": 22,
        "robustness": 78
    },
    "gpt-4-mini": {
        "overall_rating": 76,
        "safety": 48,
        "reliability": 74,
        "bias": 52,
        "robustness": 79
    },
    "gpt-4": {
        "overall_rating": 78,
        "safety": 74,
        "reliability": 73,
        "bias": 27,
        "robustness": 76
    },
    "claude-3.5-sonnet": {
        "overall_rating": 52,
        "safety": 49,
        "reliability": 51,
        "bias": 47,
        "robustness": 50
    }
}

