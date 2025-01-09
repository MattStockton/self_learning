def build_subtopics_prompt(topic: str) -> str:
    return (
        f"You are an assistant providing strictly subtopic names for '{topic}'. "
        "Return them as a single comma-separated list."
    )

def build_content_prompt(topic: str, subtopic: str, style: str, age: str,
                         length: str, knowledge_level: str) -> str:
    return (
        "You are an educational content generator. "
        f"Topic: {topic}\n"
        f"Subtopic: {subtopic}\n"
        f"Style: {style}\n"
        f"Target Audience Age: {age}\n"
        f"Knowledge Level: {knowledge_level}\n"
        f"Desired Content Length: {length}\n"
        "Produce a cohesive text explanation. No disclaimers."
    )