"""
Sentiment Analysis Service for customer reviews and feedback.
"""
from textblob import TextBlob
from typing import Dict, List
import pandas as pd


class SentimentAnalyzer:
    """Sentiment analysis using TextBlob for MVP."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        self.sentiment_labels = {
            "positive": (0.1, 1.0),
            "neutral": (-0.1, 0.1),
            "negative": (-1.0, -0.1)
        }
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of a single text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment results
        """
        if not text or not text.strip():
            return {
                "text": text,
                "sentiment": "neutral",
                "polarity": 0.0,
                "subjectivity": 0.0,
                "confidence": 0.0
            }
        
        # Analyze using TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Calculate confidence (using absolute polarity as proxy)
        confidence = abs(polarity)
        
        return {
            "text": text,
            "sentiment": sentiment,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "confidence": round(confidence, 3)
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, any]]:
        """
        Analyze sentiment of multiple texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment analysis results
        """
        return [self.analyze_text(text) for text in texts]
    
    def get_statistics(self, results: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Calculate statistics from sentiment analysis results.
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            Dictionary with aggregate statistics
        """
        if not results:
            return {
                "total_reviews": 0,
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0,
                "average_polarity": 0.0,
                "average_subjectivity": 0.0
            }
        
        df = pd.DataFrame(results)
        
        return {
            "total_reviews": len(results),
            "positive_count": int((df["sentiment"] == "positive").sum()),
            "neutral_count": int((df["sentiment"] == "neutral").sum()),
            "negative_count": int((df["sentiment"] == "negative").sum()),
            "positive_percentage": round((df["sentiment"] == "positive").mean() * 100, 2),
            "neutral_percentage": round((df["sentiment"] == "neutral").mean() * 100, 2),
            "negative_percentage": round((df["sentiment"] == "negative").mean() * 100, 2),
            "average_polarity": round(df["polarity"].mean(), 3),
            "average_subjectivity": round(df["subjectivity"].mean(), 3),
            "average_confidence": round(df["confidence"].mean(), 3)
        }
