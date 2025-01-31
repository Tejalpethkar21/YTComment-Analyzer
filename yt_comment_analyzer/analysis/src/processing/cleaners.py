import re
import emoji

def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')

def clean_text(text):
    text = remove_emojis(text)
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    return text.strip()