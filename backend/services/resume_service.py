"""
Resume Screening Service for HR automation.
"""
import re
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class ResumeScreener:
    """Resume screening and ranking system."""
    
    def __init__(self):
        """Initialize the resume screener."""
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=500,
            ngram_range=(1, 2)
        )
        
        # Common skills to extract
        self.tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'machine learning', 'deep learning', 'nlp', 'ai',
            'fastapi', 'django', 'flask', 'nodejs', 'express',
            'git', 'agile', 'scrum', 'ci/cd', 'devops'
        ]
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            List of identified skills
        """
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.tech_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def extract_experience_years(self, text: str) -> int:
        """
        Extract years of experience from resume.
        
        Args:
            text: Resume text
            
        Returns:
            Estimated years of experience
        """
        # Simple regex patterns for experience
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience'
        ]
        
        years = []
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            years.extend([int(match) for match in matches])
        
        return max(years) if years else 0
    
    def screen_resume(self, resume_text: str, job_description: str) -> Dict[str, any]:
        """
        Screen a single resume against a job description.
        
        Args:
            resume_text: The resume content
            job_description: The job description
            
        Returns:
            Dictionary with screening results
        """
        if not resume_text or not job_description:
            return {
                "match_score": 0.0,
                "skills_found": [],
                "experience_years": 0,
                "recommendation": "reject"
            }
        
        # Calculate similarity score using TF-IDF
        try:
            vectors = self.vectorizer.fit_transform([job_description, resume_text])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            match_score = round(similarity * 100, 2)
        except:
            match_score = 0.0
        
        # Extract skills
        skills_found = self.extract_skills(resume_text)
        
        # Extract experience
        experience_years = self.extract_experience_years(resume_text)
        
        # Make recommendation
        if match_score >= 70 and len(skills_found) >= 5:
            recommendation = "highly_recommended"
        elif match_score >= 50 and len(skills_found) >= 3:
            recommendation = "recommended"
        elif match_score >= 30:
            recommendation = "maybe"
        else:
            recommendation = "reject"
        
        return {
            "match_score": match_score,
            "skills_found": skills_found,
            "skills_count": len(skills_found),
            "experience_years": experience_years,
            "recommendation": recommendation
        }
    
    def rank_resumes(self, resumes: List[Dict[str, str]], job_description: str) -> List[Dict[str, any]]:
        """
        Rank multiple resumes against a job description.
        
        Args:
            resumes: List of dictionaries with 'id' and 'text' keys
            job_description: The job description
            
        Returns:
            List of ranked resumes with scores
        """
        results = []
        
        for resume in resumes:
            resume_id = resume.get('id', 'unknown')
            resume_text = resume.get('text', '')
            
            analysis = self.screen_resume(resume_text, job_description)
            results.append({
                "resume_id": resume_id,
                **analysis
            })
        
        # Sort by match score
        results.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Add rank
        for idx, result in enumerate(results, 1):
            result['rank'] = idx
        
        return results
