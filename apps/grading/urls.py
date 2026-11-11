from django.urls import path

from . import views

app_name = "grading"

urlpatterns = [
    path("", views.sheet_list, name="list"),
    path("upload/<int:exam_id>/", views.upload_sheet, name="upload"),
    path("result/<int:pk>/", views.result_detail, name="result"),
]
