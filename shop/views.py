from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
from django.http import HttpResponse
from django.urls import reverse
from .models import Product,Cart,CartItem,Contact,Order
from  math import ceil


# Create your views here.
 
def index(request):
    return render(request, 'shop/index.html')


@login_required
def shop(request):
    categories = ["Men's Fashion","Electronics","Kid's Fashion"]
    context = []
    for category in categories:
        products = Product.objects.filter(category = category)  #retrive all products from the database
        n = len(products)
        nslides = n//4 + ceil((n/4)-(n//4))
        context.append({
            'category' : category,
            'range': range(1,nslides), 
            'product': products })
    allprod = {"context": context}
    return render(request,'shop/shop.html',allprod)


@login_required
def add_to_cart(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_item,item_created = CartItem.objects.get_or_create(product=product,cart=cart)

    if  item_created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
        
    return redirect('cart')

@login_required
def cart(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.product.price*item.quantity for item in items)

    context = {'cart_items': items,'total': total}
    return render(request,'shop/cart.html', context)


@login_required
def remove_cart(request,product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem,cart=cart,product=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required
def delete_cart(request,product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem,cart=cart,product=product_id)
    cart_item.delete()

    return redirect('cart')

@login_required
def contact(request):
    return render(request,"shop/contact.html")

@login_required
def contacts(request):
    name = request.POST.get('name','')
    email = request.POST.get('email','')
    phone = request.POST.get('phone','')
    desc = request.POST.get('desc','')
    contact = Contact(name=name,email=email,phone=phone,desc=desc)
    contact.save()
    return HttpResponse('''Contact details added successfully 
                        <br><a href="{}" class="btn btn-primary mt-3" role="button">Continue Shopping</a>
                        '''.format(reverse('shop')))

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Attempting to authenticate user with email: {email}")

        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request, user, backend="shop.backends.EmailBackend")
            return redirect('shop')

        else:
            if User.objects.filter(email=email).exists():
                return render(request, 'shop/login.html', {'error': 'Invalid Credentials'})
            user=User.objects.create(
                email=email,
                username = email.split('@')[0],
                password=make_password(password),  
                )
            login(request, user, backend="shop.backends.EmailBackend")
            return redirect('shop')
                     
    return render(request,'shop/login.html')



def logout_view(request):
    logout(request)
    return redirect('/')

        

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    total = sum(item.product.price*item.quantity for item in items)
    context = {'cart_items' : items, 'total':total}
    return render(request,"shop/checkout.html",context)


@login_required
def buy_decrease(request,product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.get(product=product_id, cart=cart)
    total = cart_item.product.price*cart_item.quantity
    context = {'cart_items' : [cart_item], 'total' : total}
    return render(request,"shop/buy_now.html",context)

  
@login_required
def buy_now(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_item,item_created = CartItem.objects.get_or_create(product=product,cart=cart)
    total = cart_item.product.price*cart_item.quantity
    context = {'cart_items' : [cart_item] ,'total' : total}
    return render(request, "shop/buy_now.html",context)


@login_required
def add_product(request,product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(product=product_id, cart=cart)

    if item_created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('buy_decrease',product_id=product_id)

@login_required
def remove_product(request,product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.quantity=1

    return redirect('buy_decrease',product_id=product_id)


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        phone = request.POST.get('phone')
        total = request.POST.get('total')

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        #We convert the amount in paisa format as per Razorpay standard
        amount = int(float(total)*100)

        razorpay_order = client.order.create({'amount':amount, 'currency': 'INR', 'payment_capture': '1'})

        #Now we save the save order details in the database
        order = Order.objects.create(
            name=name,
            email=email,
            address=address,
            address2=address2,
            city=city,
            state=state,
            zip_code=zipcode,
            phone=phone,
            razorpay_orderid = razorpay_order['id']
        )
        order.save()


        #Now we pass the order and Razorpay details to the frontend
        context = {
            'order' : order,
            'razorpay_orderid' : razorpay_order['id'],
            'razorpay_merchant_key': settings.RAZORPAY_API_KEY,
            'total_amount': amount,
            'currency': 'INR',
            }
        return render(request,'shop/payment_success.html',context)
    
    return render(request,'shop/checkout.html')



@csrf_exempt
def payment_verify(request):
    if request.method == "POST":
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)) 

        #Now we fetch the payment details from the razorpay/request
        razorpay_orderid = request.POST.get('razorpay_order_id')
        razorpay_paymentid = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        #We verify the payment siganture

        params_dict = {
            'razorpay_orderid' : razorpay_orderid,
            'razorpay_paymentid' : razorpay_paymentid,
            'razorpay_signature' : razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(razorpay_orderid=razorpay_orderid)
            order.razorpay_paymentid = razorpay_paymentid
            order.status='Paid'
            order.save()
            return HttpResponse('Payment is successfull and Your order details are',{order})
        except:
            return HttpResponse('payment is unsuccessful')
        
    return redirect('shop')









