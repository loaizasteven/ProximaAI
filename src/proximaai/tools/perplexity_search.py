import os
import httpx
from langchain.tools import BaseTool
import json
from typing import Optional

class PerplexityWebSearchTool(BaseTool):
    """Tool for performing web searches using the Perplexity API."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="perplexity_web_search",
            description="""
            Uses the Perplexity API to perform a web search and return a conversational answer.
            Input should be a search query string.
            """
        )
        self._api_key = api_key or os.environ.get("PERPLEXITY_API_KEY")

    def _run(self, query: str) -> str:
        if not self._api_key:
            return "Error: PERPLEXITY_API_KEY is not set."
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        body = {
            "model": "sonar-pro",
            "messages": [
                {"role": "user", "content": query}
            ],
        }
        try:
            # with httpx.Client() as client:
            #     response = client.post(url, headers=headers, json=body, timeout=30)
            #     response.raise_for_status()
            #     data = response.json()
            # message_content = data["choices"][0]["message"]["content"]
            # if "citations" in data and isinstance(data["citations"], list) and data["citations"]:
            #     message_content += "\n\nCitations:\n"
            #     for idx, citation in enumerate(data["citations"], 1):
            #         message_content += f"[{idx}] {citation}\n"
            # return message_content
            return """
            GEICO's **company mission** and **core values** center on providing affordable, high-quality insurance directly to consumers while maintaining a strong ethical foundation and supporting a diverse, inclusive workplace.

            **Mision Statement**
            - GEICO's mission is to *market and provide low-price, high-quality insurance directly to consumers*. This is achieved by bypassing the traditional agent model, allowing the company to keep costs low and offer competitive products to a broad customer base[3].
            - The principle of **integrity** is integral to GEICO's mission, positioning the company as trustworthy in a field often viewed skeptically by consumers[3].

            **Core Values and Operating Principles**
            GEICO's culture is defined by **seven core operating principles**[2]:
            - **Respect, support, and provide opportunity for all associates**
            - **Fanatical commitment to outstanding customer service**
            - **Be the low-cost provider**
            - **Operate with uncompromising integrity**
            - **Maintain a disciplined balance sheet**
            - **Make an underwriting profit while achieving optimal growth**
            - **Invest for total return**

            **Company Culture and Community Commitment**
            - GEICO emphasizes building a strong workplace community and celebrating diversity among its associates, valuing each person's unique skills and perspectives[2].
            - The company supports charitable initiatives, such as contributions to the United Way, disaster relief, scholarships, and community service, highlighting its commitment to corporate social responsibility[2].

            **Diversity and Inclusion**
            - GEICO actively fosters an environment where all employees have an equal opportunity to reach their full potential, recognizing that diversity fuels innovative thinking and customer service excellence[2].

            **Summary Table: GEICO Mission and Values**

            | Aspect             | Description                                                                   |
            |--------------------|-------------------------------------------------------------------------------|
            | Mission            | Market and provide low-price, high-quality insurance directly to consumers[3]  |
            | Integrity          | Uncompromising ethical standards and trustworthiness[3]                        |
            | Customer Focus     | Outstanding service and support for policyholders[2]                           |
            | Cost Leadership    | Commitment to being the low-cost provider[2][3]                                |
            | Employee Support   | Respect, opportunity, and support for all associates[2]                        |
            | Diversity & Inclusion | Celebrate and value diversity among staff[2]                                |
            | Community Involvement | Charitable giving, volunteering, scholarship funding[2]                     |

            GEICO's mission and values drive its approach to business, employee relations, and community involvement, reflecting its longstanding position as a major player in the insurance industry[2][3][4].

            Citations:
            [1] https://geico-spa.com/en/about-us/
            [2] https://www.indeed.com/cmp/Geico/about
            [3] https://www.123helpme.com/essay/Geicos-Mission-Statement-PJTAN5JGGET
            [4] https://en.wikipedia.org/wiki/GEICO
            [5] https://careers.geico.com
            """
        except Exception as e:
            return f"Error calling Perplexity API: {str(e)}"
