from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail

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
    if request.session.get('has_access') == True:
        return redirect('products')

    form = AccessForm()
    if request.method == 'POST':
        form = AccessForm(request.POST)
        if form.is_valid():
            request.session['has_access'] = True
            request.session.set_expiry(0)
            message = '''Alguien ha visto los productos de www.monin.com.mx
            \n\nEstos son los datos: \nNombre: %s \nCiudad: %s \nCorreo: %s
            ''' % (form.cleaned_data.get('name'), form.cleaned_data.get('city'), form.cleaned_data.get('email'))

            send_mail(settings.SUBJECT, message, settings.FROM, [settings.TO], fail_silently=False)
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
    if not request.session.get('has_access') == True:
        return redirect('access')
    return render(request, "products.html")

def contact(request):
    '''
    Shows contact page
    '''
    return render(request, "contact.html")

