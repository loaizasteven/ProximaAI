from jinja2 import Template
from pathlib import Path
import os

class PromptTemplates:
    _template_dir = Path(__file__).parent / 'templates'
    _templates = {}
        
    """Load all templates from the templates directory"""
    for filename in os.listdir(_template_dir):
        if filename.endswith('.j2'):
            template_name = os.path.splitext(filename)[0]
            with open(os.path.join(_template_dir, filename), 'r') as f:
                _templates[template_name] = Template(f.read())

    def __new__(cls, template_name: str, **kwargs):
        """Render the template with the given kwargs for jinja2"""
        general_agent_prompt = cls._templates["GENERAL_AGENT"].render()
        try:
            return cls._templates[template_name].render(**kwargs, general_agent_prompt=general_agent_prompt).strip()
        except KeyError:
            return f"Template {template_name} not found"

# Example usage:
print(PromptTemplates('LEAD_AGENT'))
