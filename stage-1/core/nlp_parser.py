import re

def parse_natural_query(query):
    if not query and not isinstance(query, str):
        raise ValueError("Invalid query: must be a non-empty string")
    
    text = query.lower()
    filters = {}

    if "palindrome" in text or "palindromic" in text:
        filters['is_palindrome'] = True
    
    if "single word" in text or "one word" in text:
        filters['word_count'] = 1
    
    return filters
