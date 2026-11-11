from celery import shared_task
from django.conf import settings

from ai_engine.grader import ExamGrader
from ai_engine.ocr_processor import extract_text

from .models import AnswerSheet, QuestionResult


@shared_task(bind=True, max_retries=2)
def grade_answer_sheet(self, sheet_id: int):
    sheet = AnswerSheet.objects.select_related("exam").get(pk=sheet_id)
    sheet.status = AnswerSheet.Status.PROCESSING
    sheet.save(update_fields=["status"])

    try:
        sheet.extracted_text = extract_text(sheet.file.path)
        questions = list(sheet.exam.questions.all())

        grader = ExamGrader(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_MODEL)
        graded = grader.grade_sheet(
            sheet.extracted_text,
            [
                {
                    "number": q.number,
                    "text": q.text,
                    "max_marks": float(q.max_marks),
                    "answer_key": q.answer_key,
                    "rubric": q.rubric,
                }
                for q in questions
            ],
        )

        sheet.results.all().delete()
        by_number = {q.number: q for q in questions}
        total = 0
        for item in graded["results"]:
            q = by_number.get(item["number"])
            if not q:
                continue
            score = min(float(item["score"]), float(q.max_marks))
            total += score
            QuestionResult.objects.create(
                sheet=sheet,
                question=q,
                student_answer=item.get("student_answer", ""),
                score=score,
                feedback=item.get("feedback", ""),
                similarity=item.get("similarity"),
            )

        sheet.total_score = total
        sheet.overall_feedback = graded.get("overall_feedback", "")
        sheet.status = AnswerSheet.Status.GRADED
        sheet.error = ""
    except Exception as exc:  # noqa: BLE001
        sheet.status = AnswerSheet.Status.FAILED
        sheet.error = str(exc)
        sheet.save()
        raise self.retry(exc=exc, countdown=30)

    sheet.save()
    return sheet.pk
