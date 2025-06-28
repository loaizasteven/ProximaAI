"""
ProximaAI Tools - Collection of tools for job search, resume building, and career coaching.
"""

from proximaai.tools.agent_builder import AgentBuilder, AgentSpec
from proximaai.tools.web_search import WebSearchTool, CompanyResearchTool
from proximaai.tools.resume_tools import ResumeParserTool, ResumeOptimizerTool
from proximaai.tools.career_coaching import CareerAdvisorTool, InterviewPreparationTool, SkillDevelopmentTool
from proximaai.tools.job_search import JobSearchTool, JobAnalyzerTool, ApplicationTrackerTool

__all__ = [
    # Agent Building
    "AgentBuilder",
    "AgentSpec",
    
    # Web Search
    "WebSearchTool",
    "CompanyResearchTool",

    # Resume Tools
    "ResumeParserTool",
    "ResumeOptimizerTool",
    
    # Career Coaching
    "CareerAdvisorTool",
    "InterviewPreparationTool",
    "SkillDevelopmentTool",
    
    # Job Search
    "JobSearchTool",
    "JobAnalyzerTool",
    "ApplicationTrackerTool",
] 