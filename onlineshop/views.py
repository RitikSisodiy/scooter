from django.db.models.fields import NOT_PROVIDED
from LeoScooter.settings import SECRET_KEY
from django import views
from django.shortcuts import render, redirect
from . models import *
from django.contrib.admin.decorators import register
from django.core import mail
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.views import View
from . forms import *
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum
import json
import string
import random
from django.contrib.auth.decorators import login_required
MERCHANT_KEY='a1Q7vq@5Q#PvFVc@'

# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'index.html',context)

def about(request):
    return render(request,'about.html')

def careers(request):
    return render(request,'careers.html')

def contact(request):
    message =""
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        sub = request.POST['sub']
        question = request.POST['question']
        data = Contact(name=name, email=email, phone=phone, sub=sub, question=question)
        data.save()
        # print(name + phone + sub)
        subject = 'LeoElectric Contact'
        html_message = render_to_string('email.html',{'name':name,'phone':phone,'email':email,'sub':sub, 'question':question})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = 'surajnaithani70@gmail.com'
        send_mail(subject, plain_message, from_email,[to],
        fail_silently=True,
        )
        message = "Thanks For Contacting Us We Will Get Back To You Soon :)"
    return render(request,'contact.html',{"msg": message})

def products(request):
    prod = Product.objects.all()
    return render(request,'productpage.html',{'products':prod})

def testdrive(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        bikemodel = request.POST['bikemodel']
        address = request.POST['address']
        zipcode = request.POST['zipcode']
        question = request.POST['question']
        data = TestDrive(name=name, email=email, phone=phone, bikemodel=bikemodel,address=address,zipcode=zipcode, question=question)
        data.save()
        # print(name + phone + bikemodel + zipcode + address)
    return render(request,'testdrive.html')

def productdetails(request,id):
    return render(request,'ProductDetails.html',)

def register(request):
    form = CustomerRegistrationForm()

    if request.method == 'POST':

        # if User.objects.filter(username = username).exists():
        #     messages.error(request, "This username is already taken")
        #     return redirect('register')

        # if User.objects.filter(email=email).exists():
        #     messages.error(request,"email is already in use")
        #     return redirect('register')

        # if len(username) > 10:
        #     messages.error(request,"username must be under 10 characters")
        #     return redirect('register')

        # if not username.isalnum():
        #     messages.error(request,"username should contain letters and numbers only")
        #     return redirect('register')
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        # cls='p-3 mb-2 bg-success text-white' 
        # msg='yours account is created succesfully'
        # return render(request,'user_login.html',{'cls':cls, 'msg':msg})
            messages.success(request,'your account is created successfully')
            return redirect('userlogin')
    return render(request,'Register.html',{'form':form,'form1':form})

# class CustomerRegistrationView(View):
#     def get(self, request):
#         form = CustomerRegistrationForm()
#         return render(request, 'registration.html',{'form':form})

#     def Post(self, request):
#         form = CustomerRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return render(request, 'registration.html',{'form':form})



def userlogin(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "successfully logged in")
            if request.user.is_superuser:
                return redirect('dashboardindex')
            if request.GET.get('next') is not None:
                return redirect(request.GET.get('next'))
            return redirect('profile')
        else:
            messages.error(request, "invalid credentials, please try again")
            return redirect('userlogin')

    return render(request,'user_login.html')

# def profile(request):
#     return render(request,'Profile.html')

class profileview(View):
    def get(self,request):
        res = {}
        res['n_order'] = OrderPlaced.objects.filter(user=request.user.id).count()
        res['n_tdrive'] = TestDrive.objects.filter(email=request.user.email).count()
        form = CustomerProfileForm()
        return render(request,'userdashboard.html',res)

    def post(self, request):
        if  profile.objects.filter(user=request.user.id).exists():
            form = CustomerProfileForm(request.POST,instance=profile.objects.filter(user=request.user.id)[0])
        else:
            form = CustomerProfileForm(request.POST)
        form1 = CustomeruserForm(request.POST,instance=request.user)
        if form.is_valid() and form1.is_valid:
            form.save()
            form1.save()
            messages.success(request,'Profile Updated Successfully')
            if request.GET.get('next') is not None and request.GET.get('next') !='':
                return redirect(request.GET.get('next'))
        return redirect('editprofile')
    def vieworders(request):
        res = {}
        res['products'] = OrderPlaced.objects.filter(user=request.user.id).order_by('-order_date')
        return render(request,'userproduct.html',res)
    def editprofile(request):
        res={}
        ins = Customer.objects.filter(user=request.user.id)
        ins = ins[0] if ins.exists() else None
        print(ins)
        res['form1'] = CustomeruserForm(instance = request.user)
        if  profile.objects.filter(user=request.user.id).exists():
            res['form'] = CustomerProfileForm(instance=profile.objects.filter(user=request.user.id)[0])
        else:
            res['form'] = CustomerProfileForm(initial={'user':request.user})
        return render(request,'usereditprofile.html',res)
    def editpass(request):
        res = {}
        if request.method == 'POST':
            opass = request.POST.get('old_password')
            password = request.POST.get('password')
            password_confirmation = request.POST.get('password_confirmation')
            user = authenticate(username=request.user.username, password=opass)
            print(user)
            if password == password_confirmation and password is not None and user is not None:
                user = User.objects.get(id= request.user.id)
                user.set_password(password)
                user.save()
                user = authenticate(username=request.user.username, password=password)
                login(request,user)
                messages.success(request,"Your password is changed Successfully")
                return redirect('editpass')
            if password != password_confirmation:
                messages.error(request,"Password and confirm password is not Matched")
            if user is None:
                messages.error(request,"Please cheack your password!")
            return redirect('editpass')
            
        return render(request,'userchangepass.html',res)
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'address.html',{'add':add})

# class ProfileView(View):
#     def get(self, request):
#         pass


def logout(request):
    auth.logout(request)
    messages.success(request, "successfully logged out")
    return redirect('index')
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        if Cart.objects.filter(user=user.id,product=product).exists():
            return addcart(request,product)
        Cart(user=user, product=product).save()
        return redirect('/cart')
    else:
        messages.success(request, "Login Required")
        return redirect('userlogin')

def showcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount += tempamount
            totalamount = amount + shipping_amount

            return render(request,'Cart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'emptycart.html')
    


def checkout(request):
    if request.method == "POST":
        return paymentdone(request)
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 0.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
        totalamount = amount + shipping_amount
    res = {}
    res['form1'] = CustomeruserForm(instance = request.user)
    if  profile.objects.filter(user=request.user.id).exists():
        res['form'] = CustomerProfileForm(instance=profile.objects.filter(user=request.user.id)[0])
    else:
        res['form'] = CustomerProfileForm(initial={'user':request.user})
    return render(request,'checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'form':res['form'],'form1':res['form1']})

def paymentdone(request):
    user=request.user
    if request.method == "POST":
        custid = request.user.email
        customer = request.user.id
        cart = Cart.objects.filter(user=user)
        email =request.POST.get('email')
        first_name =request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        state =request.POST.get('state')
        city =request.POST.get('city')
        address =request.POST.get('address')
        zip =request.POST.get('zip')
        total = 0
        for c in cart:
            order = OrderPlaced.objects.create(user=user, product=c.product, quantity=c.quantity,price=c.product.price)
            total+= (c.product.price * c.quantity)
            order.save()
            orderaddress(order = order,first_name=first_name,last_name=last_name,state=state,city=city,address=address,zip=zip).save()
            c.delete()
        param_dict={

            'MID': 'TaFiEU45447912471030',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(total),
            'CUST_ID': custid,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'DEFAULT',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://'+request.get_host()+'/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generateSignature(param_dict, MERCHANT_KEY)
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return  render(request, 'paytm/paytm.html', {'param_dict': param_dict})
    return render(request,'Cart.html')
    
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verifySignature(response_dict, MERCHANT_KEY, checksum)
    if verify:
        orderob = OrderPlaced.objects.get(order_id=response_dict['ORDERID'])
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            orderob.status = "Accepted"
            orderob.save()
        else:
            orderob.status = "Cancel"
            orderob.save()
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paytm/paymentstatus.html', {'response': response_dict})
    

def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request,'orders.html',{'order_placed':op})

def productdetails(request,id):
    products = Product.objects.get(pk=id)
    spec = specs.objects.filter(Product=products.id)
    return render(request,'ProductDetails.html',{'escooter':products,'specs':spec})

def h5(request):
    return render(request,'h5.html')
    
def base(request):
    return render(request,'base.html')
    
def getproddetails(request):
    id = request.GET.get('id')
    data = Product.objects.get(id = id).__dict__
    del data['_state']
    print(data)
    data = json.dumps(data)
    return HttpResponse(data)
def deletecart(request,id):
    citem = Cart.objects.filter(user = request.user.id,product=id)[0].delete()
    return redirect('cart')
def addcart(request,id):
    citem = Cart.objects.filter(user = request.user.id,product=id)[0]
    citem.quantity = citem.quantity + 1
    citem.save()
    return redirect('cart')
def minuscart(request,id):
    citem = Cart.objects.filter(user = request.user.id,product=id)[0]
    if citem.quantity == 1:
        #   citem.delete()
        return redirect("cart")
    citem.quantity = citem.quantity - 1
    citem.save()
    return redirect('cart')
@login_required(login_url="userlogin")
def buynow(request,id):
    prod = Product.objects.filter(id=id)
    if request.method=="POST":
        email =request.POST.get('email')
        first_name =request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        state =request.POST.get('state')
        city =request.POST.get('city')
        address =request.POST.get('address')
        zip =request.POST.get('zip')
        order = OrderPlaced.objects.create(user=request.user, product=prod[0], quantity=1,price=prod[0].price)
        orderaddress(order = order,first_name=first_name,last_name=last_name,state=state,city=city,address=address,zip=zip).save()
        total = (prod[0].price * 1)
        order.save()
        param_dict={
            'MID': 'TaFiEU45447912471030',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(total),
            'CUST_ID': request.user.email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'DEFAULT',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://'+request.get_host()+'/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generateSignature(param_dict, MERCHANT_KEY)
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return  render(request, 'paytm/paytm.html', {'param_dict': param_dict})
    add = Customer.objects.filter(user=request.user)
    res = {}
    res['form1'] = CustomeruserForm(instance = request.user)
    if  profile.objects.filter(user=request.user.id).exists():
        res['form'] = CustomerProfileForm(instance=profile.objects.filter(user=request.user.id)[0])
    else:
        res['form'] = CustomerProfileForm(initial={'user':request.user})
    return render(request,'checkout.html',{'cartitems':prod,'totalamount':prod[0].price,'add':add,'buynow':True,'form':res['form'],'form1':res['form1']})
    