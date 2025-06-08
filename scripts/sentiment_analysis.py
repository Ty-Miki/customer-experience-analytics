from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        # try VADER first
        try:
            self.vader = SentimentIntensityAnalyzer()
        except Exception:
            self.vader = None  # fallback to TextBlob

    def predict(self, text: str) -> tuple:
        if not isinstance(text, str) or not text.strip():
            return ("neutral", 0.0)

        if self.vader:
            scores = self.vader.polarity_scores(text)
            compound = scores["compound"]
            label = (
                "positive" if compound > 0.05 else
                "negative" if compound < -0.05 else
                "neutral"
            )
            return (label, compound)

        else:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            label = (
                "positive" if polarity > 0.05 else
                "negative" if polarity < -0.05 else
                "neutral"
            )
            return (label, polarity)
