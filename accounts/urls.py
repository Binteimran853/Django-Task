from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('sign-up/', views.user_register, name='sign-up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit-profile/', views.EditProfile.as_view(), name='edit-profile'),
]
