def run_language_test(transcript: str):

    transcript_lower = transcript.lower()

    foreign_words = [
        "ciao", "bonjour", "hola", "guten tag",
        "hallo", "buenos dias"
    ]

    score = 100

    for word in foreign_words:
        if word in transcript_lower:
            score -= 25

    if score < 0:
        score = 0

    return {
        "score": score,
        "passed": score >= 90
    }