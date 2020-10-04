"""yeoboseyo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from yeoboseyo.views import Home, TriggerCreate, TriggerUpdate, \
    switch_status, switch_mail, switch_masto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name="home"),
    path('add', TriggerCreate.as_view(), name='add'),
    path('edit/<int:pk>/', TriggerUpdate.as_view(), name='edit'),
    path('delete/<int:pk>/', TriggerUpdate.as_view(), name='delete'),
    path('switch_status/<int:id>/<int:status>', switch_status, name='switch_status'),
    path('switch_mail/<int:id>/<int:status>', switch_mail, name='switch_mail'),
    path('switch_masto/<int:id>/<int:status>', switch_masto, name='switch_masto'),
]
