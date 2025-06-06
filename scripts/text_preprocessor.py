import re
import spacy

class ReviewPreprocessor:
    def __init__(self):
        # emoji pattern: anything outside basic ASCII or special symbols
        self.emoji_pattern = re.compile(
            "[" 
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Symbols & pictographs
            "\U0001F680-\U0001F6FF"  # Transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # Flags
            "\U00002500-\U00002BEF"  # Chinese, Japanese, Korean
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    def clean_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""

        text = text.lower()
        text = re.sub(r'<.*?>', ' ', text)                 # Remove HTML tags
        text = re.sub(r'http\S+|www.\S+', ' ', text)       # Remove URLs
        text = re.sub(r'\S+@\S+', ' ', text)               # Remove emails
        text = re.sub(r'\d+', ' ', text)                   # Remove numbers
        text = re.sub(r'[^\w\s]', ' ', text)               # Remove punctuation
        text = self.emoji_pattern.sub(r'', text)           # Remove emojis
        text = re.sub(r'\s+', ' ', text)                   # Remove extra spaces

        return text.strip()

    def tokenize_text(self, text: str) -> list:
        doc = self.nlp(text)
        tokens = [
            token.lemma_ for token in doc 
            if not token.is_stop and token.is_alpha and len(token) > 2
        ]
        return tokens
