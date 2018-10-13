
from django.urls import path,include

from novels import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.M_IndexView.as_view(),name="novels_index"),

    path('novels', include(
        ('novels.mobileurls', 'novels'), namespace="novels")),

    path('users/', include(
        ('users.mobileurls', 'users'), namespace="users")),

    path('operation/', include(
        ('operation.mobileurls', 'operation'), namespace="operation")),

    path('search/', include(
        ('search.mobileurls', 'search'), namespace="search")),

    path('info-<int:bookid>/', views.Old_M_InfoView.as_view(), name="old_novels_info"),
    path('wapbook-<int:bookid>-<int:chapterid>/', views.Old_M_ContentView.as_view(), name="old_novels_content"),
    path('favicon.ico', RedirectView.as_view(url=r'static/favicon.ico'))
]


handler404 = 'novels.views.page_not_found'
handler500 = 'novels.views.page_error'