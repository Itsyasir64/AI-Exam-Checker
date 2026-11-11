from django.urls import path

from . import views

app_name = "exams"

urlpatterns = [
    path("", views.exam_list, name="list"),
    path("new/", views.exam_create, name="create"),
    path("<int:pk>/", views.exam_detail, name="detail"),
    path("<int:pk>/questions/add/", views.question_add, name="question_add"),
]
