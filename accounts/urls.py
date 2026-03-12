from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('edit-profile/', views.EditProfile.as_view(), name='edit-profile'),
]
