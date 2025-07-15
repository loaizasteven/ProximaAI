from proximaai.utils.structured_output import OrchestratorStateMultiAgent, TailoredResumeWithReasoning

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field
from typing import Any, Optional

import logging
logger = logging.getLogger(__name__)


class DesignerAgent(BaseModel):
    query: HumanMessage | str
    model: BaseChatModel
    system_prompt: Optional[SystemMessage] = None
    model_config: dict = {"arbitrary_types_allowed": True}

    def model_post_init(self, __context: Any, **kwargs):
        # TODO: Pull prompt from MCP Server
        self.system_prompt = SystemMessage(
            content="""
            You are a resume optimization assistant. Your job is to rewrite the user's resume in markdown format, tailored for the target company/job.
            As a resume optimization agent your mission is to ensure the resume fits well to the roles description and requirements, maximize the potential
            for the resume to pass the ATS system and reach the hands of a recruiter.

            Instructions:
            - Preserve all original resume sections and content unless something is truly irrelevant to the target job/company.
            - Tailor or highlight content for the target job/company, but do not remove any section or content unless it is clearly irrelevant.
            - Add new content only if it increases relevance for the target job/company.
            - For each section (e.g., Experience, Education, Skills, etc.), provide a reasoning object describing what was changed, added, or removed, and why.
            - Always include two leading blank line after any header (including bolded section headers) and before any markdown list, to ensure correct markdown rendering.
            - Return a structured output as a JSON object with two fields:
                - tailored_resume_markdown: the tailored resume as a markdown string
                - reasoning: a list of objects, each with section, change, and justification fields, describing the reasoning for each section's changes
            - Example output:
            {{
            "tailored_resume_markdown": "...markdown...",
            "reasoning": [
                {{"section": "Experience", "change": "Rewrote bullet points to emphasize leadership", "justification": "Target job emphasizes leadership."}},
                ...
            ]
            }}
            """
        )

    @staticmethod
    def __format_response(value) -> dict[str, str]:
        if isinstance(value, dict):
            data = value
        elif hasattr(value, 'model_dump'):
            data = value.model_dump()
        else:
            raise TypeError("Unexpected response type")
        
        return data

    def invoke(self) -> dict:
        logger.info("🎯 Tailoring resume markdown for company/job")

        # Instantiate Agent with Structured Output
        structured_model = self.model.with_structured_output(TailoredResumeWithReasoning)
        messages = [
            self.system_prompt,
            self.query,
        ]
        response = structured_model.invoke(messages)
        logger.info("✅ Tailored resume markdown and reasoning generated.")

        data = self.__format_response(response)
        return {
            "tailored_resume_markdown": data["tailored_resume_markdown"], 
            "tailor_reasoning": data["reasoning"]
        }
