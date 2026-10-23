from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/data/', views.api_data, name='api_data'),
    path('api/bookings/', views.api_bookings, name='api_bookings'),
    path('api/chat/', views.api_chat, name='api_chat'),
    path('api/signup/', views.api_signup, name='api_signup'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/auth-status/', views.api_auth_status, name='api_auth_status'),
]