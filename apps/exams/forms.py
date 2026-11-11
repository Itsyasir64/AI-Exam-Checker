from django import forms

from .models import Exam, Question


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ("title", "subject", "description", "question_paper")


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("number", "text", "max_marks", "answer_key", "rubric")
