from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from app1.forms import payForm, productForm
from app1.models import Register, payment, Category, product, Admin_log
from django.contrib.auth.hashers import make_password, check_password
from django.views import View


def index(request):
    products = None
    ct = Category.objects.all()
    categoryid = request.GET.get('category')
    if categoryid:
        products = product.get_all_prd_by_categoryID(categoryid)
    else:
        products = product.get_all_prd();
    data = {'products': products, 'ct': ct, "who": request.session.get('email')}

    return render(request, 'index.html', data)


#
# def category(request):
#     categories = Category.objects.all()
#     return render(request, 'index.html', {"categories": categories})


def aboutus(request):
    return render(request, 'aboutus.html')


def contact(request):
    return render(request, 'contact.html')


class cart(View):
    def get(self, request):
        ids = list(request.session.get('kart').keys())
        products = product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html', {'products': products})

def checkout(request):
    print("enter to 11111111111")
    form = payForm()
    if request.method == 'POST':
        print("enter to 222222222222222222")
        form = payForm(request.POST, request.FILES)
        if form.is_valid():
            print("enter to 3333333333333333333333")
            form.save()
            return redirect('finale')
        # else:
        #     return("*****ERROR IN VALIDATION******")
    return render(request, 'checkout.html', {"form": form})


def finale(request):
    return render(request, 'finale.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Register.get_customer_by_email(email)
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email
                return redirect('index')
            else:
                error_message = 'Email or Password Incorrect!!'
        else:
            error_message = 'Email or Password Incorrect!!'
        print(email, password)
        return render(request, 'login.html', {'error': error_message})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    else:
        postData = request.POST
        name = postData.get('name')
        email = postData.get('email')
        phone = postData.get('phone')
        password = postData.get('password')

        customer = Register(name=name,
                            email=email,
                            phone=phone,
                            password=password)
        error_message = None
        isExists = customer.isExists()
        if isExists:
            error_message = 'Email Already Exist'
        if not error_message:
            print(name, email, phone, password)
            customer.password = make_password(customer.password)

        customer.register()
        return redirect("index")


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
    def post(self, request):
        email = request.session.get('email')
        pro = request.POST.get('product')
        remove = request.POST.get('remove')
        kart = request.session.get('kart')
        if kart:
            quantity = kart.get(pro)
            if quantity:
                if remove:
                    if quantity <= 1:
                        kart.pop(pro)
                    else:
                        kart[pro] = quantity - 1
                else:
                    kart[pro] = quantity + 1

            else:
                kart[pro] = 1
        else:
            kart = {}
            kart[pro] = 1

        request.session['kart'] = kart
        print('cart', request.session['kart'])
        print('you are : ', request.session.get('email'))
        return redirect('/')

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


#######ADMIN#######

def admin_mall(request):
    return render(request, 'ad_mall.html')


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


def adminpro(request):
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
