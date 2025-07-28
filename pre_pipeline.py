import re
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Cleans control characters, invisible Unicode chars, newlines, tabs, and punctuation.
    """
    # Remove control chars and invisible Unicode
    text = re.sub(r'[^\x20-\x7E]', ' ', text)  
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

    # Remove all punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_text(raw_text: str) -> list[str]:
    """
    Clean, tokenize, lemmatize and remove stopwords and punctuation.
    """
    cleaned = clean_text(raw_text)
    doc = nlp(cleaned)

    return [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and token.lemma_.isalpha()
    ]
