from django.urls import path 
from league import views

app_name = 'league'

urlpatterns = [
    path('gw1-19/', views.gw1_19, name='gw1-19'),
    path('gw20-38/', views.gw20_38, name='gw20-38'),
]

