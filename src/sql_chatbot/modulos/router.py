
def is_api_request(question: str) -> bool:
    keywords = ["clima", "tiempo", "temperatura", "weather"]
    return any(keyword in question.lower() for keyword in keywords)
    