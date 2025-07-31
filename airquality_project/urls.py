"""
URL configuration for airquality_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# myproject/urls.py
'''from django.contrib import admin
from django.urls import path, include
from prediction import views 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('prediction.urls')),  # replace 'myapp' with your actual app name
]'''
from django.contrib import admin
from django.urls import path
from prediction import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', views.predict_view, name='predict'),
    path('', views.predict_view, name='home'),  # 👈 This line fixes the 404 on /
]


