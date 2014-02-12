from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test

from main.forms import AccessForm, AuthForm

# Auth views

def get_user_rol(user):
    """
    Function to determinate the user rol
    """
    return user.groups.values_list('name',flat=True)[0]

def _gen_password(password_length=8):
    password = []
    for group in (string.ascii_letters, string.digits):
        password += random.sample(group, 3)

    password += random.sample(string.ascii_letters + string.digits, password_length - len(password))
    random.shuffle(password)
    password = ''.join(password)
    return password

def is_admin(user):
    """
    Function to determinate if the user belongs to the admin group
    """
    if get_user_rol(user) == 'admin':
        return True
    return False

def is_client(user):
    """
    Function to determinate if the user belongs to the sales group
    """
    if get_user_rol(user) == 'client':
        return True
    return False

def login(request):
    '''
    Manage the login of the users
    '''

    if request.user.is_authenticated():
        if is_salesman(request.user):
            template = 'contacts'
        else:
            template = 'contacts'
        return redirect(template)

    auth_form = AuthenticationForm()
    if request.method == 'POST':
        auth_form = AuthenticationForm(None, request.POST)
        if auth_form.is_valid():
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            auth_login(request, form.get_user())
            if is_salesman(request.user):
                template = 'contacts'
            else:
                template = 'contacts'
            return redirect(template)
    return render_to_response('registration/login.html', RequestContext(request, {
        'form': auth_form,
    }))

@login_required
def logout(request):
    '''
    Manage the logout of the users
    '''
    auth_logout(request)
    return redirect(reverse('index'))

# App views

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
    Manage the login of the clients
    '''

    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(None, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('order')
    return render(request, "clients.html", {
        'form': form,
    })

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

@login_required
@user_passes_test(lambda u: is_client(u))
def order(request):
    '''
    Shows order page
    '''
    return render(request, "order.html")

