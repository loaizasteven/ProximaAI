"""
Career Coaching Tools - Tools for career advice, interview preparation, and skill development.
"""

from typing import Dict, List, Any, Optional
from langchain.tools import BaseTool
import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CareerGoal:
    """Represents a career goal."""
    goal_type: str  # short_term, medium_term, long_term
    description: str
    target_date: str
    progress: float  # 0.0 to 1.0


@dataclass
class SkillGap:
    """Represents a skill gap analysis."""
    skill_name: str
    current_level: str  # beginner, intermediate, advanced, expert
    target_level: str
    importance: str  # low, medium, high, critical
    learning_resources: List[str]


class CareerAdvisorTool(BaseTool):
    """Tool for providing career advice and guidance."""
    
    def __init__(self):
        super().__init__(
            name="career_advisor",
            description="""
            Provides personalized career advice based on user's background, goals, and current situation.
            Offers guidance on career transitions, skill development, and professional growth.
            
            Input should be JSON with user background and specific questions.
            Returns personalized career advice and recommendations.
            """
        )
    
    def _run(self, input_json: str) -> str:
        """Provide career advice based on user input."""
        try:
            data = json.loads(input_json)
            background = data.get("background", "")
            question = data.get("question", "")
            goals = data.get("goals", [])
            
            advice = self._generate_career_advice(background, question, goals)
            return json.dumps(advice, indent=2)
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON input"
        except Exception as e:
            return f"Error providing career advice: {str(e)}"
    
    def _generate_career_advice(self, background: str, question: str, goals: List[str]) -> Dict[str, Any]:
        """Generate personalized career advice."""
        advice = {
            "general_recommendations": [],
            "skill_development": [],
            "career_path_suggestions": [],
            "action_items": [],
            "resources": []
        }
        
        # Analyze background and generate recommendations
        if "entry level" in background.lower() or "junior" in background.lower():
            advice["general_recommendations"].append("Focus on building foundational skills and gaining practical experience")
            advice["skill_development"].append("Consider certifications in your field to demonstrate expertise")
        
        if "mid career" in background.lower() or "senior" in background.lower():
            advice["general_recommendations"].append("Focus on leadership skills and strategic thinking")
            advice["career_path_suggestions"].append("Consider management or specialized technical roles")
        
        if "career change" in background.lower():
            advice["general_recommendations"].append("Leverage transferable skills from your previous experience")
            advice["action_items"].append("Network with professionals in your target industry")
        
        # Add specific advice based on question
        if "salary" in question.lower():
            advice["general_recommendations"].append("Research market rates for your role and experience level")
            advice["action_items"].append("Prepare salary negotiation strategies")
        
        if "promotion" in question.lower():
            advice["general_recommendations"].append("Document your achievements and contributions")
            advice["action_items"].append("Schedule a meeting with your manager to discuss career growth")
        
        if "work life balance" in question.lower():
            advice["general_recommendations"].append("Set clear boundaries and prioritize self-care")
            advice["action_items"].append("Consider flexible work arrangements or remote opportunities")
        
        # Add resources
        advice["resources"] = [
            "LinkedIn Learning courses",
            "Professional networking events",
            "Industry conferences",
            "Mentorship programs",
            "Online communities and forums"
        ]
        
        return advice


class InterviewPreparationTool(BaseTool):
    """Tool for interview preparation and practice."""
    
    def __init__(self):
        super().__init__(
            name="interview_preparer",
            description="""
            Helps prepare for job interviews by providing common questions, best practices,
            and personalized preparation strategies.
            
            Input should be JSON with job role, company, and interview type.
            Returns interview preparation materials and strategies.
            """
        )
    
    def _run(self, input_json: str) -> str:
        """Prepare interview materials and strategies."""
        try:
            data = json.loads(input_json)
            job_role = data.get("job_role", "")
            company = data.get("company", "")
            interview_type = data.get("interview_type", "general")  # phone, technical, behavioral, etc.
            
            preparation = self._prepare_interview_materials(job_role, company, interview_type)
            return json.dumps(preparation, indent=2)
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON input"
        except Exception as e:
            return f"Error preparing interview materials: {str(e)}"
    
    def _prepare_interview_materials(self, job_role: str, company: str, interview_type: str) -> Dict[str, Any]:
        """Prepare comprehensive interview materials."""
        preparation = {
            "common_questions": self._get_common_questions(job_role, interview_type),
            "company_research": self._get_company_research_points(company),
            "preparation_strategies": self._get_preparation_strategies(interview_type),
            "practice_scenarios": self._get_practice_scenarios(job_role),
            "follow_up_questions": self._get_follow_up_questions()
        }
        
        return preparation
    
    def _get_common_questions(self, job_role: str, interview_type: str) -> Dict[str, List[str]]:
        """Get common interview questions by category."""
        questions = {
            "behavioral": [
                "Tell me about a time you faced a difficult challenge at work.",
                "Describe a situation where you had to work with a difficult team member.",
                "Give me an example of when you went above and beyond for a project.",
                "Tell me about a time you failed and what you learned from it.",
                "Describe a situation where you had to make a decision with limited information."
            ],
            "technical": [
                "Walk me through your technical background and experience.",
                "What technologies are you most comfortable with?",
                "Describe a technical problem you solved recently.",
                "How do you stay updated with industry trends?",
                "What's your approach to debugging complex issues?"
            ],
            "general": [
                "Why are you interested in this position?",
                "What are your strengths and weaknesses?",
                "Where do you see yourself in 5 years?",
                "Why should we hire you?",
                "What are your salary expectations?"
            ]
        }
        
        # Add role-specific questions
        if "manager" in job_role.lower() or "lead" in job_role.lower():
            questions["leadership"] = [
                "Tell me about a time you led a team through a difficult project.",
                "How do you handle conflicts within your team?",
                "Describe your management style.",
                "How do you motivate your team members?",
                "What's your approach to delegating tasks?"
            ]
        
        return questions
    
    def _get_company_research_points(self, company: str) -> List[str]:
        """Get points to research about the company."""
        return [
            f"Company mission, vision, and values",
            f"Recent news and developments about {company}",
            f"Company culture and work environment",
            f"Products/services and market position",
            f"Leadership team and organizational structure",
            f"Financial performance and growth trajectory",
            f"Competitors and industry position",
            f"Recent achievements and awards"
        ]
    
    def _get_preparation_strategies(self, interview_type: str) -> List[str]:
        """Get preparation strategies for different interview types."""
        strategies = {
            "phone": [
                "Prepare a quiet, professional environment",
                "Have your resume and notes readily available",
                "Practice speaking clearly and at a good pace",
                "Prepare questions to ask the interviewer"
            ],
            "technical": [
                "Review technical concepts and coding problems",
                "Practice coding on a whiteboard or paper",
                "Prepare to explain your technical decisions",
                "Review your past technical projects"
            ],
            "behavioral": [
                "Prepare STAR method responses",
                "Have specific examples ready for common scenarios",
                "Practice telling your stories concisely",
                "Focus on outcomes and learnings"
            ]
        }
        
        return strategies.get(interview_type, strategies["general"])
    
    def _get_practice_scenarios(self, job_role: str) -> List[Dict[str, str]]:
        """Get practice scenarios for the job role."""
        scenarios = [
            {
                "scenario": "You're asked to explain a complex technical concept to a non-technical stakeholder.",
                "approach": "Use analogies and avoid jargon. Focus on business value and outcomes."
            },
            {
                "scenario": "You discover a critical bug in production code.",
                "approach": "Assess impact, communicate immediately, and work on a fix. Document the process."
            },
            {
                "scenario": "A team member is consistently missing deadlines.",
                "approach": "Have a private conversation, understand the root cause, and offer support."
            }
        ]
        
        return scenarios
    
    def _get_follow_up_questions(self) -> List[str]:
        """Get thoughtful follow-up questions to ask interviewers."""
        return [
            "What does success look like in this role in the first 6 months?",
            "What are the biggest challenges facing the team right now?",
            "How would you describe the company culture?",
            "What opportunities for growth and development are available?",
            "What's the next step in the interview process?",
            "Is there anything about my background that concerns you?"
        ]


class SkillDevelopmentTool(BaseTool):
    """Tool for skill development planning and tracking."""
    
    def __init__(self):
        super().__init__(
            name="skill_developer",
            description="""
            Helps create skill development plans, track progress, and recommend learning resources.
            Analyzes skill gaps and provides personalized learning paths.
            
            Input should be JSON with current skills, target skills, and career goals.
            Returns skill development plan and recommendations.
            """
        )
    
    def _run(self, input_json: str) -> str:
        """Create a skill development plan."""
        try:
            data = json.loads(input_json)
            current_skills = data.get("current_skills", {})
            target_skills = data.get("target_skills", [])
            career_goals = data.get("career_goals", [])
            
            development_plan = self._create_skill_development_plan(
                current_skills, target_skills, career_goals
            )
            return json.dumps(development_plan, indent=2)
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON input"
        except Exception as e:
            return f"Error creating skill development plan: {str(e)}"
    
    def _create_skill_development_plan(self, current_skills: Dict[str, str], 
                                     target_skills: List[str], 
                                     career_goals: List[str]) -> Dict[str, Any]:
        """Create a comprehensive skill development plan."""
        # Analyze skill gaps
        skill_gaps = self._analyze_skill_gaps(current_skills, target_skills)
        
        # Prioritize skills based on career goals
        prioritized_skills = self._prioritize_skills(skill_gaps, career_goals)
        
        # Create learning paths
        learning_paths = self._create_learning_paths(prioritized_skills)
        
        # Generate timeline
        timeline = self._generate_timeline(learning_paths)
        
        return {
            "skill_gaps": [{"skill": gap.skill_name, "current": gap.current_level, 
                           "target": gap.target_level, "importance": gap.importance} 
                          for gap in skill_gaps],
            "prioritized_skills": prioritized_skills,
            "learning_paths": learning_paths,
            "timeline": timeline,
            "resources": self._get_learning_resources(),
            "progress_tracking": self._create_progress_tracking(prioritized_skills)
        }
    
    def _analyze_skill_gaps(self, current_skills: Dict[str, str], 
                           target_skills: List[str]) -> List[SkillGap]:
        """Analyze gaps between current and target skills."""
        skill_gaps = []
        
        for target_skill in target_skills:
            current_level = current_skills.get(target_skill, "beginner")
            target_level = "advanced"  # Default target level
            
            # Determine importance based on skill type
            importance = "medium"
            if target_skill in ["python", "javascript", "leadership", "communication"]:
                importance = "high"
            elif target_skill in ["machine learning", "data science"]:
                importance = "critical"
            
            # Generate learning resources
            learning_resources = self._get_skill_resources(target_skill)
            
            skill_gaps.append(SkillGap(
                skill_name=target_skill,
                current_level=current_level,
                target_level=target_level,
                importance=importance,
                learning_resources=learning_resources
            ))
        
        return skill_gaps
    
    def _prioritize_skills(self, skill_gaps: List[SkillGap], 
                          career_goals: List[str]) -> List[Dict[str, Any]]:
        """Prioritize skills based on career goals and importance."""
        prioritized = []
        
        for gap in skill_gaps:
            priority_score = 0
            
            # Score based on importance
            importance_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
            priority_score += importance_scores.get(gap.importance, 1)
            
            # Score based on career goal alignment
            for goal in career_goals:
                if gap.skill_name.lower() in goal.lower():
                    priority_score += 2
            
            prioritized.append({
                "skill": gap.skill_name,
                "priority_score": priority_score,
                "current_level": gap.current_level,
                "target_level": gap.target_level,
                "importance": gap.importance
            })
        
        # Sort by priority score
        prioritized.sort(key=lambda x: x["priority_score"], reverse=True)
        return prioritized
    
    def _create_learning_paths(self, prioritized_skills: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Create learning paths for prioritized skills."""
        learning_paths = {}
        
        for skill_info in prioritized_skills[:5]:  # Top 5 skills
            skill = skill_info["skill"]
            current = skill_info["current_level"]
            target = skill_info["target_level"]
            
            path = []
            
            if current == "beginner" and target in ["intermediate", "advanced", "expert"]:
                path.extend([
                    "Complete foundational courses",
                    "Practice with small projects",
                    "Join online communities"
                ])
            
            if current in ["beginner", "intermediate"] and target in ["advanced", "expert"]:
                path.extend([
                    "Work on complex projects",
                    "Contribute to open source",
                    "Mentor others"
                ])
            
            if target == "expert":
                path.extend([
                    "Publish technical content",
                    "Speak at conferences",
                    "Lead technical initiatives"
                ])
            
            learning_paths[skill] = path
        
        return learning_paths
    
    def _generate_timeline(self, learning_paths: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Generate a timeline for skill development."""
        timeline = {
            "month_1": [],
            "month_2_3": [],
            "month_4_6": [],
            "month_7_12": []
        }
        
        for skill, path in learning_paths.items():
            if path:
                timeline["month_1"].append(f"Start learning {skill}: {path[0]}")
                if len(path) > 1:
                    timeline["month_2_3"].append(f"Continue {skill}: {path[1]}")
                if len(path) > 2:
                    timeline["month_4_6"].append(f"Advanced {skill}: {path[2]}")
                if len(path) > 3:
                    timeline["month_7_12"].append(f"Expert {skill}: {path[3]}")
        
        return timeline
    
    def _get_learning_resources(self) -> Dict[str, List[str]]:
        """Get learning resources by category."""
        return {
            "online_courses": [
                "Coursera",
                "edX",
                "Udemy",
                "LinkedIn Learning",
                "Pluralsight"
            ],
            "books": [
                "Technical books for your specific skills",
                "Career development books",
                "Industry-specific publications"
            ],
            "communities": [
                "Stack Overflow",
                "Reddit (r/learnprogramming, r/cscareerquestions)",
                "Discord/Slack communities",
                "Meetup groups"
            ],
            "practice_platforms": [
                "LeetCode",
                "HackerRank",
                "CodeWars",
                "GitHub (personal projects)"
            ]
        }
    
    def _get_skill_resources(self, skill: str) -> List[str]:
        """Get specific resources for a skill."""
        resources = {
            "python": ["Python.org tutorials", "Real Python", "Automate the Boring Stuff"],
            "javascript": ["MDN Web Docs", "Eloquent JavaScript", "You Don't Know JS"],
            "leadership": ["The Leadership Challenge", "Dare to Lead", "Leadership courses"],
            "communication": ["Crucial Conversations", "Toastmasters", "Communication workshops"]
        }
        
        return resources.get(skill, ["General online courses", "Books and tutorials", "Practice projects"])
    
    def _create_progress_tracking(self, prioritized_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a progress tracking system."""
        return {
            "tracking_method": "Weekly skill assessments and project milestones",
            "metrics": [
                "Hours spent learning",
                "Projects completed",
                "Certifications earned",
                "Peer feedback scores"
            ],
            "checkpoints": [
                "Monthly progress review",
                "Quarterly skill assessment",
                "Bi-annual career goal alignment"
            ]
        } 