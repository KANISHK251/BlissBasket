from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.urls import reverse
from .models import Product,Cart,CartItem,Contact
from  math import ceil


# Create your views here.
 
def index(request):
    return render(request, 'shop/index.html')


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


def cart(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.product.price*item.quantity for item in items)

    context = {'cart_items': items,'total': total}
    return render(request,'shop/cart.html', context)



def remove_cart(request,product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem,cart=cart,product=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def delete_cart(request,product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem,cart=cart,product=product_id)
    cart_item.delete()

    return redirect('cart')


def contact(request):
    return render(request,"shop/contact.html")


def contacts(request):
    name = request.POST.get('name','')
    email = request.POST.get('email','')
    phone = request.POST.get('phone','')
    desc = request.POST.get('desc','')
    contact = Contact(name=name,email=email,phone=phone,desc=desc)
    print(contact)
    contact.save()
    return HttpResponse('''Contact details added successfully 
                        <br><a href="{}" class="btn btn-primary mt-3" role="button">Continue Shopping</a>
                        '''.format(reverse('shop')))

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

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
    return redirect('login')

        


def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    total = sum(item.product.price*item.quantity for item in items)
    context = {'cart_items' : items, 'total':total}
    return render(request,"shop/checkout.html",context)


def buy_decrease(request,product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.get(product=product_id, cart=cart)
    total = cart_item.product.price*cart_item.quantity
    context = {'cart_items' : [cart_item], 'total' : total}
    return render(request,"shop/buy_now.html",context)

  

def buy_now(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_item,item_created = CartItem.objects.get_or_create(product=product,cart=cart)
    total = cart_item.product.price*cart_item.quantity
    context = {'cart_items' : [cart_item] ,'total' : total}
    return render(request, "shop/buy_now.html",context)



def add_product(request,product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(product=product_id, cart=cart)

    if item_created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('buy_decrease',product_id=product_id)


def remove_product(request,product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.quantity=1

    return redirect('buy_decrease',product_id=product_id)






def tracker(request):
    return HttpResponse("We are at tracker page")

def search(request):
    return HttpResponse("We are at search page")

def prodView(request):
    return HttpResponse("We are at productView page")







