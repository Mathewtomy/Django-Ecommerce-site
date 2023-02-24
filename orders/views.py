from django.shortcuts import render
from django.http import HttpResponse

# HttpResponse= sending request
# Create your views here.
# def index(request):
#     return HttpResponse("<h1> welcome to products </h1>")

def index(request):
    
    return HttpResponse("<h1> Your order List </h1>")

