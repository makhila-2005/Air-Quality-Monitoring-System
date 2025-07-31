# myapp/urls.py
'''from django.urls import path
from .views import predict_view

urlpatterns = [
    path('predict/', predict_view, name='predict'),
]'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_view, name='predict'),
]
