def detect_language(text: str) -> str:
    """
    Detect language based on script + common words
    """
    # Marathi / Hindi (Devanagari)
    if any(char >= '\u0900' and char <= '\u097F' for char in text):
        marathi_keywords = ["आहे", "करा", "शेत", "पिक", "सिंचन", "कसे"]
        if any(word in text for word in marathi_keywords):
            return "marathi"
        return "hindi"

    # Default
    return "english"
