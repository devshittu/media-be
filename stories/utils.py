import re

def extract_hashtags(text):
    return set(part[1:] for part in re.findall(r"#\w+", text))
