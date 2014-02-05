from django.shortcuts import render

from main.forms import AccessForm

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

def our(request):
    '''
    Shows our page
    '''
    return render(request, "our.html")

def access(request):
    '''
    Shows access page
    '''
    form = AccessForm()
    if request.method == 'POST':
        form = AccessForm(request.POST)
        if form.is_valid():
            return redirect('products')
    return render(request, "access.html", {
        'form': form,
    })

def clients(request):
    '''
    Shows clients page
    '''
    return render(request, "clients.html")

def products(request):
    '''
    Shows products page
    '''
    return render(request, "products.html")

def contact(request):
    '''
    Shows contact page
    '''
    return render(request, "contact.html")

