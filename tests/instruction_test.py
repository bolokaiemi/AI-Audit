def run_instruction_test(transcript: str):

    transcript_lower = transcript.lower()

    score = 100

    if "one sentence" in transcript_lower:

        # naive check for long responses
        sentences = transcript.count(".")
        if sentences > 5:
            score -= 40

    return {
        "score": score,
        "passed": score >= 90
    }