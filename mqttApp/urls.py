from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register,name='register'),
    path('login/', views.login,name='login'),
    path('details/',views.details),
    path('deviceDetails/',views.deviceDetails,name='deviceDetails'),
    path('deviceDetails/<str:id>/<str:name>/',views.deviceDetails,name='deviceDetails'),

]
