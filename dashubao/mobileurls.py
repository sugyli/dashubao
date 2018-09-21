
from django.urls import path
from django.urls import include

from novels import views


urlpatterns = [
    path('', views.M_IndexView.as_view(),name="novels_index"),

    path('novel', include(
        ('novels.mobileurls', 'novels'), namespace="novels")),

    path('users/', include(
        ('users.mobileurls', 'users'), namespace="users")),

    path('operation/', include(
        ('operation.mobileurls', 'operation'), namespace="operation")),


    path('info-<int:bookid>/', views.M_InfoView.as_view(), name="novels_info"),
    path('wapbook-<int:bookid>-<int:chapterid>/', views.M_ContentView.as_view(), name="novels_content")
]
