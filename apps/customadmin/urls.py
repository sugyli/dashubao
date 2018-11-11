from django.urls import path
from customadmin import views


urlpatterns = [
    path('chapterList/<bookid>/', views.ChapterList.as_view(), name="customadmin_chapterList"),
]