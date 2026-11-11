from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExamForm, QuestionForm
from .models import Exam


@login_required
def exam_list(request):
    exams = Exam.objects.all()
    if request.user.is_teacher:
        exams = exams.filter(teacher=request.user)
    return render(request, "exams/list.html", {"exams": exams})


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
