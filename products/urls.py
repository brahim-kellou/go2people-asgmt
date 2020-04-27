from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.indexView, name='index'),
    path('<slug:product_slug>/', views.productView, name='product')
]
