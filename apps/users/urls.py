from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="users_login"),
    path('register/', views.RegisterView.as_view(), name="users_register"),
    path('forget/', views.ForgetPwdView.as_view(), name="users_forget"),
    path('logout/', views.LogoutView.as_view(), name="users_logout"),


    path('reset/<active_code>/', views.ResetView.as_view(), name="users_reset"),
    path('modifypwd/', views.ModifyPwdView.as_view(), name="users_modifypwd"),

    path('home/', views.M_UserindexView.as_view(), name="users_home"),
    path('info/', views.M_UserinfoView.as_view(), name="users_info"),
    path('updatepwd/', views.M_UpdatePwdView.as_view(), name="users_updatepwd"),

    path('qiandao/', views.M_QandaoView.as_view(), name="users_qiandao"),
    path('adduserask/<comefrom>/', views.M_AddUserAskView.as_view(), name="users_adduserask"),


    path('message/', views.M_MessageView.as_view(), name="users_message"),
    path('gonggao/', views.M_GonggaoView.as_view(), name="users_gonggao"),


    path('ask/', views.M_AskView.as_view(), name="users_ask"),
    path('favbook/', views.M_FavBookView.as_view(), name="users_favbook"),

    path('touxian/', views.M_TouxianView.as_view(), name="users_touxian"),
]