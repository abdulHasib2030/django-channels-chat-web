from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('register/', views.UserRegisterView, name= 'signup'),
    path('home/', views.ChatPage, name= 'home'),
    path('login/', views.login_view, name= 'login'),
    path('home/<str:username>/', views.chat_view, name='username')
]