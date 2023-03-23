from django.urls import path,include
from  .views import *
from django.contrib import admin
#from mpesa.urls import mpesa_urls

urlpatterns = [
    path('home/', home , name='home'),
    path('register/', register, name='register'),
    path('',login_user,name ='login'),
    path('home/billing_info/login/',login_user,name ='login1'),
    path('daraja/stk_push',stk_push_callback,name='stk_push_callback'),
    path('index/', index, name='index'),
    path('home/billing_info/', billing_info, name='billing_info1'),
     path('register/home/billing_info/', billing_info, name='billing_info'),
    path('/billing/', billing, name='billing'),
]