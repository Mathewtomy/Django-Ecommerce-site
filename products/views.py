from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Contact,About,Category,Customer,Order,Return,Product_option_description,Blog,Banner,Product_Category,CartItem
from .forms import MyForm
from .forms import ContactusForm
from .returns import ReturnForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import make_password
from django.views import View
from django.db.models import Sum
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa  
import razorpay
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib.sessions.models import Session
from datetime import datetime
import uuid
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
# from payment_integration.config.settings.django import (
#     RAZORPAY_KEY_ID,
#     RAZORPAY_KEY_SECRET,
# )
from .constants import PaymentStatus
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

# def index(request):
#     # return HttpResponse("welcome to product page")
#     products=Product.objects.all()
#     return render(request,'index.html',{'products':products})



def details(request):
    return HttpResponse("welcome to details page")   
def contact(request):
    sub = ContactusForm
    if request.method == 'POST':
        sub = ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            
    return render(request, 'contact.html', {'form':sub})

    # return HttpResponse("welcome to product page")
    # contacts=Contact.objects.all()
    # return render(request,'contact.html',{'contactz':contacts})
def about(request):
    
    about=About.objects.all()
    return render(request,'about.html',{'about':about})

def blog(request):
    
    blog=Blog.objects.all()
    categories = Category.objects.all()
    products = Product.objects.filter(status=2)
    data = {}
 
    data['blog'] = blog  
    data['categories'] = categories
    data['products'] = products 
   
    
    
    return render(request,'blog.html',data)
    
def product(request):
    
    blog=Blog.objects.all()
    categories = Category.objects.all()
    products = Product.objects.filter(Q(status=2))[:4]
    banner=Banner.objects.all()
    status=Product_Category.objects.all()
    allproduct = Product.objects.all()[:16]
    dress = Product.objects.filter(Q(category=2))[:1]
    sunglass = Product.objects.filter(Q(category=3))[:1]
    bag = Product.objects.filter(Q(category=4))[:1]
    footwear= Product.objects.filter(Q(category=5))[:1]
    watch = Product.objects.filter(Q(category=1))[:1]
    
    data = {}
 
    data['blog'] = blog  
    data['categories'] = categories
    data['products'] = products 
    data['banner'] = banner
    data['allproduct'] =  allproduct
    data['dress'] = dress
    data['sunglass'] = sunglass
    data['bag'] = bag
    data['footwear'] = footwear
    data['watch'] = watch
    data['status'] = status
    return render(request,'product.html',data)

def signup(request):
  if request.method == "POST":
    form = MyForm(request.POST)
    if form.is_valid():
      form.save()
  else:
      form = MyForm()
  return render(request, 'signup.html',{'form':form})

def retrieve(request):
    details=Product.objects.all()
    return render(request,'retrieve.html',{'details':details})

def edit(request,slug):
    
    object=Product.objects.get(slug=slug)
    return render(request,'edit.html',{'object':object})
def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    object=Product.objects.get(name=query)
  
    return render(request,'view.html',{'object':object})
  

    # word variable will be shown in html when user click on search button
   
def view(request,slug):
    
    object=Product.objects.get(slug=slug)
  
    return render(request,'view.html',{'object':object})



def customer_address_view(request):
        session_key = request.session.session_key
        try:
            session = Session.objects.get(session_key=session_key)
        except Session.DoesNotExist:
            session_key = str(uuid.uuid4())
            session = Session.objects.create(session_key=session_key, expire_date=datetime.now())
            
     
        customer = request.session.get('customer')
       
        if customer:
            cart_items = CartItem.objects.filter(customer=customer)
           
                
            return render(request,'checkout.html',{'products':cart_items})   
          
        else:
            cart_items = CartItem.objects.filter(session=session)
            return render(request,'checkout.html',{'products':cart_items})  
     
def update(request, id):
    instances=Product.objects.get(id=id)
    form=MyForm(request.POST or None, instance=instances)
    if form.is_valid():
        form.save()
        instance=Product.objects.all()
        return HttpResponseRedirect(reverse('retrieve'))
    
class Cart(View):
    def get(self , request):
        
        session_key = request.session.session_key
        try:
            session = Session.objects.get(session_key=session_key)
        except Session.DoesNotExist:
            session_key = str(uuid.uuid4())
            session = Session.objects.create(session_key=session_key, expire_date=datetime.now())
            
        
        customer = request.session.get('customer')
       
        if customer:
            cart_items = CartItem.objects.filter(customer=customer)
           
            cart_total = 0
            product_totals = []
            for item in cart_items:
                
                item_total = item.quantity * item.product.price
                product_totals.append(item_total)
                cart_total += item_total
                
                
            return render(request, "cart.html", {'products': cart_items, 'cart_total': cart_total})
        else:
            cart_items = CartItem.objects.filter(session=session)
            cart_total = 0
            product_totals = []
            for item in cart_items:
                product_total = item.product.price * item.quantity
                product_totals.append(product_total)
                cart_total += item.total()
                
            return render(request, "cart.html", {'products': cart_items, 'cart_total': cart_total})
            
       
        
class Account(View):
    def get(self , request):
        customers = request.session.get('customer')
        
        customer=Customer.objects.get(id=customers)
       
        return render(request,'account.html',{'customer':customer})
      
def Accountupdate(request):
     if request.method == ('POST'):
         customers = request.session.get('customer')
         customer=Customer.objects.get(id=customers)
        #  form=MyForm(request.POST or None, instance=customer)
         postData = request.POST
         first_name = postData.get ('firstname')
         last_name = postData.get ('lastname')
         phone = postData.get ('phone')
         email = postData.get ('email')
        #  password = postData.get ('password')
         update=Customer.objects.filter(id=customers).update(first_name=first_name,last_name=last_name,phone=phone,email=email)
        #  update.save()
         return HttpResponseRedirect('account')
        #  if form.is_valid():
        #      form.save()
        #  else:
        #      form = MyForm()
        # return HttpResponseRedirect('account')
      
             
        
class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        
        session_key = request.session.session_key
        try:
            session = Session.objects.get(session_key=session_key)
        except Session.DoesNotExist:
            session_key = str(uuid.uuid4())
            session = Session.objects.create(session_key=session_key, expire_date=datetime.now())
            
        if customer:
            cart_item = CartItem.objects.filter(customer=customer)
            cart_items = CartItem.objects.filter(customer=customer).values('product')
            product_ids = [item['product'] for item in cart_items]
            
            for item in cart_item:
                quantity=item.quantity
                product = Product.objects.get(id=item.product.id)
                
                order = Order(customer=Customer(id=customer),
                              product=product,
                              price=product.price,
                              address=address,
                              phone=phone,
                              quantity=quantity)
                
                 # reduce tyre stock quantity
                total_product = Product.objects.get(id=order.product.id)
                total_product.stock = product.stock - order.quantity
                
                total_product.save()
                order.save()
            
            order_id = Order.objects.latest('id')
            
            CartItem.objects.filter(customer=customer).delete()
            
            # product_id=Product.objects.get(id=total_product.id)
            # print(total_product.id)
            # product_name=product_id.name
         
           
            # customers=Customer.objects.get(id=customer) 
            # first_name=customers.first_name
            # email=customers.email
            
            # subject = 'Thank you for registering to our site'
            # message = ' it  means a world to us - your order id is '
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [email]
            # send_mail( subject, message, email_from, recipient_list )
           

    
            # message = "your item  sucesfully ordered"
            
            # message = EmailMessage(
            # "Subject",
            #  "Some body."
            # "mtomy1@yahoo.com",
            # [email],
            # )
            # message.attach("document.pdf", pdf_file.read())
            # message.send(fail_silently=False) 
            
            request.session['cart'] = {}
        
            messages.success(request, 'successfully completed your order.')
            return redirect('cart')
    
class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print (email, password)
        return render (request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
       
        paginator =Paginator(orders, 3)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)  
        except PageNotAnInteger:
            page_obj = paginator.page(1)
            
       
        
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        
        context = {'page_obj': page_obj}
        return render(request,'orders.html',context)
        
        # return render(request,'orders.html',{'orders':orders})
        
       

class Register (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        
        error_message = self.validateCustomer (customer)

        if not error_message:
            print (first_name, last_name, phone, email, password)
            customer.password = make_password (customer.password)
            customer.register ()
            return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
class Cartview(View):


    def post(self , request):
        product = request.POST.get('product')
        products=Product.objects.filter(id=product).aggregate(
            total=Sum('stock')
            )['total']
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            
            if cart[product] < products:
                
                if quantity>=1:
                 cart[product]  = quantity+1
                   
            else:
                   cart[product] = quantity
            
                
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
  
        return redirect('cart')    


def cart_items(request):
    cart_items = CartItem.objects.filter(cart_id=request.session.get("cart_id"))
    return {'cart_items': cart_items}


class Index(View):
    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        session_key = request.session.session_key
        
        try:
            session = Session.objects.get(session_key=session_key)
        except Session.DoesNotExist:
            session_key = str(uuid.uuid4())
            session = Session.objects.create(session_key=session_key, expire_date=datetime.now())

        cart_item = CartItem.objects.filter(session=session, product=product_id)

        customer = request.session.get('customer')
        product = Product.objects.get(id=product_id)
        if customer:
            customer = Customer.objects.get(id=customer)
        else:
            customer = Customer.objects.get(id=1)

        total_stock = Product.objects.filter(id=product_id).aggregate(
            total=Sum('stock')
        )['total']

        if cart_item.exists():
            quantity = cart_item.first().quantity
            if remove:
                if quantity <= 1:
                    cart_item.delete()
                else:
                    cart_item.update(quantity=quantity - 1)
            else:
                if quantity >= total_stock:
                    messages.success(request, 'Quantity value not be greater than product quantity.')
                else:
                    cart_item.update(quantity=quantity + 1)
        else:
            quantity=1
            if quantity >= total_stock:
                    messages.success(request, 'Quantity value not be greater than product quantity.')
            else:
                CartItem.objects.create(
                customer=customer,
                product=product,
                session=session,
                quantity=1
            )
        request.session['cart'] = cart
        return redirect('homepage')
    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')
    


    
def store(request):
    # item_ids = request.session.get('cart', [])
    # items = CartItem.objects.filter(id__in=item_ids)
   
    # if not cart:
    #     request.session['cart'] = {}
    products = None
    categories = Category.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.objects.all();
        
    default_page = 1
    page = request.GET.get('page', default_page)
    items_per_page = 9
    paginator = Paginator(products, items_per_page)
    try:
        items_page = paginator.page(page)  
    except PageNotAnInteger:
        
        items_page = paginator.page(default_page)
            
    except EmptyPage:
        
        items_page = paginator.page(paginator.num_pages)

    table_1 = Product.objects.values_list('id', flat=True)
   
    products_option=Product_option_description.objects.filter(product_option=2)
      
    customer_id = request.session.get('customer')
    cart_length = 0
    session_key = request.session.session_key
    try:
        
        session = Session.objects.get(session_key=session_key)
            
            
    except Session.DoesNotExist:
        
        session_key = str(uuid.uuid4())
        session = Session.objects.create(session_key=session_key, expire_date=datetime.now())
        
    if customer_id:
        # If a customer id is present, get the customer and their carts
        
        customer = Customer.objects.get(id=customer_id)
       
        carts = CartItem.objects.filter(customer=customer)
        
        CartItem.objects.filter(session=session).update(customer=customer)
        cart_length = carts.count()
        
    else:
        
       
        carts=CartItem.objects.filter(session=session)
        
        cart_length = carts.count()
    
        # Create a dictionary to store the count of each product in the cart
    product_counts = {}
    for cart_item in carts:
        
        
        
    # Increment the count of each product in the cart
       product_id = cart_item.product.id
       quantity=cart_item.quantity
       if product_id in product_counts:
     
           product_counts[product_id] += quantity
       else:
           product_counts[product_id] = quantity
        
    cart_items_text = ', '.join([f"{value}" for key, value in product_counts.items()])
  
    
    cart_text = f"{cart_items_text} IN CART" 
    
    cart_items = ', '.join([f"{key}" for key, value in product_counts.items()])

    cart_texts = f"{cart_items} IN CART" 

    
    data = {}
    data['all_img'] = Product.objects.all().distinct()   
    data['products'] = items_page  
    data['categories'] = categories
    data['option']= products_option
    data['carts']=carts
    data['cart_length']=cart_length
    data['cart_text']=cart_text
    data['product_counts'] = product_counts

 
    
    print('you are : ', request.session.get('email'))
    
    return render(request,'index.html',data)
    
  

class ReturnView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        returns = Return.get_return_by_customer(customer)
        paginator =Paginator(returns, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            page_obj = paginator.page(1)
            
        # if page_number is not an integer then assign the first page
        
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        # if page is empty then return last page
        
        context = {'page_obj': page_obj}
        
        # print(returns)
        
        # return render(request,'returns.html',{'returns':returns})
        return render(request,'returns.html',context)
 
    
def Addreturn(request,id):
    
    # quantity = None
    object=Order.objects.get(id=id)
    order = Order.objects.filter(id=id)
    if order:
        quantity=Order.objects.filter(id=id).aggregate(
            total=Sum('quantity')
            )['total'] 
    else:
        quantity=0
        
    returns = Return.objects.filter(order=id)
    if returns:
        qty=  Return.objects.filter(order=id).aggregate(
            total=Sum('quantity')
            )['total'] or Decimal()
        
    else:
        qty = 0
    data = {}
    data['qty'] = qty
    data['quantity'] = quantity
    
    if (qty == quantity):
        return redirect('homepage')
        
 
        
    return render(request,'add-return.html',{'object':object})

def Updatereturn(request, id):
    object=Order.objects.get(id=id)
    Orders = Order.objects.filter(id=id).values_list('id')
    quantity = request.POST.get('quantity')
    reason = request.POST.get('reason')
    
    customer = request.session.get('customer')
    
    products=Order.objects.filter(id=id).aggregate(
            total=Sum('product')
            )['total']
    
    returns = Return.objects.filter(order=id)
    if returns:
        qty=  Return.objects.filter(order=id).aggregate(
            total=Sum('quantity')
            )['total'] or Decimal()
        
    else:
        qty = 1
    # products = Order.objects.filter(id=id).values_list('product', flat=True)
    
    print(quantity, customer,products,Orders)
    order = Return(customer=Customer(id=customer),
                          product=Product(id=products),
                          
                          order=Order(id=Orders),
                          reason=reason,
                          quantity=quantity )
    
    if (int(quantity) > int(qty)):
    #    return redirect(request,'add-return',{'object':object})
       messages.success(request, 'Quantity value should not  be Greater than Return Quantity.')
       return redirect('orders')
        # raise ValidationError(
        #     "Quantity value should not  be Greater than Return Quantity"
        #     )
    
    products=Order.objects.filter(id=id).values_list('product', flat=True)
    pr=list(products)
    ids=pr
    # print(pr)
    
    filters = {}
    
    for value in pr:
        filters[''] = value
    # print(value)
   
        
    stock =Product.objects.filter(id=value).aggregate(
            total=Sum('stock')
            )['total']
    # quantity=Order.objects.filter(id=id).aggregate(
    #         total=Sum('quantity')
    #         )['total']
    # print (quantity)
   
    total= int(stock) + int(quantity)
    total_product = Product.objects.filter(id=value).update(stock=total)
  
    order.save()
    messages.success(request, 'Return successfully updated.')
    return redirect('orders')




def Addcancel(request,id):
    
    products=Order.objects.filter(id=id).values_list('product', flat=True)
    pr=list(products)
    ids=pr
    # print(pr)
    
    filters = {}
    
    for value in pr:
        filters[''] = value
    # print(value)
   
        
    stock =Product.objects.filter(id=value).aggregate(
            total=Sum('stock')
            )['total']
    quantity=Order.objects.filter(id=id).aggregate(
            total=Sum('quantity')
            )['total']
    # print (quantity)
   
    total= int(stock) + int(quantity)
    total_product = Product.objects.filter(id=value).update(stock=total)
        
    Order.objects.filter(id=id).delete()
                

      
               
    
    messages.success(request, 'successfully canceled your order.')
    return redirect('orders')
    # return render(request,'carts.html',{'products':pr})
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    # pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)

def download_invoice_view(request,orderID,productID):
    order=Order.objects.get(id=orderID)
    product=Product.objects.get(id=productID)
        
    customer=Order.objects.filter(id=orderID).values_list('customer', flat=True)
    pr=list(customer)
    ids=pr
    # print(pr)
    
    filters = {}
    
    for value in pr:
        filters[''] = value
    
    customers=Customer.objects.get(id=value)
    mydict={
        'orderid':order.date,
        'orderDate':order.date,
        'customerName':customers.first_name,
        'customerEmail':customers.email,
        'customerMobile':customers.phone,
        'shipmentAddress':order.address,
        'orderStatus':order.status,

        'productName':product.name,
        'productImage':product.image,
        'productPrice':product.price,
        'productDescription':product.description,
        # 'productDescription':product.description,


    }
    return render_to_pdf('download_invoice.html',mydict)

def is_ajax(request):
    return request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def search_auto(request):
   if is_ajax(request):    
    q = request.GET('term')
    
    
    
    
    products = Product.objects.filter(name=q)    
    results = []
    for pr in products:
      product_json = {}
      product_json.label = pr.name
      product_json.value = pr.name
      product_json.image = pr.image
      results.append(product_json)
    data = json.dumps(results)
   else:
       
    data = 'fail'
   mimetype = 'application/json'
   return HttpResponse(data, mimetype)


def view_to_add_item_to_cart(request, id):
    product = request.POST.get('product')
    remove = request.POST.get('remove')
    cart = request.session.get('cart')
        
    products=Product.objects.filter(id=product).aggregate(
            total=Sum('stock')
            )['total']
    
    if cart:
        
        quantity = cart.get(product)
        if quantity:
            
            if remove:
                
                if quantity<=1:
                    
                    cart.pop(product)
                else:
                    
                    cart[product]  = quantity-1
            else:
                
                if cart[product] > products-1:
                    
                    messages.success(request, 'Quantity value not  be Greater than Product Quantity.')
                else:
                    
                    cart[product]  = quantity+1

        else:
                cart[product] = 1
    else:
        
        cart = {}
        cart[product] = 1

        request.session['cart'] = cart
    
    products = Product.objects.get(id=id)
    
    customer = request.session.get('customer')
    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
   
    if customer:
        customers = Customer(id=customer)
    else:
        customers=Customer(1)
    
    cart_item, created = CartItem.objects.get_or_create(
    customer=customers,
    product=products,
    session=session,
    defaults={'quantity': 1}
)

    if not created:
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
        
    
    return redirect('homepage')


def Remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



def update_cart(request, cart_item_id, quantity):
    
    if request.POST.get('increment'):
         quantity += 1
    elif request.POST.get('decrement'):
        quantity -= 1
    decrement = request.POST.get('decrement')
    
    cart_item = CartItem.objects.get(id=cart_item_id)
    product_id = request.POST.get('product_id')
    
    total_stock = Product.objects.filter(id=product_id).aggregate(
            total=Sum('stock')
        )['total']
    
    if decrement:
        if quantity < 1:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
    else:
        
        if quantity >= total_stock:
            
            messages.success(request, 'Quantity value not be greater than product quantity.')
        else:
            
            cart_item.quantity = quantity
        
    
    
    cart_item.save()
    return redirect('cart')
# def update_cart(request, cart_item_id, quantity):
    
#     if request.POST.get('increment'):
#          quantity += 1
#     elif request.POST.get('decrement'):
#         if quantity > 1:
#             quantity -= 1
#         elif quantity == 2:
#             quantity -= 1
#         else:
#             messages.success(request, 'Quantity cannot be less than 1.')
#     decrement = request.POST.get('decrement')
    
#     cart_item = CartItem.objects.get(id=cart_item_id)
#     product_id = request.POST.get('product_id')
    
#     total_stock = Product.objects.filter(id=product_id).aggregate(
#             total=Sum('stock')
#         )['total']
    
#     if decrement:
#         if quantity <= 1:
#             cart_item.delete()
#         else:
#             cart_item.quantity = quantity
#     else:
        
#         if quantity >= total_stock:
            
#             messages.success(request, 'Quantity value not be greater than product quantity.')
#         else:
            
#             cart_item.quantity = quantity
        
    
    
#     cart_item.save()
#     return redirect('cart')