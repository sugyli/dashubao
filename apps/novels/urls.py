from django.urls import path
from novels import views


urlpatterns = [
    path('_info/<slug:bookid>/', views.InfoView.as_view(), name="novels_info"),
    path('_content/<slug:chapterid>/', views.ContentView.as_view(), name="novels_content"),
    path('_sortlist/<int:sortid>/', views.M_SortListView.as_view(), name="novels_sortlist"),

    path('_historybookshelf/', views.M_HstoryBookshelfView.as_view(), name="novels_historybookshelf"),
]