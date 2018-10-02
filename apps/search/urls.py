from django.urls import path

from search import views

urlpatterns = [
    path('bd_search/', views.M_SearchView.as_view(), name="search_bd_search"),

]