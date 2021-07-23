from django.urls import path
from . import views

from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.loginpage, name='login'),
    path('logout/',views.logoutuser, name='logout'),



    path('userpage', views.userpage, name='userpage'),
    path('settings', views.accountsettings, name='settings'),
    path('', views.home, name='dashboard'),
    path('product/',views.product, name='product'),
    path('customer/<str:pk>/',views.customer, name='customer'),

    path('create_order/<str:pk>/',views.create_order, name='create_order'),
    path('update_order/<str:pk>/',views.update_order, name='update_order'),
    path('delete_order/<str:pk>/',views.delete_order, name='delete_order'),

    path('reset_password/', auth_view.PasswordResetView.as_view(template_name='accounte/password_reset.html'), 
    name='reset_password'),


    path('reset_password_sent/', auth_view.PasswordResetDoneView.as_view(template_name='accounte/password_reset_sent.html'), 
    name='password_reset_done'),


    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='accounte/password_reset_form.html'), 
    name='password_reset_confirm'),


    path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='accounte/password_reset_done.html'), 
    name='password_reset_complete'),




]