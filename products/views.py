from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from django.shortcuts import render ,get_object_or_404 , redirect
from django.http import Http404,HttpResponseRedirect
from django.contrib import messages
import random
from products.models import Product, Variation ,Category
from products.mixin import StaffRequiredMixin,LoginRequiredMixin
from products.forms import VariationInventoryFormset,ProductFilterForm
from django.contrib.auth.decorators import login_required
from django_filters import FilterSet,CharFilter,NumberFilter
# Create your views here.




class CategoryDetailView(DetailView):
    model = Category
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        default_product = obj.default_category.all()
        products = (product_set|default_product).distinct()
        context['products'] = products
        return context






class CategoryListView(StaffRequiredMixin,ListView):
    model = Category


class ProductDetailView(DetailView):
    model = Product
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        instance = self.get_object()
        related = sorted(Product.objects.get_related(instance)[:6] ,key=lambda x: random.random())
        context['related'] = related
        return context





class VariationListView(StaffRequiredMixin,ListView):
    model = Variation
    def get_context_data(self,*args , **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['formset'] = VariationInventoryFormset(queryset=self.get_queryset())
        return context
    def get_queryset(self , *args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        prime_key = self.kwargs.get("pk")
        if prime_key:
            product = get_object_or_404(Product , pk=prime_key)
            qs = qs.filter(product=product)
        return qs
    def post(self, request,*args,**kwars):
        formset = VariationInventoryFormset(request.POST,request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            messages.success(self.request,"Your Variation updated.")
            return redirect("product_list")

        raise Http404
class ProductFilter(FilterSet):
    title = CharFilter(name = 'title',lookup_type='icontains',distinct = True)
    categories = CharFilter(name = 'categories__title',lookup_type='icontains',distinct = True)
    categories_id = CharFilter(name = 'categories__id',lookup_type='icontains',distinct = True)
    min_price = NumberFilter(name = 'variation__price',lookup_type='gte',distinct = True)
    max_price = NumberFilter(name = 'variation__price',lookup_type='lte',distinct = True)
    class Meta:
        model = Product
        fields = [
        'categories_id',
        'min_price',
        'max_price',
        'title',
        'categories',
        'description',
        ]

class FilterMixin(object):
    filter_class = None
    search_ordering_param = 'ordering'
    def get_queryset(self,*args,**kwargs):
        try:
            qs = super(FilterMixin,self).get_queryset(*args,**kwargs)
            return qs
        except:
            raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")
    def get_context_data(self,*args,**kwargs):
        context = super(FilterMixin,self).get_context_data(*args,**kwargs)
        qs = self.get_queryset()
        ordering = self.request.GET.get(self.search_ordering_param)
        if ordering:
            qs=qs.order_by(ordering)
        filter_class = self.filter_class
        if filter_class:
            f= filter_class(self.request.GET,queryset=qs)
            context['object_list'] = f
        return context



class ProductListView(FilterMixin,ListView):
    model = Product
    filter_class = ProductFilter
    queryset = Product.objects.filter(active=True)

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET or None)
        return context
    def get_queryset(self , *args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains = q)|Q(description__icontains = q))
            try:
                qs2 = qs.filter(Q(price__icontains = q))
                qs = (qs|qs2).distinct()
            except:
                pass
        return qs
