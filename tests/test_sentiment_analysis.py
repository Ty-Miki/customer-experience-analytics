import pytest
from scripts.sentiment_analysis import SentimentAnalyzer

def test_predict_with_vader_positive(monkeypatch):
    analyzer = SentimentAnalyzer()
    # Mock VADER's polarity_scores
    class MockVader:
        def polarity_scores(self, text):
            return {"compound": 0.8}
    analyzer.vader = MockVader()
    label, score = analyzer.predict("Great app!")
    assert label == "positive"
    assert score == 0.8

def test_predict_with_vader_negative(monkeypatch):
    analyzer = SentimentAnalyzer()
    class MockVader:
        def polarity_scores(self, text):
            return {"compound": -0.7}
    analyzer.vader = MockVader()
    label, score = analyzer.predict("Terrible experience.")
    assert label == "negative"
    assert score == -0.7

def test_predict_with_vader_neutral(monkeypatch):
    analyzer = SentimentAnalyzer()
    class MockVader:
        def polarity_scores(self, text):
            return {"compound": 0.0}
    analyzer.vader = MockVader()
    label, score = analyzer.predict("It is an app.")
    assert label == "neutral"
    assert score == 0.0

def test_predict_with_textblob(monkeypatch):
    analyzer = SentimentAnalyzer()
    analyzer.vader = None  # Force fallback to TextBlob

    class MockBlob:
        class Sentiment:
            polarity = 0.6
        @property
        def sentiment(self):
            return self.Sentiment()
    monkeypatch.setattr("scripts.sentiment_analysis.TextBlob", lambda text: MockBlob())

    label, score = analyzer.predict("Nice!")
    assert label == "positive"
    assert score == 0.6

def test_predict_empty_and_non_string(monkeypatch):
    analyzer = SentimentAnalyzer()
    assert analyzer.predict("") == ("neutral", 0.0)
    assert analyzer.predict(None) == ("neutral", 0.0)
    assert analyzer.predict(123) == ("neutral", 0.0)