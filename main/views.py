#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse , Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from main.forms import AccessForm, AuthForm, OrderForm
from main.models import Product


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
    Function to determinate if the user belongs to the clients group
    """
    if get_user_rol(user) == 'client':
        return True
    return False

def is_distributor(user):
    """
    Function to determinate if the user belongs to the distibutor group
    """
    if get_user_rol(user) == 'distributor':
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
    auth_logout(request)
    form = AuthForm()
    form_errors = None
    if request.method == 'POST':
        form = AuthForm(None, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('order')
        else:
          form_errors = form.errors.get('__all__')
    return render(request, "clients.html", {
        'form': form,
        'form_errors': form_errors,
    })

def products(request):
    '''
    Shows products page
    '''
    if not request.session.get('has_access') == True:
        return redirect('access')
    return render(request, "products.html")

@login_required
@user_passes_test(lambda u: is_client(u))
def order(request):
    '''
    Shows order page
    '''
    return render(request, "order.html")

@login_required
@user_passes_test(lambda u: is_client(u))
def order_product(request, pk):
    '''
    Shows order product page
    '''
    product = Product.objects.get(pk=pk)
    form = OrderForm(initial={'product': product})
    form_errors = None
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.client = request.user
            order.save()
            return redirect('order')
    return render(request, "product_order.html", {
        'form': form,
        'form_errors': form_errors,
        'pk': pk,
    })

@login_required
@user_passes_test(lambda u: is_client(u))
def order_delete(request,):
    '''
    Delete  order product
    '''
    orders = request.user.orders.all()
    for order in orders:
        order.delete()
    return HttpResponse(json.dumps({'response': 1}))

@login_required
@user_passes_test(lambda u: is_client(u))
def order_do(request,):
    '''
    Do a order product
    '''
    orders = request.user.orders.all()
    message = 'Pedido realizado por el cliente con num %s desde  www.monin.com.mx:\n\n' % request.user.username
    for order in orders:
        message += 'Modelo:%s Talla:%s  Color:%s Cantidad:%s Precio:%s \n' % (order.product.model, order.size, order.color, order.quantity, order.product.price)

    send_mail(settings.SUBJECT, message, settings.FROM, [settings.TO], fail_silently=False)
    for order in orders:
        order.delete()
    return HttpResponse(json.dumps({'response': 1}))

@login_required
def products_all(request):
    '''
    Retrive all products to fill the products table
    '''
    aaData = []
    start = request.POST.get('iDisplayStart')
    display_length = request.POST.get('iDisplayLength')
    end = start + display_length
    search = request.POST.get('sSearch')
    sort = request.POST.get('iSortCol_0')
    ORDER_BY_FIELDS = {
        0: 'model',
    }

    if search:
        products = Product.objects.exclude(active=False).filter(
            Q(model__icontains=search)
        )
    else:
        products = Product.objects.filter(active=True)

    if sort:
        direction = '-' if request.POST.get('sSortDir_0') == 'desc' else '' # asc or desc?
        index_of_field = int(sort) # order by which field?
        order_statment = direction + ORDER_BY_FIELDS.get(index_of_field)
        products = products.order_by(order_statment)

    count = products.count()
    for product in products[start:end]:
        aaData.append([
            product.model,
            product.price,
            '<a href="order/product/%s"><input type="submit" class="superbutton do-order" value="Agregar a pedido"></a>' % product.pk,
        ])
    data = {
        "iTotalRecords": count,
        "iDisplayStart": start,
        "iDisplayLength": display_length,
        "iTotalDisplayRecords": count,
        "aaData":aaData
    }
    return HttpResponse(json.dumps(data))

@login_required
def clients_all(request):
    '''
    Retrive all clients to fill the products table
    '''
    aaData = []
    start = request.POST.get('iDisplayStart')
    display_length = request.POST.get('iDisplayLength')
    end = start + display_length
    search = request.POST.get('sSearch')
    sort = request.POST.get('iSortCol_0')
    ORDER_BY_FIELDS = {
        0: 'model',
    }

    if search:
        clients = User.objects.filter(groups__name='client').filter(
            Q(username=search)
        )
    else:
        clients = User.objects.filter(groups__name='client')

    count = clients.count()
    for client in clients[start:end]:
        aaData.append([
            client.username,
            client.date_joined.strftime('%d-%m-%Y'),
            client.last_login.strftime('%d-%m-%Y'),
            'Activo' if client.is_active else 'Inactivo',
            '<a href=""><button type="button" class="btn btn-xs btn-info">Cambiar contraseña</button></a>&nbsp;<a href=""><button type="button" class="btn btn-xs btn-warning">Desactivar</button></a>&nbsp;<a href=""><button type="button" class="btn btn-xs btn-danger">Eliminar</button></a>',
        ])
    data = {
        "iTotalRecords": count,
        "iDisplayStart": start,
        "iDisplayLength": display_length,
        "iTotalDisplayRecords": count,
        "aaData":aaData
    }
    return HttpResponse(json.dumps(data))


@login_required
def orders_all(request):
    '''
    Retrive all orders to fill the orders table
    '''
    aaData = []
    start = request.POST.get('iDisplayStart')
    display_length = request.POST.get('iDisplayLength')
    end = start + display_length
    search = request.POST.get('sSearch')
    sort = request.POST.get('iSortCol_0')
    orders = request.user.orders.all()

    count = orders.count()
    for order in orders[start:end]:
        aaData.append([
            order.product.model,
            order.product.price,
            order.color,
            order.size,
            order.quantity,
        ])

    data = {
        "iTotalRecords": count,
        "iDisplayStart": start,
        "iDisplayLength": display_length,
        "iTotalDisplayRecords": count,
        "aaData":aaData
    }
    return HttpResponse(json.dumps(data))

def contact(request):
    '''
    Shows contact page
    '''
    return render(request, "contact.html")


# Mobile views

def mobile(request):
    '''
    Shows index mobile page
    '''
    auth_logout(request)
    form = AuthForm()
    form_errors = None
    if request.method == 'POST':
        form = AuthForm(None, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('mobile_order')
        else:
          form_errors = form.errors.get('__all__')
    return render(request, "mobile.html", {
        'form': form,
        'form_errors': form_errors,
    })

@login_required
@user_passes_test(lambda u: is_distributor(u))
def mobile_order(request):
    '''
    Shows order page
    '''
    if request.method == 'POST':
        message = 'Pedido realizado desde  www.monin.com.mx:\n\n'
        for i in range(15):
            i = i + 1 
            if request.POST.get('active-%s' % i) == '1':
                message += 'Modelo:%s Talla:%s  Color:%s Cantidad:%s Precio:%s \n' % (request.POST.get('model-' + str(i)), request.POST.get('size-' + str(i)), request.POST.get('color-' + str(i)), request.POST.get('quantity-' + str(i)), request.POST.get('price-' + str(i)))

        send_mail(settings.SUBJECT, message, settings.FROM, [settings.TO], fail_silently=False)
        return render(request, "mobile_order_sent.html")
    return render(request, "mobile_order.html", {
        'loop': [i+1 for i in range(16)]
    })

# Admin views
def admin_login(request):
    '''
    Shows index mobile page
    '''
    auth_logout(request)
    form = AuthForm()
    form_errors = None
    if request.method == 'POST':
        form = AuthForm(None, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('admin')
        else:
          form_errors = form.errors.get('__all__')
    return render(request, "admin_login.html", {
        'form': form,
        'form_errors': form_errors,
    })

# Admin views
@login_required
@user_passes_test(lambda u: is_admin(u))
def admin(request):
    '''
    Shows index mobile page
    '''
    return render(request, "admin.html")