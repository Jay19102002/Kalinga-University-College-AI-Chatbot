import re

def normalize_text(text: str) -> str:
    """Normalize user input text for NLP intent classification."""
    if not text:
        return ""
    
    # Lowercase
    text = text.lower().strip()
    
    # Standardize common acronyms / course variations
    text = re.sub(r'\bb\.tech\b', 'btech', text)
    text = re.sub(r'\bb\.com\b', 'bcom', text)
    text = re.sub(r'\bb\.sc\b', 'bsc', text)
    text = re.sub(r'\bm\.sc\b', 'msc', text)
    text = re.sub(r'\bb\.pharm\b', 'bpharm', text)
    text = re.sub(r'\bd\.pharm\b', 'dpharm', text)
    text = re.sub(r'\bpharm\.d\b', 'pharmd', text)
    text = re.sub(r'\bb\.ed\b', 'bed', text)
    text = re.sub(r'\bm\.ed\b', 'med', text)
    text = re.sub(r'\bph\.d\b|\bphd\b', 'phd', text)
    text = re.sub(r'\bll\.b\b|\bllb\b', 'llb', text)
    text = re.sub(r'\bll\.m\b|\bllm\b', 'llm', text)
    text = re.sub(r'\bkal-mat\b|\bkalmat\b', 'kalmat', text)
    text = re.sub(r'\bkalsee\b', 'kalsee', text)
    
    # Remove punctuation except hyphen/percent where relevant
    text = re.sub(r'[^\w\s\-\%]', ' ', text)
    
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
