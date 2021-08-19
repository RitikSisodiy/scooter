from django.urls import path, include
from .import views
urlpatterns = [
    path('',views.index, name="dashboardindex"),
    path('product',views.allproducts, name="allproducts"),
    path('product/addspecfication/<int:id>',views.addspecs, name="addspecs"),
    path('product/updatespecfication/<int:id>',views.updatespecs, name="updatespecs"),
    path('product/deletespecfication/<int:id>',views.deletespecs, name="deletespecs"),
]