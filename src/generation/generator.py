import os
from groq import Groq


class AnswerGenerator:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set."
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model = "openai/gpt-oss-120b"

    def generate(
        self,
        query: str,
        context: str,
    ):

        prompt = f"""
You are an AI codebase investigation assistant.

Answer the user's question using ONLY the provided code context.

Rules:
- Use only information directly supported by the provided code.
- Do not assume framework behavior unless it is explicitly shown in the context.
- Do not invent files, functions, variables, or behavior.
- If something cannot be determined from the context, clearly say that it is not shown.
- Explain the relevant code concisely.
- Reference file paths and line numbers when available.
- Do not reproduce large amounts of code unless necessary.
- Keep the answer technical and easy to understand.

User question:
{query}

Code context:
{context}

Answer:
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content