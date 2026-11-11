from django.conf import settings
from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exams"
    )
    question_paper = models.FileField(upload_to="exam_papers/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def total_marks(self):
        return sum(q.max_marks for q in self.questions.all())


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    number = models.PositiveIntegerField()
    text = models.TextField()
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    answer_key = models.TextField(help_text="Model answer used as ground truth")
    rubric = models.TextField(
        blank=True, help_text="Marking criteria, e.g. '2 marks for definition, 3 for example'"
    )

    class Meta:
        ordering = ["number"]
        unique_together = ("exam", "number")

    def __str__(self):
        return f"{self.exam.title} - Q{self.number}"
