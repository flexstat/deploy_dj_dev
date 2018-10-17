from django.shortcuts import render
import datetime



def landing(request):
    now = datetime.datetime.now()
    return render(request, 'landing/landing.html', locals()) 
