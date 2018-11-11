"""dashubao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path,include

import xadmin
from novels import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('sugyli_admin/', xadmin.site.urls),
    path('', views.IndexView.as_view(),name="novels_index"),

    path('novels', include(('novels.urls', 'novels'), namespace="novels")),

    path('users/', include(('users.urls', 'users'), namespace="users")),
    path('operation/', include(('operation.urls', 'operation'), namespace="operation")),

    path('search/', include(
            ('search.urls', 'search'), namespace="search")),

    path('book/<int:pid>/<int:bookid>/', views.Old_InfoView.as_view(), name="old_novels_info"),
    path('book/<int:pid>/<int:bookid>/index.html', views.Old_InfoView.as_view()),
    path('book/<int:pid>/<int:bookid>/<int:chapterid>.html', views.Old_ContentView.as_view(), name="old_novels_content"),
    path('favicon.ico', RedirectView.as_view(url=r'static/favicon.ico')),


    path('customadmin/', include(('customadmin.urls', 'customadmin'), namespace="customadmin"))


]


handler404 = 'novels.views.page_not_found'
handler500 = 'novels.views.page_error'