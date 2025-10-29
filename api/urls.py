from django.urls import path
from . import views

app_name = 'api'  # Namespace for the API URLs

urlpatterns = [
    # Web interface URLs
    path('', views.home_view, name='home'),  # New home view
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # API endpoints
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/protected/', views.protected_api, name='protected_api'),
] 