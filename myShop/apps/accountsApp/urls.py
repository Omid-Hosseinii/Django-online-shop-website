from django.urls import path
from .views import *
#----------------------------------------------------------------

app_name='accounts'

urlpatterns =[
    path('register',RegisterUserView.as_view(),name='register'),
    path('verify',VerifyRegisterViews.as_view(),name='verify'),
    path('login/',LoginUserView.as_view(),name='login'),
    path('logout',LogoutUserView.as_view(),name='logout'),
    path('user_panel',UserPanelView.as_view(),name='user_panel'),
    path('remember_password',RememberPasswordView.as_view(),name='remember_password'),
    path('change_password',ChangePasswordView.as_view(),name='change_password'),
    path('user_panel_last_order',user_panel_last_order,name='user_panel_last_order'),
    path('user_panel_update',UserPanelUpdateView.as_view(),name='user_panel_update'),
    path('user_panel_payment',peyment_history,name='user_panel_payment'),
    path('change_password_up',ChangePasswordUserPanelView.as_view(),name='change_password_up'),
]

