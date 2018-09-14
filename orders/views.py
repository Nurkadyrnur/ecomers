from django.shortcuts import render,redirect
from django.views.generic.edit import FormView,CreateView
from django.contrib import messages
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from carts.mixin import CartOrderMixin
from .forms import AddressForm,UserAddressForm
from .models import UserAddress,AddresType,UserCheckout,Order
from products.mixin import LoginRequiredMixin
# Create your views here.
class OrderDetailView(DetailView):
    model = Order
    def dispatch(self,*args,**kwargs):
        if self.request.user.is_authenticated():
            user_checkout = UserCheckout.objects.get_or_create(email=self.request.user.email,user=self.request.user)[0]
            self.request.session['user_checkout_id'] = user_checkout.id
        elif self.request.session.get('user_checkout_id') is None:
            return redirect('checkout')
        user_checkout_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        obj = self.get_object()
        if obj.user !=user_checkout:
            raise Http404
        return super().dispatch(*args,**kwargs)
class OrderListView(ListView):
    model = Order
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user_list = Order.objects.all()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(user_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        context['orders'] = users
        return context
    def dispatch(self,*args,**kwargs):
        if self.request.user.is_authenticated():
            user_checkout = UserCheckout.objects.get_or_create(email=self.request.user.email,user=self.request.user)[0]
            self.request.session['user_checkout_id'] = user_checkout.id
        elif self.request.session.get('user_checkout_id') is None:
            return redirect('checkout')
        return super().dispatch(*args,**kwargs)
    def get_queryset(self,*args,**kwargs):
        user_checkout_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        return super().get_queryset(*args,**kwargs).filter(user=user_checkout)


class UserAddressCreateView(CartOrderMixin,CreateView):
    model = UserAddress
    form_class = UserAddressForm
    success_url = '/checkout/address'
    template_name = 'forms.html'
    def dispatch(self,*args,**kwargs):
        cart = self.get_cart()
        if cart ==None:
            return redirect('cart')
        if self.request.user.is_authenticated():
            user_checkout = UserCheckout.objects.get_or_create(email=self.request.user.email,user=self.request.user)[0]
            self.request.session['user_checkout_id'] = user_checkout.id
        user_checkout_id = self.request.session.get('user_checkout_id')
        if user_checkout_id:
            return super().dispatch(*args,**kwargs)
        else:
            return redirect('checkout')
    def get_checkout_user(self):
        user_checkout_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        return user_checkout
    def form_valid(self,form,*args,**kwargs):
        form.instance.user = self.get_checkout_user()
        return super().form_valid(form,*args,**kwargs)


class AddresSelectFormView(CartOrderMixin,FormView):
    form_class = AddressForm
    template_name = 'orders/address_select.html'
    def dispatch(self,*args,**kwargs):
        cart = self.get_cart()
        if cart ==None:
            return redirect('cart')
        user_checkout_id = self.request.session.get('user_checkout_id')
        if user_checkout_id==None:
            return redirect('checkout')
        if self.request.user.is_authenticated():
            user_checkout = UserCheckout.objects.get_or_create(email=self.request.user.email,user=self.request.user)[0]
            self.request.session['user_checkout_id'] = user_checkout.id
        billing_address,shipping_address = self.get_address()
        if billing_address.count() ==0:
            messages.success(self.request,"Please add billingadress bifore to continue")
            return redirect('checkout_address_add')
        elif shipping_address.count() ==0:
            messages.success(self.request,"Please add shippingadress bifore to continue")
            return redirect('checkout_address_add')
        else:
            return super().dispatch(*args,**kwargs)
    def get_address(self,*args,**kwargs):
        shipping = AddresType.objects.get(id=2)
        bilding = AddresType.objects.get(id=1)
        user_checkout_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        billing_address = UserAddress.objects.filter(
        user = user_checkout,
        type = bilding
        )
        shipping_address = UserAddress.objects.filter(
        user = user_checkout,
        type = shipping
        )
        return (billing_address,shipping_address)
    def get_form(self,*args,**kwargs):
        form = super().get_form(*args,**kwargs)
        billing_address,shipping_address = self.get_address()
        form.fields['shipping_address'].queryset = shipping_address
        form.fields['billing_address'].queryset = billing_address
        return form
    def form_valid(self,form,*args,**kwargs):
        user_checkout_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        billing_address = form.cleaned_data['billing_address']
        shipping_address = form.cleaned_data['shipping_address']
        order = self.get_order()
        order.billing_address = billing_address
        order.shipping_address = shipping_address
        order.user = user_checkout
        order.save()

        return super().form_valid(form,*args,**kwargs)

    def get_success_url(self,*args,**kwargs):
        return "/checkout"
