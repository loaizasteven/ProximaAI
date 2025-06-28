from jinja2 import Template
from pathlib import Path
import os

class PromptTemplates:
    _template_dir = Path(__file__).parent / 'templates'
    _general_agent_template_name = "GENERAL_AGENT"
    _templates = {}

    if not _template_dir.exists():
        raise FileNotFoundError(f"Template directory '{_template_dir}' not found")

    for filename in os.listdir(_template_dir):
        if filename.endswith('.j2'):
            template_name = os.path.splitext(filename)[0]
            try:
                with open(os.path.join(_template_dir, filename), 'r') as f:
                    _templates[template_name] = Template(f.read())
            except Exception as e:
                print(f"Error loading template '{filename}': {e}")

    def __new__(cls, template_name: str, **kwargs):
        try:
            general_agent_prompt = cls._templates[cls._general_agent_template_name].render()
            return cls._templates[template_name].render(**kwargs, general_agent_prompt=general_agent_prompt).strip()
        except KeyError:
            return f"Template {template_name} not found"


if __name__ == "__main__":
    # Example usage:
    print(PromptTemplates('LEAD_AGENT'))
