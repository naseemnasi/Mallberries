"""mallberyy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app1 import views
from app1.middlewares.auth import auth_middleware

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("index", views.index, name='index'),
                  path('aboutus', views.aboutus, name='aboutus'),
                  path('contact', views.contact, name='contact'),
                  path('cart', views.Cart.as_view(), name='cart'),
                  path('finale', auth_middleware(views.finale.as_view()), name='finale'),
                  path('checkout', views.checkout.as_view(), name='checkout'),
                  path('login', views.login, name='login'),
                  path('logout', views.logout, name='logout'),
                  path('register', views.register.as_view(), name='register'),
                  path("",views.prod,name="product"),
                  path("details",views.details.as_view(),name="pro_details"),
                  path("shop", views.prod,name="product"),

                  ##admin side
                  path('admin_mallberry', views.admin_mall, name="admin_emall"),
                  path('ad_login', views.ad_log, name='ad_login'),
                  path('ad_logout', views.ad_logout, name='ad_logout'),
                  path('ad_addpro', views.adminpro, name="ad_addpro"),
                  path('ad_proList', views.ad_proList, name="ad_proList"),
                  path('ad_orders', views.ad_orders, name="ad_orders"),
                  path('ad_customerList', views.ad_customerList, name="ad_customerList"),
                  path('pdelete/<int:pro_id>', views.pdelete, name='pdelete'),
                  path('odelete/<int:order_id>', views.odelete, name='odelete'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
