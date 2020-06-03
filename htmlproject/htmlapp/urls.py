from django.contrib import admin
from django.urls import path,include
from htmlapp import views

urlpatterns = [
    path('',views.RegistrationView.as_view(),name='register'),
    path('home',views.LoginView.as_view(),name='login'),
    path('login',views.handleLogin,name='handleLogin'),
    path('logout',views.handleLogout,name='handleLogout'),
    path('signup',views.handleSignup,name='handleSignup'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    
    
]
