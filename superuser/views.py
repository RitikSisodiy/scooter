from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.apps import apps
from onlineshop.models import *
from django.contrib import messages

# Create your views here.
#add all app names you want to oprate in admin
allapps = ['onlineshop',]
def index(request):
    res = []
    # for app in allapps:
    #     res.append({app:apps.all_models[app]})
    return render(request,'superuser/index.html',{'models':res})
def allproducts(request):
    prods = Product.objects.all()
    return render(request,'superuser/products.html',{'prods':prods,'title':"View Product"})
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