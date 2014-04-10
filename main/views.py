# -*- encoding: utf-8 -*-
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
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

from main.forms import (AccessForm, AuthForm, OrderForm, ClientCreationForm, CategoryCreationForm,
                        ProductCreationForm, ProductSampleCreationForm, SiteConfigurationForm,
                        ContactFrom, ConfigForm, ImageSliderCreationForm, CategorySampleCreationForm)
from main.models import Product, ProductSample, SiteConfiguration, CategorySample, Category, ImageSlider


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
    sliders = ImageSlider.objects.filter(active=True, category='1')
    return render(request, "index.html", {
        'sliders': sliders,
    })

def home(request):
    '''
    Shows home page
    '''
    sliders = ImageSlider.objects.filter(active=True, category='1')
    return render(request, "home.html", {
        'sliders': sliders,
    })

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

    sliders = ImageSlider.objects.filter(active=True, category='2')
    form = AccessForm()
    if request.method == 'POST':
        form = AccessForm(request.POST)
        if form.is_valid():
            request.session['has_access'] = True
            request.session.set_expiry(0)
            message = '''Alguien ha visto los productos de www.monin.com.mx
            \n\nEstos son los datos: \nNombre: %s \nCiudad: %s \nCorreo: %s
            ''' % (form.cleaned_data.get('name'), form.cleaned_data.get('city'), form.cleaned_data.get('email'))

            send_mail(settings.SUBJECT, message, settings.FROM, [SiteConfiguration.objects.all().first().email_to_notifications], fail_silently=False)
            return redirect('products')
    return render(request, "access.html", {
        'form': form,
        'sliders':sliders,
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
    return render(request, "products.html", {
        'categories': CategorySample.objects.filter(active=True),
        'products': ProductSample.objects.filter(active=True),
    })

@login_required
@user_passes_test(lambda u: is_client(u))
def checkorder(request):
    '''
    Shows check order page
    '''
    message = ''
    if request.method == 'POST':
        orders = request.user.orders.all()
        if orders:
            c = Context({
                'orders': orders,
                'username': request.user.username,
            })
            text_content = render_to_string('mail/order_from_web.txt', c)
            html_content = render_to_string('mail/order_from_web.html', c)
            email = EmailMultiAlternatives(settings.SUBJECT, text_content)
            email.attach_alternative(html_content, "text/html")
            email.to = [SiteConfiguration.objects.all().first().email_to_notifications]
            email.send()
            message = 'El pedido se ha realizado exitosamente!'
            for order in orders:
                order.delete()
        else:
            message = 'No se puede enviar un pedido vacio'
    return render(request, "checkorder.html", {'message': message})

@login_required
@user_passes_test(lambda u: is_client(u))
def order(request):
    '''
    Shows order page
    '''
    categories = Category.objects.filter(active=True)
    return render(request, "order.html", {
        'categories': categories,
    })


@login_required
@user_passes_test(lambda u: is_client(u))
def order_category(request, pk):
    '''
    Shows order category page
    '''
    products = Product.objects.filter(active=True, category__pk=pk)
    return render(request, "order_category.html", {
        'products': products,
    })

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
        'product': product,
    })

@login_required
@user_passes_test(lambda u: is_client(u))
def orders_delete(request,):
    '''
    Delete  order product
    '''
    orders = request.user.orders.all()
    for order in orders:
        order.delete()
    return HttpResponse(json.dumps({'response': 1}))

@login_required
@user_passes_test(lambda u: is_client(u))
def order_delete(request,):
    '''
    Delete  order product
    '''
    order = request.user.orders.get(pk=request.POST.get('pk'))
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
            Q(username__icontains=search)
        )
    else:
        clients = User.objects.filter(groups__name='client')

    count = clients.count()
    for client in clients[start:end]:
        label = 'Desactivar' if client.is_active else 'Activar   '
        aaData.append([
            client.username,
            client.date_joined.strftime('%d-%m-%Y'),
            client.last_login.strftime('%d-%m-%Y'),
            'Activo' if client.is_active else 'Inactivo',
            '<a href="/admin/clients/password/%s"><button type="button" class="btn btn-xs btn-info">Cambiar contraseña</button></a>&nbsp;<button type="button" data-id="%s" class="deactivate-button btn btn-xs btn-warning">%s</button>&nbsp;<a href="/admin/clients/delete/%s"><button type="button"  class="delete-button btn btn-xs btn-danger">Eliminar</button></a>' % (client.pk, client.pk, label, client.pk),
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
        sizes = ''
        if order.qty_1:
            sizes = sizes + 'Talla 1:%s, ' % order.qty_1
        if order.qty_2:
            sizes = sizes + 'Talla 2:%s, ' % order.qty_2
        if order.qty_3:
            sizes = sizes + 'Talla 3:%s, ' % order.qty_3
        if order.qty_4:
            sizes = sizes + 'Talla 4:%s, ' % order.qty_4
        if order.qty_6:
            sizes = sizes + 'Talla 6:%s, ' % order.qty_6
        if order.qty_8:
            sizes = sizes + 'Talla 8:%s, ' % order.qty_8
        if order.qty_10:
            sizes = sizes + 'Talla 10:%s, ' % order.qty_10
        if order.qty_12:
            sizes = sizes + 'Talla 12:%s, ' % order.qty_12
        if order.qty_14:
            sizes = sizes + 'Talla 14:%s, ' % order.qty_14
        if order.qty_16:
            sizes = sizes + 'Talla 16:%s, ' % order.qty_16
        aaData.append([
            order.product.model,
            order.product.price,
            order.color,
            sizes,
            '<button data-id="%s" type="button"  class="delete-button btn btn-xs btn-danger">Eliminar</button>' % order.pk,
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
    form = ContactFrom()
    info = ''
    if request.method == 'POST':
        form = ContactFrom(request.POST)
        if form.is_valid():
            message = '%s con cuenta de correo:%s escribio un mensaje: %s' % (
                form.cleaned_data.get('name'), form.cleaned_data.get('email'), 
                form.cleaned_data.get('message')
            )
            send_mail(settings.SUBJECT, message, settings.FROM, [SiteConfiguration.objects.all().first().email_to_notifications], fail_silently=False)
            info = 'Tu mensaje se ha sido enviado, gracias por contactarnos. Estaremos respondiendo a la brevedad'
    return render(request, "contact.html", {'form': form, 'info': info})

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
        orders = []
        for i in range(15):
            i = i + 1 
            if request.POST.get('active-%s' % i) == '1':
                orders.insert(0, [
                    request.POST.get('model-' + str(i)),
                    request.POST.get('color-' + str(i)),
                    request.POST.get('quantity-' + str(i)),
                    request.POST.get('size-' + str(i)),
                ])
        c = Context({
            'orders': orders,
            'username': request.user.username,
            'client': request.POST.get('name-1'),
        })
        text_content = render_to_string('mail/order_from_mobile.txt', c)
        html_content = render_to_string('mail/order_from_mobile.html', c)
        email = EmailMultiAlternatives(settings.SUBJECT, text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = [SiteConfiguration.objects.all().first().email_to_notifications]
        email.send()
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
            Q(username__icontains=search)
        )
    else:
        clients = User.objects.filter(groups__name='client')

    count = clients.count()
    for client in clients[start:end]:
        label = 'Desactivar' if client.is_active else 'Activar   '
        aaData.append([
            client.username,
            client.date_joined.strftime('%d-%m-%Y'),
            client.last_login.strftime('%d-%m-%Y'),
            'Activo' if client.is_active else 'Inactivo',
            '<a href="/admin/clients/password/%s"><button type="button" class="btn btn-xs btn-info">Cambiar contraseña</button></a>&nbsp;<button type="button" data-id="%s" class="deactivate-button btn btn-xs btn-warning">%s</button>&nbsp;<a href="/admin/clients/delete/%s"><button type="button"  class="delete-button btn btn-xs btn-danger">Eliminar</button></a>' % (client.pk, client.pk, label, client.pk),
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
@user_passes_test(lambda u: is_admin(u))
def admin_config(request):
    '''
    Shows config page
    '''
    info = ''
    form = ConfigForm(instance=SiteConfiguration.objects.all().first())
    if request.method == 'POST':
        form = ConfigForm(request.POST, request.FILES, instance=SiteConfiguration.objects.all().first())
        if form.is_valid():
            form.save()
            info = 'Se ha guardado de forma correcta la configuracion'
    return render(request, "admin_config.html", {
        'form': form,
        'info': info,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_client_add(request):
    '''
    Shows add client page
    '''
    form = ClientCreationForm()
    if request.method == 'POST':
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Group.objects.get(name='client').user_set.add(user)
            return redirect(reverse('admin'))
    return render(request, "admin_client_add.html", {
        'form': form,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_client_password(request, pk):
    '''
    Shows change password page
    '''
    user = User.objects.get(pk=pk)
    form = AdminPasswordChangeForm(user)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            return redirect(reverse('admin'))
    return render(request, "admin_client_password.html", {
        'form': form,
        'pk': pk,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_client_deactivate(request):
    '''
    Shows add client page
    '''
    if request.method == 'POST':
        user = User.objects.get(pk=request.POST.get('pk'))
        user.is_active = not user.is_active
        user.save()
        return HttpResponse(json.dumps({'response': 1}))

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_client_delete(request, pk):
    '''
    Shows add client page
    '''
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect(reverse('admin'))
    return render(request, "admin_client_delete.html", {
        'user': user,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_categories_sample(request):
    '''
    Shows categories sample page
    '''
    return render(request, "admin_categories_sample.html")

@login_required
def admin_categories_sample_all(request):
    '''
    Retrive all categories sample to fill the categories table
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
        categories = CategorySample.objects.filter(
            Q(name__icontains=search)
        )
    else:
        categories = CategorySample.objects.all()

    count = categories.count()
    for category in categories[start:end]:
        label = 'Desactivar' if category.active else 'Activar   '
        aaData.append([
            category.name,
            'Activo' if category.active else 'Inactivo',
            '<button type="button" data-id="%s" class="deactivate-button btn btn-xs btn-warning">%s</button>&nbsp;<a href="/admin/category/delete/%s"><button type="button"  class="delete-button btn btn-xs btn-danger">Eliminar</button></a>' % (category.pk, label, category.pk),
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
@user_passes_test(lambda u: is_admin(u))
def admin_category_sample_add(request):
    '''
    Shows add category sample page
    '''
    form = CategorySampleCreationForm()
    if request.method == 'POST':
        form = CategorySampleCreationForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect(reverse('admin_categories_sample'))
    return render(request, "admin_category_sample_add.html", {
        'form': form,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_category_sample_deactivate(request):
    '''
    Shows deactivate category page
    '''
    if request.method == 'POST':
        category = CategorySample.objects.get(pk=request.POST.get('pk'))
        category.active = not category.active
        category.save()
        return HttpResponse(json.dumps({'response': 1}))

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_category_sample_delete(request, pk):
    '''
    Shows add client page
    '''
    category = CategorySample.objects.get(pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect(reverse('admin_categories_sample'))
    return render(request, "admin_category_sample_delete.html", {
        'category': category,
    })


@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_products_sample(request):
    '''
    Shows products sample page
    '''
    return render(request, "admin_products_sample.html")

@login_required
def admin_products_sample_all(request):
    '''
    Retrive all products sample to fill the products table
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
        products = ProductSample.objects.filter(
            Q(name__icontains=search)
        )
    else:
        products = ProductSample.objects.all()

    count = products.count()
    for product in products[start:end]:
        label = 'Desactivar' if product.active else 'Activar   '
        aaData.append([
            product.name,
            product.category.name,
            'Activo' if product.active else 'Inactivo',
            '<a href="%s"><button type="button" class="btn btn-xs btn-info">Ver foto</button></a>&nbsp;<button type="button" data-id="%s" class="deactivate-button btn btn-xs btn-warning">%s</button>&nbsp;<a href="/admin/product/sample/delete/%s"><button type="button"  class="delete-button btn btn-xs btn-danger">Eliminar</button></a>' % (product.photo.url, product.pk, label, product.pk),
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
@user_passes_test(lambda u: is_admin(u))
def admin_product_sample_add(request):
    '''
    Shows add product sample page
    '''
    form = ProductSampleCreationForm()
    if request.method == 'POST':
        form = ProductSampleCreationForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect(reverse('admin_products_sample'))
    return render(request, "admin_product_sample_add.html", {
        'form': form,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_product_sample_deactivate(request):
    '''
    Shows deactivate product page
    '''
    if request.method == 'POST':
        product = ProductSample.objects.get(pk=request.POST.get('pk'))
        product.active = not product.active
        product.save()
        return HttpResponse(json.dumps({'response': 1}))

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_product_sample_delete(request, pk):
    '''
    Shows add client page
    '''
    product = ProductSample.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect(reverse('admin_products_sample'))
    return render(request, "admin_product_sample_delete.html", {
        'product': product,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_products(request):
    '''
    Shows products sample page
    '''
    return render(request, "admin_products.html")

@login_required
def admin_products_all(request):
    '''
    Retrive all products sample to fill the products table
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
        products = Product.objects.filter(
            Q(name__icontains=search)
        )
    else:
        products = Product.objects.all()

    count = products.count()
    for product in products[start:end]:
        label = 'Desactivar' if product.active else 'Activar   '
        aaData.append([
            product.model,
            '%s' % product.category.name if product.category else 'No disponible',
            '$%s' % round(product.price, 2),
            'Activo' if product.active else 'Inactivo',
            '<a href="%s"><button type="button" class="btn btn-xs btn-info">Ver foto</button></a>&nbsp;<button type="button" data-id="%s" class="deactivate-button btn btn-xs btn-warning">%s</button>&nbsp;<a href="/admin/product/delete/%s"><button type="button"  class="delete-button btn btn-xs btn-danger">Eliminar</button></a>' % (product.photo.url, product.pk, label, product.pk),
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
@user_passes_test(lambda u: is_admin(u))
def admin_product_add(request):
    '''
    Shows add product sample page
    '''
    form = ProductCreationForm()
    if request.method == 'POST':
        data = request.POST.copy()
        for d in data:
            data[d] = data[d].replace('$', '').replace(',', '')
        form = ProductCreationForm(data, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect(reverse('admin_products'))
    return render(request, "admin_product_add.html", {
        'form': form,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_product_deactivate(request):
    '''
    Shows deactivate product page
    '''
    if request.method == 'POST':
        product = Product.objects.get(pk=request.POST.get('pk'))
        product.active = not product.active
        product.save()
        return HttpResponse(json.dumps({'response': 1}))

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_product_delete(request, pk):
    '''
    Shows add client page
    '''
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect(reverse('admin_products'))
    return render(request, "admin_product_delete.html", {
        'product': product,
    })


@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_sliders(request):
    '''
    Shows sliders sample page
    '''
    return render(request, "admin_sliders.html")

@login_required
def admin_sliders_all(request):
    '''
    Retrive all sliders sample to fill the sliders table
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
        sliders = ImageSlider.objects.filter(
            Q(name__icontains=search)
        )
    else:
        sliders = ImageSlider.objects.all()

    count = sliders.count()
    for slider in sliders[start:end]:
        label = 'Desactivar' if slider.active else 'Activar   '
        aaData.append([
            slider.name,
            'Principal' if slider.category == '1' else 'Productos',
            'Activo' if slider.active else 'Inactivo',
            '<a href="%s"><button type="button" class="btn btn-xs btn-info">Ver foto</button></a>&nbsp;<button type="button" data-id="%s" class="deactivate-button btn btn-xs btn-warning">%s</button>&nbsp;<a href="/admin/slider/delete/%s"><button type="button"  class="delete-button btn btn-xs btn-danger">Eliminar</button></a>' % (slider.photo.url, slider.pk, label, slider.pk),
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
@user_passes_test(lambda u: is_admin(u))
def admin_slider_add(request):
    '''
    Shows add slider sample page
    '''
    form = ImageSliderCreationForm()
    if request.method == 'POST':
        form = ImageSliderCreationForm(request.POST, request.FILES)
        if form.is_valid():
            slider = form.save()
            return redirect(reverse('admin_sliders'))
    return render(request, "admin_slider_add.html", {
        'form': form,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_slider_deactivate(request):
    '''
    Shows deactivate slider page
    '''
    if request.method == 'POST':
        slider = ImageSlider.objects.get(pk=request.POST.get('pk'))
        slider.active = not slider.active
        slider.save()
        return HttpResponse(json.dumps({'response': 1}))

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_slider_delete(request, pk):
    '''
    Shows delete slider page
    '''
    slider = ImageSlider.objects.get(pk=pk)
    if request.method == 'POST':
        slider.delete()
        return redirect(reverse('admin_sliders'))
    return render(request, "admin_slider_delete.html", {
        'slider': slider,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_categories(request):
    '''
    Shows categories  page
    '''
    return render(request, "admin_categories.html")

@login_required
def admin_categories_all(request):
    '''
    Retrive all categories  to fill the categories table
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
        categories = Category.objects.filter(
            Q(name__icontains=search)
        )
    else:
        categories = Category.objects.all()

    count = categories.count()
    for category in categories[start:end]:
        label = 'Desactivar' if category.active else 'Activar   '
        aaData.append([
            category.name,
            'Activo' if category.active else 'Inactivo',
            '<a href="%s"><button type="button" class="btn btn-xs btn-info">Ver foto</button></a>&nbsp;<button type="button" data-id="%s" class="deactivate-button btn btn-xs btn-warning">%s</button>&nbsp;<a href="/admin/category/delete/%s"><button type="button"  class="delete-button btn btn-xs btn-danger">Eliminar</button></a>' % (category.photo.url, category.pk, label, category.pk),
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
@user_passes_test(lambda u: is_admin(u))
def admin_category_add(request):
    '''
    Shows add category sample page
    '''
    form = CategoryCreationForm()
    if request.method == 'POST':
        form = CategoryCreationForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect(reverse('admin_categories'))
    return render(request, "admin_category_add.html", {
        'form': form,
    })

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_category_deactivate(request):
    '''
    Shows deactivate category page
    '''
    if request.method == 'POST':
        category = Category.objects.get(pk=request.POST.get('pk'))
        category.active = not category.active
        category.save()
        return HttpResponse(json.dumps({'response': 1}))

@login_required
@user_passes_test(lambda u: is_admin(u))
def admin_category_delete(request, pk):
    '''
    Shows add category page
    '''
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect(reverse('admin_categories'))
    return render(request, "admin_category_delete.html", {
        'category': category,
    })