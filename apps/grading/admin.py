from django.contrib import admin

from .models import AnswerSheet, QuestionResult


class ResultInline(admin.TabularInline):
    model = QuestionResult
    extra = 0


@admin.register(AnswerSheet)
class AnswerSheetAdmin(admin.ModelAdmin):
    list_display = ("exam", "student", "status", "total_score", "uploaded_at")
    inlines = [ResultInline]
