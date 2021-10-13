from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('check_room', views.check_room, name='check_room'),

    # Django default authentication generic views
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
