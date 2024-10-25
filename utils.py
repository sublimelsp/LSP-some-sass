def get_eol(text: str) -> str:
    for i, char in enumerate(text):
        if char == '\r':
            if (i + 1) < len(text) and text[i + 1] == '\n':
                return '\r\n'
            return '\r'
        elif char == '\n':
            return '\n'
    return '\n'
