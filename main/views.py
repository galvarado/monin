from django.shortcuts import render

def index(request):
    '''
    Shows index page
    '''
    return render(request, "index.html")

def home(request):
    '''
    Shows home page
    '''
    return render(request, "home.html")

def zohoverify(request):
    '''
    Shows index page
    '''
    return render(request, "verifyforzoho.html")