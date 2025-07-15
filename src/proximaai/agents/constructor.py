from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field
from typing import Any, Union, Literal, Optional

from proximaai.utils.structured_output import MarkdownResponse
from jinja2 import Template
import markdown
import os
import re

# Load template
template_path = os.path.join(os.path.dirname(__file__), '../prebuilt/templates/RESUME_AGENT.j2')
with open(template_path, 'r') as f:
    template_str = f.read()

import logging
logger = logging.getLogger(__name__)


class TextConstructorAgent(BaseModel):
    template: Union[Template, str] = template_str
    model: BaseChatModel
    model_config: dict = {"arbitrary_types_allowed": True}

    def model_post_init(self, __context: Any, **kwargs):
        # TODO: Pull prompt from MCP Server
        if isinstance(self.template, str):
            self.template = Template(template_str)

    @staticmethod
    def __format_response(value: str) -> str:
        if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

        clean_text = value.replace('\\n', '\n').replace('\\"', '"').replace('\\t', '\t')
        return clean_text

    @staticmethod
    def strip_code_block(text):
        # Remove triple backtick code blocks (with or without language)
        return re.sub(r"^```[a-zA-Z]*\\n|\\n```$", "", text.strip(), flags=re.MULTILINE)

    def invoke(self, method: Literal["format", "convert-html"], markdown_like:str) -> dict:
        if method == "format":
            # Get reasoning from the model with structured output
            rendered_prompt = self.template.render(resume_markdown=markdown_like) #type: ignore
            structured_model = self.model.with_structured_output(MarkdownResponse)
            response = structured_model.invoke(rendered_prompt)
            formatted_md = __format_response(value=response.text) #type: ignore

            return {"formatted_resume_markdown": formatted_md, "current_step": "format_resume_with_template_complete"}
        else:
            logger.info("🎯 Converting markdown to HTML")

            # Format and convert
            formatted_md = self.strip_code_block(markdown_like)
            html = markdown.markdown(formatted_md, extensions=['extra'])
            return {"resume_html": html, "current_step": "markdown_to_html_complete"}
