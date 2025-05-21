import tiktoken

def chunk_text(text: str, max_tokens: int = 300) -> list[str]:
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(enc.encode(" ".join(current))) > max_tokens:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks
