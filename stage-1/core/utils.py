import hashlib
from collections import Counter


def analyze_string(value):    
    # Normalize whitespace and case for palindrome checks
    cleaned = ''.join(value.lower().split())

    # SHA-256 hash
    sha256_hash = hashlib.sha256(value.encode('utf-8')).hexdigest()

    # Character Frequency
    freq_map = dict(Counter(value))

    # Build result dictionary
    return {
        # "id": sha256_hash,
        "length": len(value),
        "is_palindrome": cleaned == cleaned[::-1],
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "character_frequency_map": freq_map,
        "sha256_hash": sha256_hash
    }