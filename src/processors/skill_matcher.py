from typing import List, Dict, Any, Optional
import re

class SkillMatcher:
    """Matches and scores resume skills against required skills."""
    
    def match_skills(self, 
                    resume_text: str, 
                    must_have_skills: List[str], 
                    nice_to_have_skills: Optional[List[str]] = None,
                    industry_experience: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Match skills in resume against required skills.
        
        Args:
            resume_text: Full text of the resume
            must_have_skills: List of required skills
            nice_to_have_skills: List of nice to have skills
            industry_experience: List of required industry experience
            
        Returns:
            Dictionary with match results and scores
        """
        if nice_to_have_skills is None:
            nice_to_have_skills = []
        if industry_experience is None:
            industry_experience = []
            
        # Normalize text
        resume_text = resume_text.lower()
        
        # Match skills
        must_have_matches = []
        must_have_missing = []
        
        for skill in must_have_skills:
            skill_lower = skill.lower()
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', resume_text):
                must_have_matches.append(skill)
            else:
                must_have_missing.append(skill)
                
        nice_to_have_matches = []
        for skill in nice_to_have_skills:
            skill_lower = skill.lower()
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', resume_text):
                nice_to_have_matches.append(skill)
                
        industry_matches = []
        for exp in industry_experience:
            exp_lower = exp.lower()
            if re.search(r'\b' + re.escape(exp_lower) + r'\b', resume_text):
                industry_matches.append(exp)
                
        # Check for education
        has_education = False
        education_patterns = [
            r'\b(bachelor|master|phd|doctorate|degree|diploma|mba)\b',
            r'\buniversity\b',
            r'\bcollege\b'
        ]
        for pattern in education_patterns:
            if re.search(pattern, resume_text):
                has_education = True
                break
                
        # Calculate scores
        must_have_score = 0
        if must_have_skills:  # Avoid division by zero
            must_have_score = (len(must_have_matches) / len(must_have_skills)) * 60
            
        nice_to_have_score = 0
        if nice_to_have_skills:  # Avoid division by zero
            nice_to_have_score = (len(nice_to_have_matches) / len(nice_to_have_skills)) * 20
            
        industry_score = 0
        if industry_experience:  # Avoid division by zero
            industry_score = (len(industry_matches) / len(industry_experience)) * 10
            
        education_score = 10 if has_education else 0
        
        total_score = must_have_score + nice_to_have_score + industry_score + education_score
        
        return {
            'must_have': {
                'matches': must_have_matches,
                'missing': must_have_missing,
                'score': must_have_score
            },
            'nice_to_have': {
                'matches': nice_to_have_matches,
                'score': nice_to_have_score
            },
            'industry': {
                'matches': industry_matches,
                'score': industry_score
            },
            'education': {
                'present': has_education,
                'score': education_score
            },
            'total_score': total_score
        }