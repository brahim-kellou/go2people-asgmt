from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.indexView, name='index'),
    path('<int:product_id>/', views.productView, name='product')
]
