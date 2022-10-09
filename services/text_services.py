def text_contains_any_word(text, words):
    """ works in any case"""
    for word in words:
        return word.lower() in text.lower()
    return False
