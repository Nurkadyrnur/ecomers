"""djano18 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from newlater import views
from carts.views import CartView,CartCount,CheckoutView,CheckoutFinalView
from orders.views import AddresSelectFormView,UserAddressCreateView,OrderListView,OrderDetailView
urlpatterns = [
	url(r'^$',views.home, name = 'home'),
    url(r'^contact/$',views.contact, name = 'contact'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^categories/', include('products.urls_categories')),
    url(r'^cart/$', CartView.as_view(),name='cart'),
    url(r'^order/$', OrderListView.as_view(),name='order'),
    url(r'^order/(?P<pk>\d+)/$', OrderDetailView.as_view(),name='order_detail'),
    url(r'^checkout$', CheckoutView.as_view(),name='checkout'),
    url(r'^cart/count$', CartCount.as_view(),name='cart_count'),
    url(r'^checkout/address$', AddresSelectFormView.as_view(),name='checkout_address'),
    url(r'^checkout/address/add$', UserAddressCreateView.as_view(),name='checkout_address_add'),
    url(r'^checkout/final$', CheckoutFinalView.as_view(),name='checkout_final'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
