from django.shortcuts import render
from newlater.forms import SignUpForm,ContactForm
from django.core.mail import send_mail
from djano18.settings import EMAIL_HOST_USER
from products.models import ProductFeatured,Product
# Create your views here.
def home(request):
	template = 'home.html'
	title='Perfect'
	form = SignUpForm(request.POST or None)
	featured_img = ProductFeatured.objects.order_by('?').first()
	products = Product.objects.all().order_by('?')[:6]
	context = {
	'title':title,
	'form':form,
	'featured_img':featured_img,
	'products':products,
	}
	return render(request,template,context)
def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		email=form.cleaned_data.get('email')
		full_name=form.cleaned_data.get('full_name')
		message=form.cleaned_data.get('message')
		message_text = """
		%s:%s
		"""%(full_name,message)

		html_mes = """
		<h1>hello</h1>
		"""
		send_mail(
		    'site contact form',
		    message_text,
		    EMAIL_HOST_USER,
		    [email],
			html_message=html_mes,
		    fail_silently=False,
		)
		form = ContactForm()
	context = {
	'form':form
	}
	return render(request,'forms.html',context)
