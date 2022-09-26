from unicodedata import name
from django.urls import path
from . import views

urlpatterns =[
    path('adminout',views.adminout,name='adminout'),
    path("",views.adminstart,name="adminstart"),
    path("home",views.adminhome,name="adminhome"),
    path('edituser',views.edituser,name='edituser'),
    path('deleteuser',views.deleteuser,name='deleteuser'),
    path('adduser',views.adduser,name='adduser')
    ]
