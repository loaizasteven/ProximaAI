"""
Resume Tools - Tools for resume parsing, analysis, and optimization.
"""

from typing import Dict, List, Any, Optional
from langchain.tools import BaseTool
import json
import re
from dataclasses import dataclass


@dataclass
class ResumeSection:
    """Represents a section of a resume."""
    section_type: str
    content: str
    confidence: float


@dataclass
class ResumeAnalysis:
    """Analysis results for a resume."""
    skills: List[str]
    experience_years: int
    education_level: str
    key_achievements: List[str]
    improvement_suggestions: List[str]
    ats_score: float  # Applicant Tracking System compatibility score


class ResumeParserTool(BaseTool):
    """Tool for parsing and extracting information from resumes."""
    
    def __init__(self):
        super().__init__(
            name="resume_parser",
            description="""
            Parses resume text to extract key information including skills, experience, 
            education, and achievements.
            
            Input should be the resume text content.
            Returns structured resume data.
            """
        )
    
    def _run(self, resume_text: str) -> str:
        """Parse resume text and extract structured information."""
        try:
            sections = self._extract_sections(resume_text)
            analysis = self._analyze_resume(sections)
            
            result = {
                "sections": [{"type": s.section_type, "content": s.content} for s in sections],
                "analysis": {
                    "skills": analysis.skills,
                    "experience_years": analysis.experience_years,
                    "education_level": analysis.education_level,
                    "key_achievements": analysis.key_achievements,
                    "ats_score": analysis.ats_score
                }
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error parsing resume: {str(e)}"
    
    def _extract_sections(self, text: str) -> List[ResumeSection]:
        """Extract different sections from resume text."""
        sections = []
        
        # Simple section extraction (in production, use more sophisticated NLP)
        section_patterns = {
            "experience": r"(?i)(experience|work history|employment)",
            "education": r"(?i)(education|academic|degree)",
            "skills": r"(?i)(skills|technical skills|competencies)",
            "summary": r"(?i)(summary|objective|profile)"
        }
        
        lines = text.split('\n')
        current_section = "general"
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line starts a new section
            for section_name, pattern in section_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    if current_content:
                        sections.append(ResumeSection(
                            section_type=current_section,
                            content='\n'.join(current_content),
                            confidence=0.8
                        ))
                    current_section = section_name
                    current_content = [line]
                    break
            else:
                current_content.append(line)
        
        # Add the last section
        if current_content:
            sections.append(ResumeSection(
                section_type=current_section,
                content='\n'.join(current_content),
                confidence=0.8
            ))
        
        return sections
    
    def _analyze_resume(self, sections: List[ResumeSection]) -> ResumeAnalysis:
        """Analyze resume sections and extract insights."""
        # Extract skills
        skills = []
        for section in sections:
            if section.section_type == "skills":
                skills = self._extract_skills(section.content)
        
        # Estimate experience years
        experience_years = self._estimate_experience(sections)
        
        # Determine education level
        education_level = self._determine_education_level(sections)
        
        # Extract achievements
        key_achievements = self._extract_achievements(sections)
        
        # Calculate ATS score
        ats_score = self._calculate_ats_score(sections, skills)
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_suggestions(sections, skills, ats_score)
        
        return ResumeAnalysis(
            skills=skills,
            experience_years=experience_years,
            education_level=education_level,
            key_achievements=key_achievements,
            improvement_suggestions=improvement_suggestions,
            ats_score=ats_score
        )
    
    def _extract_skills(self, content: str) -> List[str]:
        """Extract skills from content."""
        # Common technical skills
        common_skills = [
            "python", "javascript", "java", "react", "node.js", "sql", "aws",
            "docker", "kubernetes", "machine learning", "data analysis",
            "project management", "agile", "scrum", "leadership", "communication"
        ]
        
        found_skills = []
        content_lower = content.lower()
        
        for skill in common_skills:
            if skill in content_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _estimate_experience(self, sections: List[ResumeSection]) -> int:
        """Estimate years of experience from resume."""
        # Simple estimation based on content length and keywords
        total_content = " ".join([s.content for s in sections])
        
        # Look for year patterns
        year_pattern = r'\b(20\d{2}|19\d{2})\b'
        years = re.findall(year_pattern, total_content)
        
        if years:
            years = [int(y) for y in years]
            return max(years) - min(years)
        
        # Fallback: estimate based on content length
        return len(total_content) // 1000  # Rough estimate
    
    def _determine_education_level(self, sections: List[ResumeSection]) -> str:
        """Determine education level from resume."""
        education_content = ""
        for section in sections:
            if section.section_type == "education":
                education_content = section.content.lower()
                break
        
        if "phd" in education_content or "doctorate" in education_content:
            return "PhD"
        elif "master" in education_content:
            return "Master's"
        elif "bachelor" in education_content or "bs" in education_content:
            return "Bachelor's"
        elif "associate" in education_content:
            return "Associate's"
        else:
            return "High School or Other"
    
    def _extract_achievements(self, sections: List[ResumeSection]) -> List[str]:
        """Extract key achievements from resume."""
        achievements = []
        
        for section in sections:
            content = section.content
            # Look for achievement indicators
            achievement_indicators = [
                r'increased.*by.*%',
                r'reduced.*by.*%',
                r'led.*team.*of',
                r'managed.*budget.*of',
                r'achieved.*goal',
                r'improved.*efficiency'
            ]
            
            for pattern in achievement_indicators:
                matches = re.findall(pattern, content, re.IGNORECASE)
                achievements.extend(matches)
        
        return achievements[:5]  # Return top 5 achievements
    
    def _calculate_ats_score(self, sections: List[ResumeSection], skills: List[str]) -> float:
        """Calculate ATS compatibility score."""
        score = 0.0
        
        # Check for clear section headers
        section_headers = [s.section_type for s in sections]
        if "experience" in section_headers:
            score += 0.2
        if "education" in section_headers:
            score += 0.2
        if "skills" in section_headers:
            score += 0.2
        
        # Check for keywords/skills
        score += min(len(skills) * 0.05, 0.3)
        
        # Check for formatting (simple heuristics)
        total_content = " ".join([s.content for s in sections])
        if len(total_content) > 500:  # Sufficient content
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_suggestions(self, sections: List[ResumeSection], skills: List[str], ats_score: float) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        if ats_score < 0.7:
            suggestions.append("Improve ATS compatibility by adding more relevant keywords")
        
        if len(skills) < 5:
            suggestions.append("Add more specific technical skills")
        
        if not any(s.section_type == "summary" for s in sections):
            suggestions.append("Add a professional summary section")
        
        return suggestions


class ResumeOptimizerTool(BaseTool):
    """Tool for optimizing resumes for specific job postings."""
    
    def __init__(self):
        super().__init__(
            name="resume_optimizer",
            description="""
            Optimizes resume content for specific job postings by analyzing job requirements
            and suggesting improvements to increase match rate.
            
            Input should be JSON with 'resume_text' and 'job_description'.
            Returns optimized resume suggestions.
            """
        )
    
    def _run(self, input_json: str) -> str:
        """Optimize resume for a specific job posting."""
        try:
            data = json.loads(input_json)
            resume_text = data.get("resume_text", "")
            job_description = data.get("job_description", "")
            
            if not resume_text or not job_description:
                return "Error: Both resume_text and job_description are required"
            
            optimization = self._optimize_resume(resume_text, job_description)
            return json.dumps(optimization, indent=2)
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON input"
        except Exception as e:
            return f"Error optimizing resume: {str(e)}"
    
    def _optimize_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Optimize resume for job description."""
        # Extract keywords from job description
        job_keywords = self._extract_keywords(job_description)
        
        # Extract keywords from resume
        resume_keywords = self._extract_keywords(resume_text)
        
        # Find missing keywords
        missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
        
        # Calculate match percentage
        match_percentage = len(set(job_keywords) & set(resume_keywords)) / len(job_keywords) * 100
        
        # Generate optimization suggestions
        suggestions = self._generate_optimization_suggestions(missing_keywords, job_description)
        
        return {
            "match_percentage": round(match_percentage, 2),
            "missing_keywords": missing_keywords,
            "suggestions": suggestions,
            "recommended_improvements": self._get_improvement_recommendations(match_percentage)
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Common job-related keywords
        keywords = []
        
        # Technical skills
        tech_keywords = [
            "python", "java", "javascript", "react", "angular", "vue", "node.js",
            "sql", "nosql", "mongodb", "postgresql", "aws", "azure", "gcp",
            "docker", "kubernetes", "git", "agile", "scrum", "kanban"
        ]
        
        # Soft skills
        soft_keywords = [
            "leadership", "communication", "teamwork", "problem solving",
            "analytical", "creative", "organized", "detail-oriented"
        ]
        
        text_lower = text.lower()
        
        for keyword in tech_keywords + soft_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
        
        return keywords
    
    def _generate_optimization_suggestions(self, missing_keywords: List[str], job_description: str) -> List[str]:
        """Generate specific optimization suggestions."""
        suggestions = []
        
        if missing_keywords:
            suggestions.append(f"Add these keywords to your resume: {', '.join(missing_keywords[:5])}")
        
        if "experience" in job_description.lower():
            suggestions.append("Highlight relevant work experience that matches the job requirements")
        
        if "education" in job_description.lower():
            suggestions.append("Ensure your education section is prominently featured")
        
        return suggestions
    
    def _get_improvement_recommendations(self, match_percentage: float) -> List[str]:
        """Get improvement recommendations based on match percentage."""
        if match_percentage >= 80:
            return ["Excellent match! Your resume is well-aligned with the job requirements."]
        elif match_percentage >= 60:
            return ["Good match. Consider adding more relevant keywords and experience."]
        elif match_percentage >= 40:
            return ["Moderate match. Significant improvements needed in keyword alignment and experience relevance."]
        else:
            return ["Low match. Consider if this position is the right fit, or significantly revise your resume."] 