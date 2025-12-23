import os
import json
import jsonschema
from groq import Groq
from dotenv import load_dotenv
from taxonomy import VALID_LEAVES

# Load environment variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "enum": list(VALID_LEAVES) + ["[UNMAPPED]"]
        },
        "reasoning": {"type": "string"}
    },
    "required": ["category", "reasoning"]
}

LLM_PROMPT = """
You are a strict genre classification system.

Rules:
- Choose EXACTLY ONE category from the allowed list.
- If unsure or out-of-domain, return "[UNMAPPED]".
- Do NOT invent categories.

Allowed categories:
{categories}

Story:
{story}

Return JSON only in this format:
{{
  "category": "...",
  "reasoning": "..."
}}
"""

class LLMClassifier:
    def classify(self, blurb: str) -> dict:
        prompt = LLM_PROMPT.format(
            categories=", ".join(VALID_LEAVES),
            story=blurb
        )

        try:
            response = client.chat.completions.create(
                model="llama3-8b-instant",  # ✅ valid model
                messages=[
                    {"role": "system", "content": "You output only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            raw_text = response.choices[0].message.content
            parsed = json.loads(raw_text)
            jsonschema.validate(parsed, SCHEMA)
            return parsed

        except Exception as e:
            # ✅ ABSOLUTE SAFETY NET
            return {
                "category": "[UNMAPPED]",
                "reasoning": f"LLM failure or unavailable model: {str(e)}"
            }

