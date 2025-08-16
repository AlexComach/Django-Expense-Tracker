from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transactions, name='transactions'),
    path('report/', views.report, name='report'),
] 