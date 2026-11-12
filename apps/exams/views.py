from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExamForm, QuestionForm
from .models import Exam
from apps.grading.models import AnswerSheet


@login_required
def exam_list(request):
    exams = Exam.objects.all()
    if request.user.is_teacher:
        exams = exams.filter(teacher=request.user)
    sheets = AnswerSheet.objects.all()
    if request.user.is_student:
        sheets = sheets.filter(student=request.user)
    elif request.user.is_teacher:
        sheets = sheets.filter(exam__teacher=request.user)
    status_counts = {status: sheets.filter(status=status).count() for status, _ in AnswerSheet.Status.choices}
    total_submissions = max(sheets.count(), 1)
    status_percentages = {
        status: round((count / total_submissions) * 100)
        for status, count in status_counts.items()
    }
    metrics = {
        "exam_count": exams.count(),
        "submission_count": sheets.count(),
        "graded_count": status_counts[AnswerSheet.Status.GRADED],
        "average_score": sheets.filter(status=AnswerSheet.Status.GRADED).aggregate(value=Avg("total_score"))["value"],
    }
    return render(request, "exams/list.html", {"exams": exams, "metrics": metrics, "status_counts": status_counts, "status_percentages": status_percentages})


@login_required
def exam_create(request):
    form = ExamForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        exam = form.save(commit=False)
        exam.teacher = request.user
        exam.save()
        return redirect("exams:detail", pk=exam.pk)
    return render(request, "exams/form.html", {"form": form, "title": "New exam"})


@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, "exams/detail.html", {"exam": exam})


@login_required
def question_add(request, pk):
    exam = get_object_or_404(Exam, pk=pk, teacher=request.user)
    form = QuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        q = form.save(commit=False)
        q.exam = exam
        q.save()
        return redirect("exams:detail", pk=exam.pk)
    return render(request, "exams/form.html", {"form": form, "title": "Add question"})
