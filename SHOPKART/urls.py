from unicodedata import name
from django.urls import path
from . import views

urlpatterns =[
    
    path("",views.startingpage,name="start"),
    path("home",views.homepage,name="home"),
    path("signup",views.signuppage,name="signup"),
    path("logout",views.logout,name="logout")
    ]

