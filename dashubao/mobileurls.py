
from django.urls import path,include

from novels import views


urlpatterns = [
    path('', views.M_IndexView.as_view(),name="novels_index"),

    path('novel', include(
        ('novels.mobileurls', 'novels'), namespace="novels")),

    path('users/', include(
        ('users.mobileurls', 'users'), namespace="users")),

    path('operation/', include(
        ('operation.mobileurls', 'operation'), namespace="operation")),

    path('search/', include(
        ('search.mobileurls', 'search'), namespace="search")),

    path('info-<int:bookid>/', views.Old_M_InfoView.as_view(), name="old_novels_info"),
    path('wapbook-<int:bookid>-<int:chapterid>/', views.Old_M_ContentView.as_view(), name="old_novels_content")
]
