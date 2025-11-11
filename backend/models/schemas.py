"""
Pydantic models for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


# Sentiment Analysis Models
class SentimentRequest(BaseModel):
    """Request model for sentiment analysis."""
    text: str = Field(..., min_length=1, description="Text to analyze")


class SentimentBatchRequest(BaseModel):
    """Request model for batch sentiment analysis."""
    texts: List[str] = Field(..., min_items=1, description="List of texts to analyze")


class SentimentResponse(BaseModel):
    """Response model for sentiment analysis."""
    text: str
    sentiment: str
    polarity: float
    subjectivity: float
    confidence: float


class SentimentStatistics(BaseModel):
    """Statistics for sentiment analysis results."""
    total_reviews: int
    positive_count: int
    neutral_count: int
    negative_count: int
    positive_percentage: float
    neutral_percentage: float
    negative_percentage: float
    average_polarity: float
    average_subjectivity: float
    average_confidence: float


# Resume Screening Models
class ResumeRequest(BaseModel):
    """Request model for single resume screening."""
    resume_text: str = Field(..., min_length=1, description="Resume content")
    job_description: str = Field(..., min_length=1, description="Job description")


class ResumeItem(BaseModel):
    """Single resume item for batch processing."""
    id: str = Field(..., description="Unique identifier for the resume")
    text: str = Field(..., min_length=1, description="Resume content")


class ResumeBatchRequest(BaseModel):
    """Request model for batch resume screening."""
    resumes: List[ResumeItem] = Field(..., min_items=1, description="List of resumes")
    job_description: str = Field(..., min_length=1, description="Job description")


class ResumeResponse(BaseModel):
    """Response model for resume screening."""
    match_score: float
    skills_found: List[str]
    skills_count: int
    experience_years: int
    recommendation: str


class ResumeRankingResponse(BaseModel):
    """Response model for ranked resume."""
    resume_id: str
    rank: int
    match_score: float
    skills_found: List[str]
    skills_count: int
    experience_years: int
    recommendation: str


# Fake News Detection Models
class FakeNewsRequest(BaseModel):
    """Request model for fake news detection."""
    text: str = Field(..., min_length=1, description="Article or post text")
    source: Optional[str] = Field(default="", description="Source name (optional)")


class FakeNewsResponse(BaseModel):
    """Response model for fake news detection."""
    text: str
    source: str
    is_fake_news: bool
    fake_news_probability: float
    credibility_score: float
    clickbait_score: float
    hate_score: float
    warnings: List[str]
    details: Dict


# Generic Response Models
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
