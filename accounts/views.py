from django.shortcuts import render,redirect
from .forms import user_account_form
from django.contrib import messages
from django_email_verification import sendConfirm
from django.core.mail import send_mail
from .models import User
import requests
import json
from django.contrib import auth
from dashboard.models import *
from django.http import HttpResponse

def signup(request):
	if request.method=='GET':
		referid=''
		try:
			referid=request.GET['ref']
		except:
			referid = ''
		form=user_account_form()
		return render(request,'accounts/signup.html',{'form':form,'referer':referid})
		#return HttpResponse('<h1>Signup and Login are currently closed. Businessbook verify is ongoing.We will get back shortly')

	if request.method=='POST':
		referer_id=0
		is_agent=False
		agent_id=0
		
		
		form=user_account_form(request.POST)

		

		if form.is_valid():
			if request.POST.get('referer_id') == '' and form.cleaned_data['company'] ==  '':
				return render(request,'accounts/signup.html',{'form':form,'referinvalid':'you must have a referer to create account'})
			elif request.POST.get('referer_id') == '' and form.cleaned_data['company'] !=  '':
				referer_id=0
				is_agent=False
				agent_id=int(request.POST.get('agent_id'))


			else:
				referer_id=0
			first_name	=	form.cleaned_data['first_name']
			last_name	=	form.cleaned_data['last_name']
			email 		=	form.cleaned_data['email']
			mobile		=	form.cleaned_data['mobile']
			address		=	form.cleaned_data['address']
			country		=	form.cleaned_data['country']
			company		=	form.cleaned_data['company']
			password   	=	form.cleaned_data['password']
			confirm_password = form.cleaned_data['confirm_password']

			response=request.POST['g-recaptcha-response']
			secret_key='6LdVsPEUAAAAABucQvaYu3TSb20v1ynbq8gJUokK'

			sending_request=requests.post('https://www.google.com/recaptcha/api/siteverify',data={'response':response,'secret':secret_key})
			status=json.loads(sending_request.text)['success']

			if status==False:
				return render(request,'accounts/signup.html',{'form':form,'captcha':'false'})



			if password != confirm_password:
				messages.error(request,'password did not match')
				return render(request,'accounts/signup.html',{'form':form})

			try:
				User.objects.get(email=email)
				return render(request,'accounts/signup.html',{'form':form,'userexist':'true'})
			except User.DoesNotExist:
				create_user=User.objects.create_user(password=password,first_name=first_name,last_name=last_name,email=email,mobile=mobile,address=address,country=country,company=company,is_agent=is_agent,agent_id=agent_id,is_active=True)
				balance.objects.create(user=create_user)
				refer.objects.create(user=create_user,referer=referer_id)
				#sendConfirm(create_user)
				return render(request,'accounts/activation.html')


		

		


		return render(request,'accounts/signup.html',{'form':form})




def login(request):
	if request.method=='GET':


		if request.user.is_authenticated == True:
			
			return redirect('dashboard')
		else:
			#return HttpResponse('<h1>Signup and Login are currently closed. Businessbook verify is ongoing.We will get back shortly')
			
			return render(request,'accounts/login.html')

	if request.method=='POST':
		email=request.POST['loginEmail']
		password=request.POST['loginPassword']
		remember=''



		
		authen=auth.authenticate(request,email=email,password=password)

		try:
			r=request.POST['remember']
			if r=='yes':
				remember='yes'
		except:
			remember=''
				

		if authen is not None:
			select_user=User.objects.get(email=email)
			if select_user.is_agent == False and select_user.agent_id  > 0:
				return HttpResponse('<h1 style="color:red">your agent account is under review.please wait upto 12 hour and try again</h1>')


			auth.login(request,authen)

			if remember=='yes':

				request.session['email'] = email

			

			return redirect('dashboard')

		else:
			return render(request,'accounts/login.html',{'error':'email or password is wrong'})



def logout(request):
	
	auth.logout(request)
	return redirect('login')






