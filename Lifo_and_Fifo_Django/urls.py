"""Lifo_and_Fifo_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
import donation.views

app_name = 'donation'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', donation.views.home_page, name='main'),
    path('request/donate', donation.views.described_item),
    path('request/donate_amount', donation.views.request),
    path('request/donation', donation.views.donation),
    path('list', donation.views.list, name='list'),
    path('set_office', donation.views.session_office, name='set_session_office'),
    path('request/number', donation.views.request),
    path('request/correct_request', donation.views.correct_request),
    path('request/criterion_list', donation.views.criterion),
]
