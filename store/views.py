from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View

from .models.product import Product
from .models.category import Category
from .models.customer import Customer

# Create your views here.

def home(request):
    products = None
    category = Category.get_all_categories()
   
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_product_by_category_id(categoryID)

    else:
        products = Product.get_all_products()


    data = {}
    data['product'] = products
    data['category'] = category
    return render(request, 'home.html',data)
       

class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')
    

    def post(self,request):

        postData = request.POST
        name = postData.get('name')
        phone = postData.get('phone')


        error_message = None

        value = {
            'phone':phone,
            'name':name
        }
        

        customer = Customer(name=name,
                            phone=phone)
        
        if(not name):
            error_message = "Name is Required"

        elif not phone:
            error_message = "Mobile Number is Required"

        elif len(phone) < 11:
            error_message = "Mobile Number Must be 11 Digits"

        elif customer.isExists():
            error_message = "Mobile Number Already Exists"

        if not error_message:
            messages.success(request,'Congratulation !! Successfully Registered ')

            customer.register()
            return redirect('signup')

        else:
            data = {
                'error':error_message,
                'value':value
            }
            return render(request, 'signup.html', data)


        
    


class Login(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        phone = request.POST.get('phone')
        error_message = None
        value ={
            'phone':phone
        }
        customer = Customer.objects.filter(phone=request.POST["phone"])
        if customer:
            return redirect('homepage')
        else:
            error_message = "Mobile Number is Invalid!!"
            data ={
                'error':error_message,
                'value':value
            }

        return render(request,'login.html',data)


def productdetail(request,id):
    product = Product.objects.get(id= id)
    return render(request,'productdetail.html', {'product':product})

