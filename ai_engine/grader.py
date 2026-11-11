"""Compare student answers to rubrics using an LLM."""
import json

from openai import OpenAI

from .prompts import GRADER_SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from .similarity import answer_similarity


class ExamGrader:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", use_similarity: bool = True):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.use_similarity = use_similarity

    def grade_sheet(self, answer_text: str, questions: list[dict]) -> dict:
        q_block = "\n\n".join(
            f"Q{q['number']} (max {q['max_marks']} marks): {q['text']}\n"
            f"Model answer: {q['answer_key']}\nRubric: {q['rubric'] or 'N/A'}"
            for q in questions
        )
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": GRADER_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": USER_PROMPT_TEMPLATE.format(
                        questions=q_block, answer_text=answer_text
                    ),
                },
            ],
        )
        data = json.loads(response.choices[0].message.content)

        if self.use_similarity:
            keys = {q["number"]: q["answer_key"] for q in questions}
            for item in data.get("results", []):
                try:
                    item["similarity"] = answer_similarity(
                        self.client, item.get("student_answer", ""), keys[item["number"]]
                    )
                except Exception:  # similarity is optional; never fail grading on it
                    item["similarity"] = None
        return data
