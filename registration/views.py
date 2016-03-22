from django.shortcuts import render
from django.http import HttpResponse

from .forms import RegistrationForm

def index(request):
    return render(request, 'registration/info.html')

def status(request):
    return render(request, 'registration/status.html')

def payment(request):
    form = RegistrationForm()
    return render(request, 'registration/payment.html', {'form': form})
