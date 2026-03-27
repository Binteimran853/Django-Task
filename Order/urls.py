from django.urls import path

from . import views


urlpatterns = [

    path('check-out/<int:cart_id>/', views.check_out, name='check_out'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]