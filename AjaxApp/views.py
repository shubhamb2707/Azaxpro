from django.shortcuts import render
from .models import User
from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .forms import *
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required


# for Email varification line no 13 to 19
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
#from django.contrib.auth.models import User
from django.core.mail import EmailMessage



@login_required(login_url='login/')
def index(request):
	return render(request,"index.html")


def register(request):
	
	if request.method == "POST":
		import pdb;
		pdb.set_trace()

		form = UserForm(request.POST)
		if form.is_valid():
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			username = request.POST.get('username')
			email = request.POST.get('email')
			UserField = request.POST.get('UserField')
			password = request.POST.get("password")

			user=User(
				first_name = first_name,
				last_name = last_name,
				username = username,
				email = email,
				UserField = UserField,
				)
			user.set_password(password)
			user.is_active = False
			user.save()

			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account.'
			message = render_to_string('activate_account.html', {
				'user': user,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),
				'token':account_activation_token.make_token(user),
				})

			to_email = form.cleaned_data.get('email')

			email = EmailMessage(
				mail_subject, message, to=[to_email]
				)
			email.send()

			return HttpResponse('Please confirm your email address to complete the registration')	
		    
	else:
		form = UserForm()
		return render(request,"UserRegistration.html", {"form":form})


def loginn(request):

	if request.method=='POST':
		
		lform = LoginForm(request.POST)
		if lform.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)

			if user.UserField == "student":
				auth_login(request,user)
				return redirect("register")
			elif user.UserField == "teacher":
				auth_login(request,user)
				return redirect("index")
			else:
				return HttpResponse("galat hai")
		else:
			return HttpResponse("Login Data Sahi Nahi Hai")

	else:
		lform = LoginForm()
		return render(request, 'login.html', {'lform': lform})





def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		# return redirect('home')
		return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
	else:
		return HttpResponse('Activation link is invalid!')