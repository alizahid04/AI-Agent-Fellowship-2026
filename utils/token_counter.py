def count_tokens(text):
    """Simple heuristic token counter (approx. 4 chars per token or standard split)."""
    if not text:
        return 0
    # Rough approximation: 1 token ~= 0.75 words
    return int(len(text.split()) / 0.75)