from django.contrib.auth.models import User
from onlineshop.models import contactinfo,Product,TestDrive,Contact,OrderPlaced
def alltimefunc(request):
    res = {}
    res['info'] = contactinfo.objects.all() 
    res['allprods'] = Product.objects.all()
    res['allbookings'] = TestDrive.objects.all()
    res['allContact'] = Contact.objects.all()
    res['allorders'] = OrderPlaced.objects.all()
    res['allusers'] = User.objects.all()
    return res
