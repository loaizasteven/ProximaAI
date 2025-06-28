"""
Job Search Tools - Tools for finding job opportunities, analyzing postings, and tracking applications.
"""

from typing import Dict, List, Any, Optional
from langchain.tools import BaseTool
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import re


@dataclass
class JobPosting:
    """Represents a job posting."""
    title: str
    company: str
    location: str
    description: str
    requirements: List[str]
    salary_range: Optional[str]
    job_type: str  # full_time, part_time, contract, internship
    remote_option: bool
    application_url: str
    posted_date: str
    source: str


@dataclass
class ApplicationTracker:
    """Tracks job applications."""
    job_id: str
    company: str
    position: str
    applied_date: str
    status: str  # applied, interview, offer, rejected, withdrawn
    follow_up_date: Optional[str]
    notes: str


class JobSearchTool(BaseTool):
    """Tool for searching job opportunities."""
    
    def __init__(self):
        super().__init__(
            name="job_search",
            description="""
            Searches for job opportunities based on criteria like job title, location, 
            company, and requirements.
            
            Input should be JSON with search criteria.
            Returns matching job opportunities.
            """
        )
    
    def _run(self, search_criteria_json: str) -> str:
        """Search for job opportunities."""
        try:
            criteria = json.loads(search_criteria_json)
            job_title = criteria.get("job_title", "")
            location = criteria.get("location", "")
            company = criteria.get("company", "")
            remote_only = criteria.get("remote_only", False)
            experience_level = criteria.get("experience_level", "")
            
            jobs = self._search_jobs(job_title, location, company, remote_only, experience_level)
            return json.dumps(jobs, indent=2)
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON input"
        except Exception as e:
            return f"Error searching jobs: {str(e)}"
    
    def _search_jobs(self, job_title: str, location: str, company: str, 
                    remote_only: bool, experience_level: str) -> List[Dict[str, Any]]:
        """Search for jobs based on criteria."""
        # This is a mock implementation
        # In production, integrate with job board APIs (Indeed, LinkedIn, etc.)
        
        mock_jobs = [
            {
                "title": f"Senior {job_title}",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "description": f"Looking for an experienced {job_title} to join our team.",
                "requirements": ["5+ years experience", "Python", "AWS", "Leadership"],
                "salary_range": "$120,000 - $180,000",
                "job_type": "full_time",
                "remote_option": True,
                "application_url": "https://techcorp.com/careers",
                "posted_date": "2024-01-15",
                "source": "LinkedIn"
            },
            {
                "title": f"{job_title} Developer",
                "company": "Startup Inc",
                "location": "Remote",
                "description": f"Join our fast-growing startup as a {job_title}.",
                "requirements": ["2+ years experience", "JavaScript", "React", "Agile"],
                "salary_range": "$80,000 - $120,000",
                "job_type": "full_time",
                "remote_option": True,
                "application_url": "https://startupinc.com/jobs",
                "posted_date": "2024-01-14",
                "source": "Indeed"
            }
        ]
        
        # Filter based on criteria
        filtered_jobs = []
        for job in mock_jobs:
            if self._matches_criteria(job, job_title, location, company, remote_only, experience_level):
                filtered_jobs.append(job)
        
        return filtered_jobs
    
    def _matches_criteria(self, job: Dict[str, Any], job_title: str, location: str, 
                         company: str, remote_only: bool, experience_level: str) -> bool:
        """Check if job matches search criteria."""
        # Match job title
        if job_title and job_title.lower() not in job["title"].lower():
            return False
        
        # Match location
        if location and location.lower() not in job["location"].lower():
            return False
        
        # Match company
        if company and company.lower() not in job["company"].lower():
            return False
        
        # Match remote preference
        if remote_only and not job["remote_option"]:
            return False
        
        return True


class JobAnalyzerTool(BaseTool):
    """Tool for analyzing job postings and extracting insights."""
    
    def __init__(self):
        super().__init__(
            name="job_analyzer",
            description="""
            Analyzes job postings to extract key information, requirements, and insights.
            Helps understand job requirements and company culture.
            
            Input should be the job posting text or URL.
            Returns structured analysis of the job posting.
            """
        )
    
    def _run(self, job_posting_text: str) -> str:
        """Analyze a job posting."""
        try:
            analysis = self._analyze_job_posting(job_posting_text)
            return json.dumps(analysis, indent=2)
        except Exception as e:
            return f"Error analyzing job posting: {str(e)}"
    
    def _analyze_job_posting(self, text: str) -> Dict[str, Any]:
        """Analyze job posting text and extract insights."""
        analysis = {
            "key_requirements": self._extract_requirements(text),
            "required_skills": self._extract_skills(text),
            "preferred_skills": self._extract_preferred_skills(text),
            "experience_level": self._determine_experience_level(text),
            "salary_indicators": self._extract_salary_info(text),
            "company_culture": self._analyze_company_culture(text),
            "red_flags": self._identify_red_flags(text),
            "green_flags": self._identify_green_flags(text),
            "application_tips": self._generate_application_tips(text)
        }
        
        return analysis
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract key requirements from job posting."""
        requirements = []
        
        # Look for requirement patterns
        requirement_patterns = [
            r'requirements?[:\s]+([^.\n]+)',
            r'must have[:\s]+([^.\n]+)',
            r'required[:\s]+([^.\n]+)',
            r'qualifications?[:\s]+([^.\n]+)'
        ]
        
        for pattern in requirement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            requirements.extend(matches)
        
        return [req.strip() for req in requirements if req.strip()]
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract required skills from job posting."""
        skills = []
        
        # Common technical skills
        tech_skills = [
            "python", "javascript", "java", "react", "angular", "vue", "node.js",
            "sql", "mongodb", "aws", "azure", "docker", "kubernetes", "git",
            "agile", "scrum", "machine learning", "data science", "devops"
        ]
        
        text_lower = text.lower()
        for skill in tech_skills:
            if skill in text_lower:
                skills.append(skill)
        
        return skills
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred/nice-to-have skills."""
        preferred = []
        
        # Look for preferred skill indicators
        preferred_patterns = [
            r'preferred[:\s]+([^.\n]+)',
            r'nice to have[:\s]+([^.\n]+)',
            r'bonus[:\s]+([^.\n]+)',
            r'plus[:\s]+([^.\n]+)'
        ]
        
        for pattern in preferred_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            preferred.extend(matches)
        
        return [pref.strip() for pref in preferred if pref.strip()]
    
    def _determine_experience_level(self, text: str) -> str:
        """Determine the experience level required."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["senior", "lead", "principal", "5+ years", "10+ years"]):
            return "senior"
        elif any(word in text_lower for word in ["mid", "intermediate", "3+ years", "5+ years"]):
            return "mid-level"
        elif any(word in text_lower for word in ["junior", "entry", "0-2 years", "1+ years"]):
            return "junior"
        else:
            return "not specified"
    
    def _extract_salary_info(self, text: str) -> Dict[str, Any]:
        """Extract salary information from job posting."""
        salary_info = {
            "salary_range": None,
            "benefits": [],
            "equity": False,
            "bonus": False
        }
        
        # Look for salary patterns
        salary_patterns = [
            r'\$[\d,]+[\s-]+\$[\d,]+',
            r'\$[\d,]+k[\s-]+\$[\d,]+k',
            r'salary[:\s]+([^.\n]+)',
            r'compensation[:\s]+([^.\n]+)'
        ]
        
        for pattern in salary_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                salary_info["salary_range"] = matches[0]
                break
        
        # Look for benefits
        benefit_keywords = ["health insurance", "dental", "vision", "401k", "pto", "vacation"]
        text_lower = text.lower()
        for benefit in benefit_keywords:
            if benefit in text_lower:
                salary_info["benefits"].append(benefit)
        
        # Check for equity and bonus
        if "equity" in text_lower or "stock options" in text_lower:
            salary_info["equity"] = True
        
        if "bonus" in text_lower or "performance" in text_lower:
            salary_info["bonus"] = True
        
        return salary_info
    
    def _analyze_company_culture(self, text: str) -> Dict[str, Any]:
        """Analyze company culture indicators."""
        culture = {
            "work_style": [],
            "values": [],
            "perks": [],
            "team_size": "not specified"
        }
        
        text_lower = text.lower()
        
        # Work style indicators
        if "remote" in text_lower or "work from home" in text_lower:
            culture["work_style"].append("remote-friendly")
        if "flexible" in text_lower:
            culture["work_style"].append("flexible hours")
        if "collaborative" in text_lower:
            culture["work_style"].append("collaborative")
        
        # Company values
        value_keywords = ["innovation", "diversity", "inclusion", "growth", "learning", "impact"]
        for value in value_keywords:
            if value in text_lower:
                culture["values"].append(value)
        
        # Perks
        perk_keywords = ["gym", "snacks", "coffee", "happy hour", "team events", "conferences"]
        for perk in perk_keywords:
            if perk in text_lower:
                culture["perks"].append(perk)
        
        return culture
    
    def _identify_red_flags(self, text: str) -> List[str]:
        """Identify potential red flags in job posting."""
        red_flags = []
        text_lower = text.lower()
        
        red_flag_indicators = [
            "rockstar", "ninja", "guru", "work hard play hard",
            "unlimited overtime", "startup mentality", "wearing many hats",
            "fast-paced environment", "high pressure", "crunch time"
        ]
        
        for indicator in red_flag_indicators:
            if indicator in text_lower:
                red_flags.append(f"Contains '{indicator}' - may indicate poor work-life balance")
        
        return red_flags
    
    def _identify_green_flags(self, text: str) -> List[str]:
        """Identify positive indicators in job posting."""
        green_flags = []
        text_lower = text.lower()
        
        green_flag_indicators = [
            "work-life balance", "flexible hours", "remote work",
            "professional development", "learning budget", "conference attendance",
            "competitive salary", "health benefits", "401k matching",
            "diversity", "inclusion", "equal opportunity"
        ]
        
        for indicator in green_flag_indicators:
            if indicator in text_lower:
                green_flags.append(f"Promotes '{indicator}'")
        
        return green_flags
    
    def _generate_application_tips(self, text: str) -> List[str]:
        """Generate tips for applying to this job."""
        tips = []
        
        # Analyze requirements and generate tips
        if "portfolio" in text.lower():
            tips.append("Prepare a portfolio showcasing your best work")
        
        if "cover letter" in text.lower():
            tips.append("Write a personalized cover letter addressing the company's needs")
        
        if "technical interview" in text.lower():
            tips.append("Prepare for technical coding challenges and system design questions")
        
        if "culture fit" in text.lower():
            tips.append("Research the company culture and prepare behavioral questions")
        
        tips.append("Tailor your resume to highlight relevant experience and skills")
        tips.append("Prepare thoughtful questions about the role and company")
        
        return tips


class ApplicationTrackerTool(BaseTool):
    """Tool for tracking job applications."""
    
    def __init__(self):
        super().__init__(
            name="application_tracker",
            description="""
            Tracks job applications, interview schedules, and follow-up activities.
            Helps manage the job search process and stay organized.
            
            Input should be JSON with application details or tracking commands.
            Returns application status and tracking information.
            """
        )
        # Store instance variables in a way that doesn't conflict with Pydantic
        self._applications: Dict[str, ApplicationTracker] = {}
        self._application_counter = 0
    
    @property
    def applications(self) -> Dict[str, ApplicationTracker]:
        """Get the applications dictionary."""
        return self._applications
    
    @property
    def application_counter(self) -> int:
        """Get the application counter."""
        return self._application_counter
    
    def _increment_counter(self):
        """Increment the application counter."""
        self._application_counter += 1
    
    def _run(self, input_json: str) -> str:
        """Handle application tracking operations."""
        try:
            data = json.loads(input_json)
            action = data.get("action", "")
            
            if action == "add":
                return self._add_application(data)
            elif action == "update":
                return self._update_application(data)
            elif action == "list":
                return self._list_applications(data)
            elif action == "follow_up":
                return self._schedule_follow_up(data)
            else:
                return "Error: Invalid action. Use 'add', 'update', 'list', or 'follow_up'"
                
        except json.JSONDecodeError:
            return "Error: Invalid JSON input"
        except Exception as e:
            return f"Error tracking application: {str(e)}"
    
    def _add_application(self, data: Dict[str, Any]) -> str:
        """Add a new job application."""
        company = data.get("company", "")
        position = data.get("position", "")
        applied_date = data.get("applied_date", datetime.now().strftime("%Y-%m-%d"))
        
        if not company or not position:
            return "Error: Company and position are required"
        
        self._increment_counter()
        job_id = f"job_{self._application_counter}"
        
        application = ApplicationTracker(
            job_id=job_id,
            company=company,
            position=position,
            applied_date=applied_date,
            status="applied",
            follow_up_date=None,
            notes=data.get("notes", "")
        )
        
        self._applications[job_id] = application
        
        return json.dumps({
            "message": "Application added successfully",
            "job_id": job_id,
            "application": {
                "company": company,
                "position": position,
                "applied_date": applied_date,
                "status": "applied"
            }
        }, indent=2)
    
    def _update_application(self, data: Dict[str, Any]) -> str:
        """Update an existing application."""
        job_id = data.get("job_id", "")
        new_status = data.get("status", "")
        notes = data.get("notes", "")
        
        if job_id not in self._applications:
            return "Error: Application not found"
        
        application = self._applications[job_id]
        
        if new_status:
            application.status = new_status
        
        if notes:
            application.notes = notes
        
        return json.dumps({
            "message": "Application updated successfully",
            "application": {
                "job_id": job_id,
                "company": application.company,
                "position": application.position,
                "status": application.status,
                "notes": application.notes
            }
        }, indent=2)
    
    def _list_applications(self, data: Dict[str, Any]) -> str:
        """List all applications with optional filtering."""
        status_filter = data.get("status", "")
        
        applications = []
        for job_id, app in self._applications.items():
            if not status_filter or app.status == status_filter:
                applications.append({
                    "job_id": job_id,
                    "company": app.company,
                    "position": app.position,
                    "applied_date": app.applied_date,
                    "status": app.status,
                    "follow_up_date": app.follow_up_date,
                    "notes": app.notes
                })
        
        return json.dumps({
            "total_applications": len(applications),
            "applications": applications
        }, indent=2)
    
    def _schedule_follow_up(self, data: Dict[str, Any]) -> str:
        """Schedule a follow-up for an application."""
        job_id = data.get("job_id", "")
        follow_up_date = data.get("follow_up_date", "")
        
        if job_id not in self._applications:
            return "Error: Application not found"
        
        application = self._applications[job_id]
        application.follow_up_date = follow_up_date
        
        return json.dumps({
            "message": "Follow-up scheduled successfully",
            "job_id": job_id,
            "company": application.company,
            "follow_up_date": follow_up_date
        }, indent=2) 