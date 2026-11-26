"""
pip install langchain
pip install langchain-google-genai
pip install pydantic
"""
# services/ai_evaluator.py

from django.conf import settings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field


# ============================================================
# 1. STRUCTURED OUTPUT MODEL
# ============================================================

class EvaluationResult(BaseModel):

    score: int = Field(
        description="Score awarded to the student answer"
    )

    remarks: str = Field(
        description="Brief feedback explaining the score"
    )


# ============================================================
# 2. GEMINI MODEL
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0
)


# ============================================================
# 3. STRUCTURED OUTPUT
# ============================================================

structured_llm = llm.with_structured_output(
    EvaluationResult
)


# ============================================================
# 4. PROMPT TEMPLATE
# ============================================================

prompt = ChatPromptTemplate.from_template(
    """
You are an expert programming instructor evaluating
a student's answer.
Evaluate the student's answer strictly based on the
given programming problem.
PROBLEM:
{problem}
MAXIMUM POINTS:
{max_points}
STUDENT ANSWER:
{student_answer}
EVALUATION RULES:
1. Give a score between 0 and {max_points}.
2. Never give more than {max_points}.
3. Award points based on:
   - Correctness
   - Completeness
   - Logic
   - Whether the answer actually solves the problem
4. Do not award full marks for an incomplete answer.
5. Consider minor syntax mistakes reasonably if the
   overall programming logic is correct.
6. Give concise and useful remarks.
7. Return only the requested structured output.
"""
)


# ============================================================
# 5. CREATE LANGCHAIN CHAIN
# ============================================================

evaluation_chain = prompt | structured_llm


# ============================================================
# 6. EVALUATE STUDENT ANSWER
# ============================================================

def evaluate_answer(problem, student_answer):

    result = evaluation_chain.invoke(
        {
            "problem": problem.description,
            "max_points": problem.points,
            "student_answer": student_answer,
        }
    )

    # ========================================================
    # SAFETY VALIDATION
    # ========================================================

    score = result.score

    # Score cannot be less than 0
    if score < 0:
        score = 0

    # Score cannot exceed problem points
    if score > problem.points:
        score = problem.points

    # ========================================================
    # RETURN STRUCTURED RESULT
    # ========================================================

    return EvaluationResult(
        score=score,
        remarks=result.remarks
    )