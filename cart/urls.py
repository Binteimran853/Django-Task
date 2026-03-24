from django.urls import path

from . import views


urlpatterns = [
    path('cart/', views.user_cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_cart, name='add_cart'),
    path('update_cart/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
]

