from django.contrib import admin
from django.urls import path,include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('music_quiz', views.music_quiz, name='music_quiz'),
]