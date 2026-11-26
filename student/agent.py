# pip install google-genai

from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from django.conf import settings

class EvaluationResult(BaseModel):
    score: int = Field(
        description="Score awarded to the student answer"
    )
    remarks: str = Field(
        description="Brief feedback explaining the score"
    )


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def evaluate_answer(problem, student_answer):

    prompt = f"""
You are an expert programming instructor evaluating a student's answer.
Evaluate the student's answer strictly based on the given problem.
PROBLEM:
{problem.description}
MAXIMUM POINTS:
{problem.points}
STUDENT ANSWER:
{student_answer}
Evaluation rules:
1. Give a score between 0 and {problem.points}.
2. Never give more than {problem.points}.
3. Award points based on correctness, completeness and whether the answer
   actually solves the given problem.
4. Do not award full marks for an incomplete or partially correct answer.
5. Consider minor syntax mistakes reasonably if the overall logic is correct.
6. Give concise and useful remarks.
7. Return only the requested structured output.
"""

    response = client.models.generate_content(              # this is the ai content to give a llm(ai modules)
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EvaluationResult,
        ),
    )

    result = response.parsed

    return result