from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.http import HttpRequest
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password
from django.db.models import Q,Avg,Sum
from . import models
import random
from .models import *
from accounts.models import User
from django.views import generic
from django.urls import reverse_lazy


def test(request):
	return  render(request,'accounts/activation.html')


def check_exist_or_not(request):
	objs = PremiumPlan.objects.filter(user=request.user)
	exist = False
	if (objs.exists() and objs.count() == 1):
		obj = objs.first()
		if (obj.plan == True):
			exist = True
	return  exist

def redirect_to_add_premium_plan(request):
	print('in redirect_to_add_premium_plan')
	if request.session.has_key('order_number'):
		del request.session['order_number']
		del request.session['user_id']
	user_id = request.user.id
	order_number = random.randint(100, 999)
	request.session['user_id'] = user_id
	request.session['order_number'] = order_number
	objs = PremiumPlan.objects.filter(user=request.user)
	activate = False
	exist = False
	if (objs.exists() and objs.count() == 1):
		obj = objs.first()
		if (obj.plan == False):
			activate = obj.plan
			return render(request, 'dashboard/add_premium_plan.html',
						  {'user_id': user_id, 'order_number': order_number, 'activate': activate, 'exist': exist})
		else:
			activate = True
			exist = True
			return render(request, 'dashboard/add_premium_plan.html',
						  {'user_id': user_id, 'order_number': order_number, 'activate': activate, 'exist': exist})
	else:
		print('in else redirect_to_add_premium_plan ###')
		activate = False
		return render(request, 'dashboard/add_premium_plan.html',
					  {'user_id': user_id, 'order_number': order_number, 'activate': activate, 'exist': exist})


@login_required(login_url='/accounts/login/')
def dashboard(request):
	objs = PremiumPlan.objects.filter(user=request.user)
	exist=False
	if(objs.exists() and objs.count()==1):
		obj = objs.first()
		if(obj.plan==True):
			exist=True
		else:
			return redirect('add_premium_plan')

	else:
		return redirect('add_premium_plan')


	expired_adpacks = bought_adpack.objects.filter(
								Q(expiration_date__lt=datetime.now())
								&
								Q(user=request.user)
							)
	for ob in expired_adpacks:
		ob.delete()

	total_active_adpacks1=bought_adpack.objects.filter(Q(expiration_date__gt=datetime.now()) & Q(user=request.user))
	if(total_active_adpacks1.exists()):
		for obje in total_active_adpacks1:
			# bal+=obje.everyday_revenue
			try:
				if(obje.last_benefit_date!=datetime.now().date()):
					balll = balance.objects.get(user=request.user)
					balll.current_balance = round(balll.current_balance+obje.everyday_revenue,2)
					balll.save()
					obje.last_benefit_date = datetime.now().date()
					obje.save()
			except:
				balll = 0

	total_active_adpacks = \
	bought_adpack.objects.filter(Q(expiration_date__gt=datetime.now()) & Q(user=request.user)).aggregate(
		total_act_ad=Sum('total_quantity'))['total_act_ad']

	if total_active_adpacks == None:
		total_active_adpacks=0
	total_referal 	= len(refer.objects.filter(referer=request.user.id))
	twithdraw 		= withdraw_requests.objects.filter(user=request.user).aggregate(s=Sum('amount'))['s']

	if twithdraw == None:
		twithdraw=0

	try:
		bal=balance.objects.get(user=request.user).current_balance
		bal = round(bal, 2)
	except:
		bal=0
	return render(request,'dashboard/dashboard.html',{'balance':bal,'active_adpacks':total_active_adpacks,'total_referal':total_referal,'total_withdraw':twithdraw,'exist':exist})

@csrf_exempt
def payment_success(request):

	if request.method=="POST":
		payee_account=request.POST['PAYEE_ACCOUNT']
		if payee_account == 'U24170548':
			return render(request,'dashboard/funding_success.html')
		else:
			HttpResponse('sorry,something went wrong')
	else:
		return HttpResponse('wrong destination')


@csrf_exempt
def premium_plan_success(request):
	if request.method=="POST":
		payee_account=request.POST['PAYEE_ACCOUNT']
		if payee_account == 'U24170548':
			objs = PremiumPlan.objects.filter(user=request.user)
			if (objs.exists() and objs.count() == 1):
				obj = objs.first()
				obj.user=request.user
				obj.plan=True
				obj.save()
			else:
				PremiumPlan.objects.create(user=request.user,plan=True)
			return render(request,'dashboard/add_premium_plan_successfully.html')
		else:
			HttpResponse('sorry,something went wrong')
	else:
		return HttpResponse('wrong destination')



@csrf_exempt
def payment_failed(request):
	if request.method == "POST":
		return render(request,'dashboard/funding_failed.html')

	else:
		return HttpResponse('wrong destination')



@login_required
def add_fund(request):
	# exist = check_exist_or_not(request)
	# if (not exist):
	# 	return redirect('add_premium_plan')
	if request.session.has_key('order_number'):
		del request.session['order_number']
		del request.session['user_id']



	user_id=request.user.id
	order_number=random.randint(100,999)
	request.session['user_id']=user_id
	request.session['order_number']=order_number
	return render(request,'dashboard/add_fund.html',{'user_id':user_id,'order_number':order_number})


@login_required
def add_premium_plan(request):
	if request.session.has_key('order_number'):
		del request.session['order_number']
		del request.session['user_id']
	user_id=request.user.id
	order_number=random.randint(100,999)
	request.session['user_id']=user_id
	request.session['order_number']=order_number
	objs = PremiumPlan.objects.filter(user=request.user)
	activate=False
	exist=False
	if (objs.exists() and objs.count() == 1):
		obj = objs.first()
		if (obj.plan == False):
			activate = obj.plan
			return render(request,'dashboard/add_premium_plan.html',{'user_id':user_id,'order_number':order_number,'activate':activate,'exist':exist})
		else:
			activate=True
			exist = True
			return render(request, 'dashboard/add_premium_plan.html',
						  {'user_id': user_id, 'order_number': order_number, 'activate': activate,'exist':exist})
	else:
		activate=False
		return render(request, 'dashboard/add_premium_plan.html',
					  {'user_id': user_id, 'order_number': order_number, 'activate': activate,'exist':exist})

	# return render(request,'dashboard/add_premium_plan.html',{'user_id':user_id,'order_number':order_number})


@csrf_exempt
def payment_status(request):
	if request.method=="POST":

		payee_account=request.POST['PAYEE_ACCOUNT']
		amount=float(request.POST['PAYMENT_AMOUNT'])
		payeer_account=request.POST['PAYER_ACCOUNT']
		order_number=request.POST['ORDER_NUM']
		user_id=request.POST['CUST_NUM']

		if payee_account == 'U24170548':
			usr=User.objects.get(id=int(user_id))
			bal=balance.objects.get(user=usr)
			curr_bal=float(bal.current_balance)
			bal.current_balance=(curr_bal+amount)
			bal.save()
			deposit_history.objects.create(user=request.user,amount=amount)
			return HttpResponse('success')
		else:
			return HttpResponse('failed payment')
	else:
		return HttpResponse('failed')


@login_required(login_url='/accounts/login/')
def balance_transfer(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')

	# redirect_to_add_premium_plan(request)
	if request.method == 'POST':
		toemail=request.POST['toemail']
		amount=float(request.POST['amount'])
		userbalancedata =  balance.objects.get(user=request.user)
		userbalance=userbalancedata.current_balance
		if amount>userbalance :
			messages.warning(request,'dont have enough funds')
			return redirect('send_money')
		try:
			to=balance.objects.get(user__email=toemail)
			userbalancedata.current_balance=round(float(userbalancedata.current_balance - amount),2)
			userbalancedata.save()
			to.current_balance=round(float(to.current_balance + amount),2)
			to.save()

			send_money_history.objects.create(sent_from=request.user,sent_to=toemail,sent_amount=amount)
			messages.success(request,'balance transfer successful')
			return redirect('send_money')
		except balance.DoesNotExist :
			messages.info(request,'user does not exist')
			return redirect('send_money')

@login_required(login_url='/accounts/login/')
def adpack_list(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')
	adp_list=adpack.objects.all()
	return render(request,'dashboard/adpack-list.html',{'adp_list':adp_list,'exist':exist})

@login_required(login_url='/accounts/login/')
def refer_page(request):
	usrid=request.user.id
	refered_user=refer.objects.filter(referer=int(usrid))
	return render(request,'dashboard/refer.html',{'referdata':refered_user})


@login_required(login_url='/accounts/login/')
def refer_list(request):
	usrid=request.user.id
	refered_user=refer.objects.filter(referer=int(usrid))
	return render(request,'dashboard/refer_list.html',{'referdata':refered_user})

@login_required(login_url='/accounts/login/')
def buy_adpack(request,level):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')

	if request.method == 'GET':
		adpdetails=adpack.objects.filter(level=level).first()

		return render(request,'dashboard/buy-adpack.html',{'adpack_details':adpdetails})

	if request.method == 'POST':
		level=request.POST['level']
		quantity=int(request.POST['quantity'])
		user=request.user

		adp=adpack.objects.get(level=int(level))
		total_price=round(float(adp.value*quantity),2)
		total_revenue=round(float(adp.perday_revenue*60*quantity),2)
		perday_revenue=round(float(adp.perday_revenue*quantity),2)
		affiliate_commission=round(float(adp.affiliate_earn*quantity),2)
		
		try:
			affiliate_id=refer.objects.get(user=request.user).referer
		except:
			refer.objects.create(user= request.user)
			try:
				affiliate_id = refer.objects.get(user=request.user).referer
			except:
				pass
		expiration_date=datetime.now()+timedelta(days=60)
		bal=balance.objects.get(user=request.user).current_balance
		max_buy=int(adp.max_buy)
		recent_bought=[]
		for i in range(0,int(level)):
			recent_bought.append(i)

		try:

			prev_max_buy =  adpack.objects.get(level=int(recent_bought[-1])).max_buy

		except adpack.DoesNotExist:
			prev_max_buy=0

		check=bought_adpack.objects.filter(Q(user=request.user) & Q(expiration_date__gt=datetime.now()) & Q(bought_adpacks__level=int(recent_bought[-1]))).aggregate(s=Sum('total_quantity'))['s']
		if check == None :
			check=0

		check_max=bought_adpack.objects.filter(Q(user=request.user) & Q(expiration_date__gt=datetime.now()) & Q(bought_adpacks__level=int(level))).aggregate(s=Sum('total_quantity'))['s']

		if check_max == None :
			check_max = 0

		if bal<total_price:							
			messages.info(request,'insufficient fund')
			return redirect('buy_adpack',int(level))

		elif check<prev_max_buy and int(level)!=1 :
			messages.warning(request,'you can not buy before buying(max) previous level adpack')
			return redirect('buy_adpack',int(level))

		elif (max_buy-(check_max))<quantity:
			string='you are allowed to buy only '+str((max_buy-(check_max)))+' more adpacks with this package'
			messages.error(request,string)
			return redirect('buy_adpack',int(level))
		else:
			usrbalance=balance.objects.get(user=request.user)
			usrbalance.current_balance=(usrbalance.current_balance)-total_price
			usrbalance.save()
			adpack_database=bought_adpack()
			adpack_database.user=request.user
			adpack_database.expiration_date=expiration_date
			adpack_database.buying_date=datetime.now()
			adpack_database.total_quantity=quantity
			adpack_database.bought_adpacks=adp
			adpack_database.adpack_totalreturn=total_revenue
			adpack_database.everyday_revenue=perday_revenue
			adpack_database.affiliate_commission=affiliate_commission
			adpack_database.total_price=total_price

			adpack_database.save()

			rupdate=refer.objects.get(user=request.user)
# 			adding_bal=balance.objects.get(user_id=affiliate_id)
# 			adding_bal.current_balance=round((float(adding_bal.current_balance)+affiliate_commission),2)
# 			adding_bal.save()
			rupdate.refer_earn=round(float(rupdate.refer_earn+affiliate_commission),2)
			rupdate.save()
			messages.success(request,'successfully bought adpack')
			return redirect('buy_adpack',int(level))

@login_required(login_url='/accounts/login/')
def revenue_history(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')
	sel_all_adpack = bought_adpack.objects.filter(user=request.user)
	if len(sel_all_adpack) == 0:
		return render(request,'dashboard/revenue_history.html',{'message':'you dont have revenue history','exist':exist})
	history = []
	for pack in sel_all_adpack:
		updated_adp=adpack_update.objects.filter(bought_adpack_name_id=pack.id).aggregate(paid_rev=Sum('today_revenue'))
		paid_so_far=updated_adp['paid_rev']
		history.append({'pack':pack.bought_adpacks.title,'buying_date':pack.buying_date,'expiration_date':pack.expiration_date,'total_paid':paid_so_far,'total_quantity':pack.total_quantity})

	page = request.GET.get('page', 1)
	history.reverse()
	paginator = Paginator(history, 10)

	try:
		hist=paginator.page(page)
	except PageNotAnInteger:
		hist=paginator.page(1)
	except EmptyPage:
		hist=paginator.page(paginator.num_pages)
	return render(request,'dashboard/revenue_history.html',{'history':hist,'exist':exist})

'''
	try:
		hist=paginator.page(page)

    except PageNotAnInteger:

    	hist=paginator.page(1)

    except EmptyPage:

        hist=paginator.page(paginator.num_pages)

 '''
@login_required(login_url='/accounts/login/')
def adpack_history(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')
	sel_all_adpack = bought_adpack.objects.filter(user=request.user).order_by('-buying_date')
	if len(sel_all_adpack) == 0:
		return render(request,'dashboard/adpack_history.html',{'message':'you dont have adpack history','exist':exist})


	page = request.GET.get('page', 1)
	paginator = Paginator(sel_all_adpack, 10)

	try:
		hist=paginator.page(page)
	except PageNotAnInteger:
		hist=paginator.page(1)
	except EmptyPage:
		hist=paginator.page(paginator.num_pages)
	return render(request,'dashboard/adpack_history.html',{'history':hist,'exist':exist})



class personal_info(generic.UpdateView):
	model = User
	fields=['first_name','last_name','mobile','address','profile_picture','nid_front','nid_back']
	template_name='dashboard/update-personal-info.html'
	success_url=reverse_lazy('dashboard')

	context_object_name='info'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		exist = check_exist_or_not(self.request)
		context['exist'] = exist
		print('context in personal info ##',context)
		return context

@login_required(login_url='/accounts/login/')
def payment_info(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')
	pm_info=''
	bank_info=''
	agent_info=''
	bkash_info=''
	rocket_info=''
	nagad_info=''
	try:
		pm_info=pm_accounts.objects.get(user=request.user)
	except:
		added=False
	try:
		bank_info=bank_accounts.objects.get(user=request.user)
	except:
		added=False
	try:
		agent_info=agent_accounts.objects.get(user=request.user)
	except :
		added=False
	try:
		bkash_info=bkash_accounts.objects.get(user=request.user)
	except:
		added=False
	try:
		rocket_info=rocket_accounts.objects.get(user=request.user)
	except:
		added=False
	try:
		nagad_info=nagad_accounts.objects.get(user=request.user)
	except:
		added=False



	return render(request,'dashboard/payment_info.html',{'pm_info':pm_info,
														 'bank_info':bank_info,
														 'agent_info':agent_info,
														 'bkash_info':bkash_info,
														 'rocket_info':rocket_info,
														 'nagad_info':nagad_info,
														 'exist':exist
														 })

@login_required(login_url='/accounts/login/')
def pm_add(request):
	if request.method == 'POST':
		account =  request.POST['pm_account']

		try:
			check=pm_accounts.objects.get(user=request.user)
			check.pm_account=account
			check.save()
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')

		except pm_accounts.DoesNotExist:
			pm_accounts.objects.create(user=request.user,pm_account=account)
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')


@login_required(login_url='/accounts/login/')
def agent_account_add(request):
	if request.method == 'POST':
		account =  request.POST['agent_email']

		try:
			check=agent_accounts.objects.get(user=request.user)
			check.agent_email=account
			check.save()
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')

		except agent_accounts.DoesNotExist:
			agent_accounts.objects.create(user=request.user,agent_email=account)
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')


@login_required(login_url='/accounts/login/')
def bank_info_add(request):
	if request.method == 'POST':
		
		account_number =  request.POST['bank_account_number']
		account_holder = request.POST['account_holder_name']
		bank_name = request.POST['bank_name']
		branch_name = request.POST['branch_name']
		ifsccode = request.POST['ifsccode']
		description = request.POST['description']

		try:
			check=bank_accounts.objects.get(user=request.user)
			check.account_holder_name=account_holder
			check.bank_name=bank_name
			check.account_number=account_number
			check.branch_name=branch_name
			check.ifsc_code=ifsccode
			check.description=description
			check.save()
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')

		except bank_accounts.DoesNotExist:
			bank_accounts.objects.create(user=request.user,account_holder_name=account_holder,bank_name=bank_name,branch_name=branch_name,ifsc_code=ifsccode,description=description)
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')



@login_required(login_url='/accounts/login/')
def bkash_add(request):
	if request.method == 'POST':
		account =  request.POST['bkash_account']

		try:
			check=bkash_accounts.objects.get(user=request.user)
			check.bkash_number=account
			check.save()
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')

		except bkash_accounts.DoesNotExist:
			bkash_accounts.objects.create(user=request.user,bkash_number=account)
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')

@login_required(login_url='/accounts/login/')
def rocket_add(request):
	if request.method == 'POST':
		account =  request.POST['rocket_account']

		try:
			check=rocket_accounts.objects.get(user=request.user)
			check.rocket_number=account
			check.save()
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')

		except rocket_accounts.DoesNotExist:
			rocket_accounts.objects.create(user=request.user,rocket_number=account)
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')

@login_required(login_url='/accounts/login/')
def nagad_add(request):
	if request.method == 'POST':
		account =  request.POST['nagad_account']

		try:
			check=nagad_accounts.objects.get(user=request.user)
			check.nagad_number=account
			check.save()
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')

		except nagad_accounts.DoesNotExist:
			nagad_accounts.objects.create(user=request.user,nagad_number=account)
			messages.info(request,'payment information added successfully')
			return redirect('payment_info')




@login_required(login_url='/accounts/login/')
def withdraw_premium_plan(request):
	print('in withdraw_premium_plan @@@@ ')
	# exist = check_exist_or_not(request)
	# if (not exist):
	# 	return redirect('add_premium_plan')
	price=20
	read_only=True
	context = {'price':price,'read_only':read_only}

	if request.method == 'POST':
		return render(request,'dashboard/withdraw_premium_plan.html',context)


@login_required(login_url='/accounts/login/')
def withdraw(request):
	# exist = check_exist_or_not(request)
	# if (not exist):
	# 	return redirect('add_premium_plan')
	if request.method == 'POST':
		return render(request,'dashboard/withdraw_premium_plan.html')

	if request.method == 'GET':
		return render(request,'dashboard/withdraw.html')


@login_required(login_url='/accounts/login/')
def withdraw_request_premium(request):
	print('in withdraw_request_premium')
	print("request.method",request.method)
	if request.method=='GET':
		amount = 20
		check=balance.objects.get(user=request.user).current_balance

		if amount>check:
			messages.info(request, 'not enough funds to activate premium plan')
			# return JsonResponse({'message':'not enough funds to activate premium plan'})
			return redirect('dashboard')

		b=balance.objects.get(user=request.user)
		b.current_balance=(b.current_balance-amount)
		b.save()

		obj = PremiumPlan.objects.filter(user=request.user)
		if(obj.exists()):
			obj = obj.first()
			obj.plan=True
			obj.save()
		else:
			PremiumPlan.objects.create(user=request.user, plan=True)
		messages.info(request, 'Your premium plan activated successfully')
		return redirect('dashboard')

		# return JsonResponse({'message':'Your premium plan activated successfully'})
	else:
		messages.info(request, 'Your premium plan not activated ')
		return redirect('add_premium_plan')

@login_required(login_url='/accounts/login/')
def withdraw_request(request):
	if request.method=='GET':
		method=None
		str_method=''
		via = request.GET['via']
		amount = float(request.GET['amount'])
		password = request.GET['password']

		if via=='pm':
			method=pm_accounts
			str_method='perfectMoney'
		elif via=='bt':
			method=bank_accounts
			str_method='Bank transfer'
		elif via=='at':
			method=agent_accounts
			str_method='agent transfer'
		elif via=='bkash':
			method=bkash_accounts
			str_method='bkash transfer'
		elif via=='rocket':
			method=rocket_accounts
			str_method='rocket transfer'
		elif via=='nagad':
			method=nagad_accounts
			str_method='nagad transfer'
		else:
			method=None

		check=balance.objects.get(user=request.user).current_balance
		if amount>check:
			return JsonResponse({'message':'not enough funds to withdraw'})

		if amount<100 and str_method=='Bank transfer':
			return JsonResponse({'message':'minimum withdraw for bank is 100$'})

		if amount<10 and str_method=='agent transfer':
			return JsonResponse({'message':'minimum withdraw for agent transfer is 10$'})

		if amount<50 and str_method=='perfectMoney':
			return JsonResponse({'message':'minimum withdraw for perfectMoney is 50$'})
		if amount<15 and (str_method=='bkash transfer' or str_method=='rocket transfer' or str_method=='nagad transfer'):
			return JsonResponse({'message':'minimum withdraw for mobile bank is 15$'})


		if check_password(password,request.user.password) != True:
			return JsonResponse({'message':'password did not match'})

		try:
			method.objects.get(user=request.user)
		except method.DoesNotExist:
			return JsonResponse({'message':'payment account is not added' })

		b=balance.objects.get(user=request.user)
		b.current_balance=(b.current_balance-amount)
		b.save()


		withdraw_requests.objects.create(user=request.user,method=str_method,amount=amount)

		return JsonResponse({'message':'payment request successful'})

@login_required(login_url='/accounts/login/')
def change_password(request):
	exist = check_exist_or_not(request)
	if(not exist):
		return redirect('add_premium_plan')
	if request.method == 'GET':


		return render(request,'dashboard/change-password.html',{'exist':exist})

	if request.method == 'POST':
		curr=request.POST['current_pass']
		new=request.POST['new_pass1']
		con=request.POST['new_pass2']

		if check_password(curr,request.user.password)==False:
			messages.info(request,'current password is not correct')
			return redirect('change_password')

		if new != con:
			messages.info(request,'password did not match')
			return redirect('change_password')

		u=User.objects.get(email=request.user.email)
		u.set_password(new)
		u.save()
		messages.info(request,'password has changed successfully')

		return redirect('change_password')


		

@login_required(login_url='/accounts/login/')
def withdraw_history(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')
	all_withdraw_data=withdraw_requests.objects.filter(user=request.user).order_by('-date')
	if len(all_withdraw_data) == 0:
		return render(request,'dashboard/withdraw-history.html',{'message':'you dont have any withdraw request','exist':exist})

	withdraw_data=[]

	for req in all_withdraw_data:
		date=req.date
		amount=req.amount
		method=req.method
		payment_done=req.payment_done
		payment_error=req.payment_error
		withdraw_data.append({'date':date,'amount':amount,'method':method,'payment_done':payment_done,'payment_error':payment_error})


	page = request.GET.get('page', 1)
	paginator = Paginator(withdraw_data, 10)

	try:
		hist=paginator.page(page)
	except PageNotAnInteger:
		hist=paginator.page(1)
	except EmptyPage:
		hist=paginator.page(paginator.num_pages)



	return render(request,'dashboard/withdraw-history.html',{'hist':hist,'exist':exist})





@login_required(login_url='/accounts/login/')
def deposits_history(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')

	all_deposit_data=deposit_history.objects.filter(user=request.user).order_by('-date')

	if len(all_deposit_data) == 0:
		return render(request,'dashboard/deposit-history.html',{'message':'you dont have any deposit record','exist':exist})

	deposit_data=[]

	for req in all_deposit_data:
		date=req.date
		amount=req.amount
		method=req.method
		
		deposit_data.append({'date':date,'amount':amount,'method':method})


	page = request.GET.get('page', 1)
	paginator = Paginator(deposit_data, 10)

	try:
		hist=paginator.page(page)
	except PageNotAnInteger:
		hist=paginator.page(1)
	except EmptyPage:
		hist=paginator.page(paginator.num_pages)



	return render(request,'dashboard/deposit-history.html',{'hist':hist,'exist':exist})
	






@login_required(login_url='/accounts/login/')
def send_Money_history(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')
	all_sendmoney_data=send_money_history.objects.filter(sent_from=request.user).order_by('-date')

	if len(all_sendmoney_data) == 0:
		return render(request,'dashboard/sendmoney_history.html',{'message':'you dont have any send record','exist':exist})

	sendmoney_data=[]

	for req in all_sendmoney_data:
		date=req.date
		amount=req.sent_amount
		reciever=req.sent_to
		
		sendmoney_data.append({'date':date,'amount':amount,'reciever':reciever})


	page = request.GET.get('page', 1)
	paginator = Paginator(sendmoney_data, 10)

	try:
		hist=paginator.page(page)
	except PageNotAnInteger:
		hist=paginator.page(1)
	except EmptyPage:
		hist=paginator.page(paginator.num_pages)




	return render(request,'dashboard/sendmoney_history.html',{'history':hist,'exist':exist})












@login_required(login_url='/accounts/login/')
def receivedmoney_history(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')
	all_receivedmoney_data=send_money_history.objects.filter(sent_to=request.user.email).order_by('-date')

	if len(all_receivedmoney_data) == 0:
		return render(request,'dashboard/received_money_history.html',{'message':'you dont have any received record',
																	   'exist':exist})

	receivedmoney_data=[]

	for req in all_receivedmoney_data:
		date=req.date
		amount=req.sent_amount
		sender=req.sent_from.email
		
		receivedmoney_data.append({'date':date,'amount':amount,'sender':sender})


	page = request.GET.get('page', 1)
	paginator = Paginator(receivedmoney_data, 10)

	try:
		hist=paginator.page(page)
	except PageNotAnInteger:
		hist=paginator.page(1)
	except EmptyPage:
		hist=paginator.page(paginator.num_pages)

	return render(request,'dashboard/received_money_history.html',{'history':hist,'exist':exist})



def send_money(request):
	exist = check_exist_or_not(request)
	if (not exist):
		return redirect('add_premium_plan')
	return render(request,'dashboard/send-fund.html',{'exist':exist})




