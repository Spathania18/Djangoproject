from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name = 'signin'),
    path('signup', views.signup, name = 'signup'),
    path('homepage', views.homepage, name = 'homepage'),
    path('application', views.application, name = 'application'),
    path('allapplications', views.allapplications, name = 'allapplications'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('logout', LogoutView.as_view(next_page='signin'), name='logout'),
    #path('dashboard/filter/', views.filter_dashboard, name='filter_dashboard'),
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),
]


