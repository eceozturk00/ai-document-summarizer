import re
from collections import Counter

STOPWORDS = {
    "the","a","an","and","or","but","if","then","else","for","to","of","in","on","at","with",
    "is","are","was","were","be","been","being","it","this","that","these","those","as","by",
    "from","we","you","they","i","he","she","them","his","her","our","their"
}

def split_sentences(text: str):
    text = re.sub(r"\s+", " ", text).strip()
    # Basit cümle bölme
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]

def tokenize(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = [t for t in text.split() if len(t) >= 3 and t not in STOPWORDS and not t.isdigit()]
    return tokens

def summarize_text(text: str, n_sentences: int = 4) -> str:
    sentences = split_sentences(text)
    if not sentences:
        return "No readable text found."

    tokens = tokenize(text)
    if not tokens:
        return "Text is too short to summarize."

    freq = Counter(tokens)

    scores = []
    for s in sentences:
        s_tokens = tokenize(s)
        score = sum(freq.get(w, 0) for w in s_tokens)
        scores.append((score, s))

    top = sorted(scores, key=lambda x: x[0], reverse=True)[:n_sentences]
    # Orijinal sırayı koru (daha doğal görünür)
    top_sentences = [s for _, s in top]
    ordered = [s for s in sentences if s in top_sentences]

    return " ".join(ordered[:n_sentences])
