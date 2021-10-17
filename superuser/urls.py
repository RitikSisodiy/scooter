from django.urls import path, include
from .import views
urlpatterns = [
    path('',views.index, name="dashboardindex"),
    path('product',views.allproducts, name="allproducts"),
    path('product/addspecfication/<int:id>',views.addspecs, name="addspecs"),
    path('product/<slug:task>/' , views.editproduct , name="addproduct"),
    path('product/<slug:task>/<int:id>' , views.editproduct , name="editproduct"),
    path('product/delproduct/<int:id>' , views.delproduct , name="delproduct"),
    path('product/updatespecfication/<int:id>',views.updatespecs, name="updatespecs"),
    path('product/deletespecfication/<int:id>',views.deletespecs, name="deletespecs"),
    path('about/', views.About , name='dashboardabout'),
    path('testdrivebooking/', views.alltestdrive , name='alltestdrive'),
    path('addtestdrivebooking/', views.testdrivebooking , name='testdrivebooking'),
    path('addcontact/', views.addcontact , name='addcontact'),
    path('contacts/', views.contacts , name='dashboardcontact'),
    path('addinfo/', views.addinfo , name='addinfo'),
    path('orders/', views.orders , name='allorders'),
    path('orders/<slug:slug>', views.orders , name='catorders'),
    path('addorders/', views.addorders , name='addorders'),
    path('editorders/<int:id>', views.addorders , name='editorders'),
]