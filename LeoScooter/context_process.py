from onlineshop.models import contactinfo
def alltimefunc(request):
    res = {}
    res['info'] = contactinfo.objects.all() 
    return res
