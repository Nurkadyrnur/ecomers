import braintree
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render ,get_object_or_404 , redirect
from django.http import Http404,HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import View
from carts.models import Cart,CartItem
from products.models import Variation
from orders.forms import UserCheckoutForm
from orders.models import UserCheckout,UserAddress,Order
from django.views.generic.edit import FormMixin
from carts.mixin import CartOrderMixin
# Create your views here.

if settings.DEBUG:
    gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHAND_ID,
        public_key=settings.BRAINTREE_PUBLIC,
        private_key=settings.BRAINTREE_PRIVATE
    )
)
class CartCount(View):
    def get(self, request,*args,**kwars):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if cart_id == None:
                count = 0
            else:
                count = Cart.objects.get(pk=cart_id).cartitem_set.count()
                self.request.session['cart_count'] = count

            return JsonResponse({'count':count})
        else:
            Http404

class CartView(SingleObjectMixin,View):
    model = Cart
    template_name = "carts/view.html"
    def get_object(self,*args,**kwargs):
            self.request.session.set_expiry(0)
            cart_id = self.request.session.get("cart_id")
            if cart_id == None:
                cart = Cart()
                cart.save()
                cart_id = cart.id
                self.request.session["cart_id"] = cart.id
            cart = Cart.objects.get(id=cart_id)
            if self.request.user.is_authenticated():
                cart.user = self.request.user
                cart.save()
            return cart
    def get(self, request,*args,**kwars):
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete",False)
        create_item = False
        message_cart = ''
        if item_id:
            item_instance = get_object_or_404(Variation,id = item_id)
            qty = request.GET.get("qty",1)
            try:
                if int(qty)<1:
                    delete_item = True
            except:
                raise Http404
            cart_item,create = CartItem.objects.get_or_create(cart=cart,item=item_instance)
            if create:
                create_item = True
                message_cart = 'Success add to cart'
            if delete_item:
                cart_item.delete()
                message_cart = 'Success delete from cart'
            else:
                message_cart = 'Success add to cart'
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse('cart'))
        if request.is_ajax():
            line_total = cart_item.line_total_price
            subtotal = cart_item.cart.sub_total
            tax_total = cart_item.cart.tax_total
            total = cart_item.cart.total
            data = {'deleted':delete_item,
                    "item_added":create_item,
                    "line_total":line_total,
                    "subtotal":subtotal,
                    'message_cart':message_cart,
                    'tax_total':tax_total,
                    'total':total,
                    }
            return JsonResponse(data)
        context = {
        "object":self.get_object()
        }
        return render(request,self.template_name,context)



class CheckoutView(CartOrderMixin,FormMixin,DetailView):
    model = Cart
    template_name = 'carts/checkout_view.html'
    form_class = UserCheckoutForm
    def get_object(self,*args,**kwargs):
        cart = self.get_cart()
        return cart
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        user_can_continue = False
        user_checkout_id = self.request.session.get('user_checkout_id')
        if self.request.user.is_authenticated() or user_checkout_id !=None:
            user_can_continue =True
            if self.get_order():
                context['order'] = self.get_order()
                user_checkout_id = self.request.session.get('user_checkout_id')
                if user_checkout_id:
                    user_checkout = UserCheckout.objects.get(id=user_checkout_id)
                    context['client_token'] = user_checkout.get_client_token()
        else:
            context['login_form']= AuthenticationForm()
            context['next_url'] = self.request.build_absolute_uri()
        if self.request.user.is_authenticated():
            user_checkout = UserCheckout.objects.get_or_create(email=self.request.user.email,user=self.request.user)[0]
            self.request.session['user_checkout_id'] = user_checkout.id

        context['user_can_continue'] = user_can_continue
        context['form'] = self.get_form()

        return context
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_checkout = UserCheckout.objects.get_or_create(email=email)[0]
            self.request.session['user_checkout_id'] = user_checkout.id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def get_success_url(self):
        return reverse('checkout')
    def get(self,request,*args,**kwargs):
        get_data = super().get(request,*args,**kwargs)
        cart = self.get_cart()
        if cart ==None:
            return redirect('cart')
        user_checkout_id = self.request.session.get("user_checkout_id")
        if user_checkout_id:
            new_order = self.get_order()
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if (new_order.shipping_address == None or new_order.billing_address == None) or new_order.user !=user_checkout:
                return redirect("checkout_address")
        return get_data
class CheckoutFinalView(CartOrderMixin,View):
    def post(self,request,*args,**kwargs):
        order = self.get_order()
        nonce = request.POST.get('payment_method_nonce')
        if nonce:
            result = gateway.transaction.sale({
                "amount": order.order_total,
                "payment_method_nonce": nonce,
                "billing": {
                        "postal_code": '%s' % (order.billing_address.zipcode),
                      },
                "options": {
                    "submit_for_settlement": True
                }
            })
        if result.is_success:
            order.mark_complated(order_id=result.transaction.id)
            del request.session['cart_id']
            del request.session['order_id']
            messages.success(request,'Thank you for your order')
            return redirect('order_detail',pk=order.pk)
        else:
          messages.success(request,'%s' % (result.message))
          redirect('checkout')


    def get(self,request,*args,**kwargs):
        return redirect('checkout')
