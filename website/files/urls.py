from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('SG/',views.SG, name='SG'),
    path('TE/',views.TE, name='TE'),
    path('CN',views.CN, name='CN'),
]