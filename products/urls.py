'''
This module contains urlpatterns of products app.
'''
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('<slug:product_slug>/', views.product_view, name='product')
]
