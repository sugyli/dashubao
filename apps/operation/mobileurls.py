from django.urls import path

from operation import views

urlpatterns = [
    path('adduserzan/', views.AddUserZan.as_view(), name="operation_adduserzan"),
    path('adduserfav/', views.AddUserFav.as_view(), name="operation_adduserfav"),
    path('user_updatepwd/', views.UserUpdatePwd.as_view(), name="operation_user_updatepwd"),
]