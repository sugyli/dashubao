from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="users_login"),
    path('register/', views.RegisterView.as_view(), name="users_register"),
    path('forget/', views.ForgetPwdView.as_view(), name="users_forget"),

    path('home/', views.M_UserindexView.as_view(), name="users_home"),

]