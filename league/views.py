from django.shortcuts import render
from django.http import HttpResponse 

def home(request):
    context_dict = {'boldmessage': 'Last man standing - EPL'}
    
    return render(request, 'league/home.html', context=context_dict)