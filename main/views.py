from django.shortcuts import render

def index(request):
    '''
    Shows index page
    '''
    return render(request, "index.html")