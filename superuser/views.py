from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.apps import apps
from onlineshop.models import *
from django.contrib import messages
from .forms import ProductForm,aboutForm,about,GenForm
# Create your views here.
#add all app names you want to oprate in admin
allapps = ['onlineshop',]
def index(request):
    res = {}
    # for app in allapps:
    #     res.append({app:apps.all_models[app]})
    res['latestorders'] = OrderPlaced.objects.all().order_by('-order_date')
    return render(request,'superuser/index.html',res)
def allproducts(request):
    prods = Product.objects.all()
    return render(request,'superuser/products.html',{'prods':prods,'title':"View Product"})
def editproduct(request,id=None,task=None):
    res = {}
    if task == 'add':
        res['form'] = ProductForm()
        instan = None
    if task == 'edit':
        instan = Product.objects.get(id=id)
        res['form'] = ProductForm(instance=instan)
    if request.method == "POST":
        res['form'] = ProductForm(request.POST,request.FILES,instance=instan)
        if res['form'].is_valid():
            res['form'].save()
            messages.success(request,"Prouduct is added successfully :)")
        return render(request,'superuser/addprod.html',res)
    if task == 'del':
        return delproduct(request,id)
    return render(request,'superuser/addprod.html',res)


def delproduct(request,id=None):
    if id is not None:
        Product.objects.get(id=id).delete()
        return redirect('allproducts')

def addspecs(request,id,update=False,remove = False):
    prod = Product.objects.get(id=id)
    specsob = specs.objects.filter(Product=prod.id)
    if request.method == "POST":
        title = request.POST['title']
        oldtitle = request.POST.get('oldtitle')
        key = request.POST.getlist('key')
        value = request.POST.getlist('value')
        data = {}
        data[title] = [[key[i],value[i]] for i in range(0,len(key))]
        if specsob.exists():                
            specsobnew = specsob[0]
            updata= specsobnew.jsondata()
            if update == False:
                try:
                    a = updata[title]
                    print(a,updata)
                    messages.error(request,title+" is already exist please change the title")
                    return redirect('addspecs',id)
                except Exception as e:
                    pass
            updata[title] = data[title]
            if oldtitle is not None and oldtitle != title:
                updata.pop(oldtitle, None)
            specsobnew.listele = updata
            specsobnew.save()
            redirect('addspecs',id)
        else:
            specs(Product=prod,listele=data).save()
    return render(request, 'superuser/addspecs.html', {'product':prod,"specs":specsob})
def updatespecs(request,id,update=True):
    return addspecs(request,id,update=True)
def deletespecs(request,id,update=True):
    title = request.GET.get('deltitle')
    if title is not None:
        prod = Product.objects.get(id=id)
        specsob = specs.objects.filter(Product=prod.id)
        specsobnew = specsob[0]
        updata= specsobnew.jsondata()
        updata.pop(title, None)
        specsobnew.listele = updata
        specsobnew.save()
    return redirect('addspecs',id)

def About(request):
    res = {}
    ins = about.objects.all()
    ins = ins[0] if ins.exists() else None
    res['form'] = aboutForm(instance=ins)
    if request.method == 'POST':
        res['form'] = aboutForm(request.POST,request.FILES,instance=ins)
        if res['form'].is_valid():
            res['form'].save()
            messages.success(request ,'Changes is successfully saved :)')
    return render(request,'superuser/about.html',res)


def testdrivebooking(request):
    res = {}
    form = GenForm(TestDrive)
    res['form'] = form()
    if request.method == "POST":
        res['form'] = form(request.POST,request.FILES)
        if res['form'].is_valid():
            res['form'].save()
    return render(request,'superuser/testbooking.html',res)
def alltestdrive(request):
    res = {}
    res['testdrives'] = TestDrive.objects.all().order_by('time')
    return render(request,'superuser/alltestdrive.html',res)
def contacts(request):
    res = {}
    res['contacts'] = Contact.objects.all().order_by('time')
    return render(request,'superuser/contacts.html',res)
def addcontact(request):
    res = {}
    form = GenForm(Contact)
    res['form'] = form()
    if request.method == "POST":
        res['form'] = form(request.POST,request.FILES)
        if res['form'].is_valid():
            res['form'].save()
    return render(request,'superuser/addcontact.html',res)
def addinfo(request):
    res = {}
    form = GenForm(contactinfo)
    ins = contactinfo.objects.all()
    ins = ins[0] if ins.exists() else None
    res['form'] = form(instance=ins)
    if request.method == "POST":
        res['form'] = form(request.POST,request.FILES,instance=ins)
        if res['form'].is_valid():
            res['form'].save()
    return render(request,'superuser/addinfo.html',res)
def orders(request,slug=None):
    res = {}
    res['choices'] = STATUS_CHOICE
    if slug is None:
        res['orders'] = OrderPlaced.objects.all().order_by('order_date')
    else:
        res['orders'] = OrderPlaced.objects.filter(status=slug).order_by('order_date')
    return render(request,'superuser/orders.html',res)
def addorders(request,id=None):
    res = {}
    form = GenForm(OrderPlaced)
    ins = OrderPlaced.objects.filter(id=id)
    ins = ins[0] if ins.exists() else None
    res['form'] = form(instance=ins)
    if request.method == "POST":
        res['form'] = form(request.POST,request.FILES,instance=ins)
        if res['form'].is_valid():
            res['form'].save()
    return render(request,'superuser/addorders.html',res)


def users(request,slug=None):
    res={}
    if slug is  None:
        res['users'] = User.objects.all()
    return render(request,'superuser/users.html',res)
