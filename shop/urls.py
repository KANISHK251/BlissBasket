from django.urls import path

from .import views


urlpatterns = [
    path("", views.login_view, name = "login"),
    path("shop", views.shop, name = "shop"),  #/shop goes to views 
    path("contact", views.contact,name = "contact"),
    path("contacts", views.contacts,name = "contacts"),
    path("checkout", views.checkout,name = "checkout"),
    path("cart",views.cart,name="cart"),
    path("logout", views.logout_view,name = "logout"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('buy_now/<int:product_id>/', views.buy_now, name="buy_now"),
    path('remove_cart/<int:product_id>/',views.remove_cart,name="remove_cart"),
    path('delete_cart/<int:product_id>/',views.delete_cart,name="delete_cart"),
    path('remove_product/<int:product_id>/',views.remove_product, name="remove_product"),
    path('add_product/<int:product_id>/',views.add_product,name="add_product"),
    path('buy_decrease/<int:product_id>/',views.buy_decrease,name="buy_decrease"),
    path('payment_success',views.payment_success,name="payment_success"),
    
]

