from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('seating-chart-upload/', views.seating_chart_upload, name='seating_chart_upload'),
    path('seating-chart-type/', views.seating_chart_type, name='seating_chart_type'),
    path('together/', views.together, name="together"),
    path('together/seating_chart_webpage', views.seating_chart_webpage, name='seating_chart_webpage'),

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])