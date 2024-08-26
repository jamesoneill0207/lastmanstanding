from django.urls import path 
from league import views

app_name = 'league'

urlpatterns = [
    path('', views.home, name='home'),
]