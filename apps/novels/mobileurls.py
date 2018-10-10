from django.urls import path
from novels import views


urlpatterns = [
    path('_info/<pinyin>/<slug:bookid>/', views.M_InfoView.as_view(), name="novels_info"),
    path('_content/<slug:chapterid>/', views.M_ContentView.as_view(), name="novels_content"),

    # path('_wapsort/', views.M_WapSortView.as_view(), name="novels_wapsort_index"),
    path('_sortlist/<int:sortid>/', views.M_SortListView.as_view(), name="novels_sortlist"),


    path('_historybookshelf/', views.M_HstoryBookshelfView.as_view(), name="novels_historybookshelf"),
]