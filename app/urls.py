from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    # path('user-logs/', views.UserLogs, name='user-logs'),
]