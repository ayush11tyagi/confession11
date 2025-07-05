from django.urls import path
from . import views

urlpatterns = [
    path('', views.confession_list, name='confession_list'),
    path('submit/', views.submit_confession, name='submit_confession'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
] 