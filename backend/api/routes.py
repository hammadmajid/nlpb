"""
FastAPI routes for NLP Business Intelligence API.
"""
from fastapi import APIRouter, HTTPException
from typing import List

from backend.models.schemas import (
    SentimentRequest, SentimentBatchRequest, SentimentResponse, SentimentStatistics,
    ResumeRequest, ResumeBatchRequest, ResumeResponse, ResumeRankingResponse,
    FakeNewsRequest, FakeNewsResponse
)
from backend.services.sentiment_service import SentimentAnalyzer
from backend.services.resume_service import ResumeScreener
from backend.services.fake_news_service import FakeNewsDetector


router = APIRouter()

# Initialize services
sentiment_analyzer = SentimentAnalyzer()
resume_screener = ResumeScreener()
fake_news_detector = FakeNewsDetector()


# Sentiment Analysis Endpoints
@router.post("/sentiment/analyze", response_model=SentimentResponse, tags=["Sentiment Analysis"])
async def analyze_sentiment(request: SentimentRequest):
    """Analyze sentiment of a single text."""
    try:
        result = sentiment_analyzer.analyze_text(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sentiment/batch", response_model=List[SentimentResponse], tags=["Sentiment Analysis"])
async def analyze_sentiment_batch(request: SentimentBatchRequest):
    """Analyze sentiment of multiple texts."""
    try:
        results = sentiment_analyzer.analyze_batch(request.texts)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sentiment/statistics", response_model=SentimentStatistics, tags=["Sentiment Analysis"])
async def get_sentiment_statistics(request: SentimentBatchRequest):
    """Get aggregate statistics from sentiment analysis."""
    try:
        results = sentiment_analyzer.analyze_batch(request.texts)
        stats = sentiment_analyzer.get_statistics(results)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Resume Screening Endpoints
@router.post("/resume/screen", response_model=ResumeResponse, tags=["Resume Screening"])
async def screen_resume(request: ResumeRequest):
    """Screen a single resume against a job description."""
    try:
        result = resume_screener.screen_resume(request.resume_text, request.job_description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resume/rank", response_model=List[ResumeRankingResponse], tags=["Resume Screening"])
async def rank_resumes(request: ResumeBatchRequest):
    """Rank multiple resumes against a job description."""
    try:
        resumes_data = [{"id": r.id, "text": r.text} for r in request.resumes]
        results = resume_screener.rank_resumes(resumes_data, request.job_description)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Fake News Detection Endpoints
@router.post("/fakenews/detect", response_model=FakeNewsResponse, tags=["Fake News Detection"])
async def detect_fake_news(request: FakeNewsRequest):
    """Detect fake news and harmful content in text."""
    try:
        result = fake_news_detector.analyze(request.text, request.source)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
