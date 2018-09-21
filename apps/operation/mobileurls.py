from django.urls import path

from operation import views

urlpatterns = [

    path('adduserask/<comefrom>/', views.AddUserAsk.as_view(), name="operation_adduserask"),
    path('adduserzan/', views.AddUserZan.as_view(), name="operation_adduserzan"),
    path('adduserfav/', views.AddUserFav.as_view(), name="operation_adduserfav"),
]