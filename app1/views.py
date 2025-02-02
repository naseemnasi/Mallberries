from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from app1.forms import productForm
from app1.models import Register, Category, product, Admin_log, Order
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from app1.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator


def index(request):
    products = None
    ct = Category.objects.all()
    categoryid = request.GET.get('category')
    if categoryid:
        products = product.get_all_prd_by_categoryID(categoryid)
    else:
        products = product.get_all_prd();
    data = {'products': products, 'ct': ct}

    return render(request, 'index.html', data,)


#
# def category(request):
#     categories = Category.objects.all()
#     return render(request, 'index.html', {"categories": categories})


def aboutus(request):
    return render(request, 'aboutus.html')


def contact(request):
    return render(request, 'contact.html')


class Cart(View):
    def get(self, request):
        kart = request.session.get('kart')
        if not kart:
            request.session['kart'] = {}
        ids = list(request.session.get('kart').keys())
        products = product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html', {'products': products})


class checkout(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        return render(request, 'checkout.html')

    def post(self, request):
        customer_name = request.POST.get('customer_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        kart = request.session.get('kart')
        products = product.get_products_by_id(list(kart.keys()))
        print(address, phone, customer, kart, products, customer_name)

        for p in products:
            print(kart.get(str(p.id)))
            order = Order(customer=Register(id=customer),
                          customer_name=customer_name,
                          product=p,
                          price=p.price,
                          address=address,
                          phone=phone,
                          quantity=kart.get(str(p.id)))
            order.placeOrder()
        request.session['kart'] = {}

        return redirect('finale')


class finale(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'finale.html', {"orders": orders})


def login(request):
    return_url = None
    if request.method == 'GET':
        login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Register.get_customer_by_email(email)
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if login.return_url:
                    return HttpResponseRedirect(login.return_url)
                else:
                    login.return_url = None
                    return redirect('index')
            else:
                error_message = 'Email or Password Incorrect!!'
        else:
            error_message = 'Email or Password Incorrect!!'
        print(email, password)
        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        postData = request.POST
        name = postData.get('name')
        email = postData.get('email')
        phone = postData.get('phone')
        password = postData.get('password')
        # validation
        value = {
            'email': email
        }
        error_message = None

        customer = Register(name=name,
                            email=email,
                            phone=phone,
                            password=password)
        error_message = self.validateCustomer(customer)
        if not error_message:
            print(name, email, phone, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect("login")
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'register.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if customer.isExists():
            error_message = 'Email Address Already Registered..'

        return error_message
    # saving


####products####

def prod(request):
    products = None
    ct = Category.objects.all()
    categoryid = request.GET.get('category')
    if categoryid:
        products = product.get_all_prd_by_categoryID(categoryid)
    else:
        products = product.get_all_prd();
    data = {'products': products, 'ct': ct}
    return render(request, 'product.html', data)


class details(View):
    def get(self, request):
        products = None
        # request.session.clear()
        pd = product.objects.all()
        prdid = request.GET.get('id')
        if prdid:
            products = product.get_all_prd_by_id(prdid)
        else:
            pass;
        data = {'products': products, 'pd': pd}
        return render(request, 'pro_details.html', data)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        kart = request.session.get('kart')
        if kart:
            quantity = kart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        kart.pop(product)
                    else:
                        kart[product] = quantity - 1
                else:
                    kart[product] = quantity + 1

            else:
                kart[product] = 1
        else:
            kart = {}
            kart[product] = 1

        request.session['kart'] = kart
        print('cart', request.session['kart'])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#######ADMIN#######

def admin_mall(request):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('ad_login')
    return render(request, 'ad_mall.html',{"logged_user": request.session['username']})


def ad_log(request):
    login_status = ''
    print("11111")
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        if username is not None and password is not None:
            print("2222")
            login = Admin_log.objects.filter(
                Q(username=username) &
                Q(password=password)
            )
            if login:
                print("33333")
                request.session['username'] = username
                return redirect('admin_emall')
            else:
                login_status = 'Invalid Username or Password'
    return render(request, "ad_login.html", {"login_status": login_status})


def ad_logout(request):
    try:
        del request.session['username']
    except:
        pass
    return HttpResponseRedirect("ad_login")

def adminpro(request):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('ad_login')
    print("new")
    form = productForm()
    if request.method == 'POST':
        print("called")
        form = productForm(request.POST, request.FILES)
        print("ok")
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("*****ERROR IN VALIDATION******")
    return render(request, 'ad_addpro.html', {"form": form})


def ad_proList(request):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('ad_login')
    products = product.get_all_prd();
    return render(request, 'ad_proList.html', {"products": products})


def pdelete(request, pro_id):
    ob = product.objects.get(id=pro_id)
    if ob:
        ob.delete()
        return redirect('ad_proList')


def ad_orders(request):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('ad_login')
    orders = Order.objects.all();
    customer = request.session.get('customer')
    pd = Order.get_orders_by_customer(customer)
    data = {"orders": orders,
            "pd": pd}
    return render(request, 'ad_orders.html', data)


def odelete(request, order_id):
    ob = Order.objects.get(id=order_id)
    if ob:
        ob.delete()
        return redirect('ad_orders')

def ad_customerList(request):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('ad_login')
    registers = Register.objects.all()
    return render(request, 'ad_customerList.html', {"registers": registers})