from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.exams.models import Exam

from .models import AnswerSheet
from .tasks import grade_answer_sheet


class UploadForm(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ("file",)


@login_required
def upload_sheet(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    form = UploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        sheet = form.save(commit=False)
        sheet.exam = exam
        sheet.student = request.user
        sheet.save()
        grade_answer_sheet.delay(sheet.pk)
        return redirect("grading:result", pk=sheet.pk)
    return render(request, "grading/upload.html", {"form": form, "exam": exam})


@login_required
def result_detail(request, pk):
    sheet = get_object_or_404(AnswerSheet, pk=pk)
    return render(request, "grading/result.html", {"sheet": sheet})


@login_required
def sheet_list(request):
    sheets = AnswerSheet.objects.select_related("exam", "student")
    if request.user.is_student:
        sheets = sheets.filter(student=request.user)
    elif request.user.is_teacher:
        sheets = sheets.filter(exam__teacher=request.user)
    return render(request, "grading/list.html", {"sheets": sheets})
