from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('personas/', views.personas_list, name='personas_list'),
    path('personas/<int:pk>/', views.persona_detail, name='persona_detail'),
    path('personas/<int:pk>/select/', views.select_persona, name='select_persona'),
    path('personas/create/', views.persona_create, name='persona_create'),
    path('personas/<int:pk>/edit/', views.persona_edit, name='persona_edit'),
    path('personas/<int:pk>/delete/', views.persona_delete, name='persona_delete'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

