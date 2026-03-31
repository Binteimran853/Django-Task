from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),
    path('products-list/<int:fk>', views.products_list, name='products'),
    path('products-detail/<int:pk>/', views.product_detail, name='product_detail'),

]