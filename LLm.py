import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("Groq_Api_Key")
)


def analyze_website(page_text,links):
    prompt = f"""
You are a QA automation planner.

Analyze ONLY the website information provided below.

Do NOT invent URLs, buttons, pages, forms, or functionality.

Create 5 simple automated QA tests.

Allowed test types:

- content: verify text exists on the page
- link: verify a link exists and its href
- navigation: click an existing link and verify the destination loads

Return ONLY valid JSON.

Use exactly this structure:

{{
    "tests": [
        {{
            "name": "Test name",
            "type": "content | link | navigation",
            "target": "exact text",
            "expected": "expected result",
            "href": "actual href if testing a link"
        }}
    ]
}}

Rules:

1. Use exact information from the website.
2. For link tests, use ONLY hrefs from the LINKS section.
3. For navigation tests, use ONLY links from the LINKS section.
4. Do not invent functionality.
5. Prefer tests that Playwright can automate.
6. Include a mixture of content and link tests when possible.

PAGE TEXT:

{page_text[:12000]}

LINKS:

{json.dumps(links, indent=2)}
"""
   
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    result = response.choices[0].message.content

    try:
      return json.loads(result)
    except json.JSONDecodeError:
      print("AI returned invalid JSON:")
      print(result)
      return None