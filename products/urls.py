from django.urls import path
from .import views

from .middlewares.auth import auth_middleware
from .views import Cart,Index,store
from .views import Customer
from .views import Category
from .views import Product
from .views import Register
from .views import Login
from .views import logout
from .views import CheckOut
from .views import OrderView
from .views import ReturnView
from .views import Remove_from_cart
from .views import Cartview
# from .views import Pluscartview
# from .views import Minuscartview
from .views import Account
from .views import update_cart
urlpatterns = [
    # path('',views.index,name="index"),
    path('', Index.as_view(), name='homepage'),
        # path('store', store , name='store'),
    path('store',store,name='store'),
    path('contact',views.contact,name="contact"),
    #  path('details',views.details,name="details"),auth_middleware(Cart.as_view())
    # path('cart_products',views.cart_products,name="cart_products"),
    path('about',views.about,name="about"),
    path('blog',views.blog,name="about"),
    path('product',views.product,name="about"),
    
    path('add-cart/<int:id>',views.view_to_add_item_to_cart,name="about"),
    #  path('signup',views.signup,name="signup"),
    #  path('retrieve',views.retrieve,name="retrieve"),
    #  path('edit/<slug:slug>',views.edit,name="edit"),
    #   path('update/<int:id>',views.update,name="update"),
    #   path('register',views.register,name="register"),
    #   path('login',views.login,name="login"),
    #   path('logout',views.logout,name="logout"),
    #   path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    #   path('checkout',views.checkout,name="checkout"),
    path('search/', views.search_view,name='search'),
    path('view/<slug:slug>',views.view,name="edit"),
    path('signup', Register.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
     path('account', Account.as_view(), name='account'),
    path('orders',auth_middleware(OrderView.as_view()),name="orders"),
    path('return',auth_middleware(ReturnView.as_view()),name="returns"),
    path('add-return/<int:id>',views.Addreturn,name="add-return"),
    path('add-cancel/<int:id>',views.Addcancel,name="add-cancel"),
    path('account-update',views.Accountupdate,name="account-update"),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('updatereturn/<int:id>',views.Updatereturn,name="updatereturn"),
    path('search_auto/', views.search_auto,name='search_auto'),
    path('remove-from-cart/<int:cart_item_id>>',views.Remove_from_cart, name='remove-from-cart'),
    path('cartview',Cartview.as_view(),name="cartview"),
    path('update_cart/<int:cart_item_id>/<int:quantity>/', update_cart, name='update_cart'),
    # path('plus-from-cart',Pluscartview.as_view(),name="plus-from-cart"),
    #  path('minus-from-cart',Minuscartview.as_view(),name="minus-from-cart"),
    path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view,name='download-invoice'),
    
]
