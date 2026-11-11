from django.conf import settings
from django.db import models

from apps.exams.models import Exam, Question


class AnswerSheet(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "Processing"
        GRADED = "graded", "Graded"
        FAILED = "failed", "Failed"

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="sheets")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sheets"
    )
    file = models.FileField(upload_to="answer_sheets/")
    extracted_text = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.UPLOADED)
    error = models.TextField(blank=True)
    total_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    overall_feedback = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.student} - {self.exam}"


class QuestionResult(models.Model):
    sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE, related_name="results")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.TextField(blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    feedback = models.TextField(blank=True)
    similarity = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["question__number"]
