"""
Fake News and Hate Speech Detection Service.
"""
import re
from typing import Dict, List
from textblob import TextBlob


class FakeNewsDetector:
    """Fake news and hate speech detection system."""
    
    def __init__(self):
        """Initialize the detector."""
        # Suspicious indicators for fake news
        self.clickbait_words = [
            'shocking', 'unbelievable', 'you won\'t believe',
            'secret', 'exposed', 'scandal', 'breaking',
            'leaked', 'urgent', 'alert', 'warning'
        ]
        
        # Hate speech indicators (simplified for MVP)
        self.offensive_patterns = [
            r'\b(hate|stupid|idiot|dumb)\b',
            r'(kill|destroy|eliminate)\s+(all|every)',
        ]
        
        # Credibility indicators
        self.credible_sources = [
            'reuters', 'ap', 'bbc', 'npr', 'pbs',
            'nature', 'science', 'research', 'study', 'university'
        ]
    
    def detect_clickbait(self, text: str) -> Dict[str, any]:
        """
        Detect clickbait patterns in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with clickbait analysis
        """
        text_lower = text.lower()
        found_words = [word for word in self.clickbait_words if word in text_lower]
        
        # Check for excessive punctuation
        exclamation_count = text.count('!')
        question_count = text.count('?')
        caps_ratio = sum(1 for c in text if c.isupper()) / (len(text) + 1)
        
        clickbait_score = (
            len(found_words) * 15 +
            min(exclamation_count * 10, 30) +
            min(caps_ratio * 50, 30)
        )
        
        return {
            "is_clickbait": clickbait_score > 40,
            "clickbait_score": min(round(clickbait_score, 2), 100),
            "clickbait_words": found_words,
            "exclamation_count": exclamation_count,
            "caps_ratio": round(caps_ratio, 3)
        }
    
    def detect_hate_speech(self, text: str) -> Dict[str, any]:
        """
        Detect hate speech patterns in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with hate speech analysis
        """
        text_lower = text.lower()
        
        # Count offensive patterns
        offensive_count = 0
        for pattern in self.offensive_patterns:
            offensive_count += len(re.findall(pattern, text_lower))
        
        # Check sentiment (very negative might indicate hate)
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        hate_score = (
            offensive_count * 40 +
            (max(0, -polarity) * 30)
        )
        
        return {
            "contains_hate_speech": hate_score > 50,
            "hate_score": min(round(hate_score, 2), 100),
            "offensive_patterns_found": offensive_count,
            "sentiment_polarity": round(polarity, 3)
        }
    
    def check_credibility(self, text: str, source: str = "") -> Dict[str, any]:
        """
        Check credibility indicators in text.
        
        Args:
            text: Article text
            source: Source name (optional)
            
        Returns:
            Dictionary with credibility analysis
        """
        text_lower = text.lower()
        source_lower = source.lower()
        
        # Check for credible source mentions
        credible_mentions = sum(1 for s in self.credible_sources if s in text_lower or s in source_lower)
        
        # Check for evidence indicators
        has_citations = bool(re.search(r'\[\d+\]|\(\d{4}\)', text))
        has_quotes = text.count('"') >= 2
        
        # Calculate credibility score
        credibility_score = (
            credible_mentions * 25 +
            (30 if has_citations else 0) +
            (15 if has_quotes else 0) +
            min(len(text) / 50, 30)  # Longer, detailed articles are more credible
        )
        
        return {
            "credible": credibility_score > 50,
            "credibility_score": min(round(credibility_score, 2), 100),
            "credible_sources_mentioned": credible_mentions,
            "has_citations": has_citations,
            "has_quotes": has_quotes
        }
    
    def analyze(self, text: str, source: str = "") -> Dict[str, any]:
        """
        Comprehensive analysis for fake news and harmful content.
        
        Args:
            text: Text to analyze
            source: Source name (optional)
            
        Returns:
            Dictionary with complete analysis
        """
        if not text or not text.strip():
            return {
                "text": text,
                "is_fake_news": False,
                "fake_news_probability": 0.0,
                "warnings": [],
                "credibility_score": 0.0
            }
        
        # Run all detections
        clickbait_result = self.detect_clickbait(text)
        hate_result = self.detect_hate_speech(text)
        credibility_result = self.check_credibility(text, source)
        
        # Compile warnings
        warnings = []
        if clickbait_result['is_clickbait']:
            warnings.append("Contains clickbait patterns")
        if hate_result['contains_hate_speech']:
            warnings.append("Contains potential hate speech")
        if not credibility_result['credible']:
            warnings.append("Low credibility score")
        
        # Calculate overall fake news probability
        fake_news_prob = (
            clickbait_result['clickbait_score'] * 0.3 +
            hate_result['hate_score'] * 0.2 +
            (100 - credibility_result['credibility_score']) * 0.5
        )
        
        return {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "source": source,
            "is_fake_news": fake_news_prob > 60,
            "fake_news_probability": round(fake_news_prob, 2),
            "credibility_score": credibility_result['credibility_score'],
            "clickbait_score": clickbait_result['clickbait_score'],
            "hate_score": hate_result['hate_score'],
            "warnings": warnings,
            "details": {
                "clickbait": clickbait_result,
                "hate_speech": hate_result,
                "credibility": credibility_result
            }
        }
