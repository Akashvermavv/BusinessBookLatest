from django.db import models
from accounts.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class balance(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	current_balance=models.FloatField(max_length=9,default=0.0)

	def __str__(self):
		return str(self.user.email)


class refer(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
	referer=models.IntegerField(null=True,blank=True)
	refer_earn=models.FloatField(blank=True,null=True,default=0)

	def __str__(self):
		return str(self.user.email)


class adpack(models.Model):
	title =  models.CharField(max_length=40)
	value = models.IntegerField()
	level = models.IntegerField(null=True)
	image = models.ImageField(upload_to='adpack-image/')
	perday_revenue = models.FloatField(null=True)
	expiration_day = models.IntegerField(default=60,null=True)
	affiliate_earn = models.FloatField(null=True)
	total_return = models.FloatField(null=True)
	max_buy = models.IntegerField(null=True)

	def __str__(self):
		return str(self.title)



class bought_adpack(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	buying_date=models.DateField(null=False,default=timezone.now)
	expiration_date=models.DateField()
	total_quantity=models.IntegerField()
	bought_adpacks=models.ForeignKey(adpack,on_delete=models.CASCADE)
	adpack_totalreturn=models.FloatField()
	everyday_revenue=models.FloatField()
	affiliate_commission=models.FloatField()
	total_price=models.FloatField()
	last_benefit_date =models.DateField(default=timezone.now)


	def __str__(self):
		return str(self.bought_adpacks.title)



class adpack_update(models.Model):
	date=models.DateField(default=timezone.now)
	bought_adpack_name=models.ForeignKey(bought_adpack,on_delete=models.CASCADE)
	today_revenue=models.FloatField()

	def __str__(self):
		return str(self.bought_adpack_name)


class pm_accounts(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	pm_account = models.CharField(max_length=25,blank=True,null=True)


	def __str__(self):
		return self.user.email

	class Meta:
		verbose_name='user perfectMoney accounts'
		verbose_name_plural='user perfectMoney accounts'

class agent_accounts(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	agent_email = models.EmailField(max_length=25)

	def __str__(self):
		return self.user.email

	class Meta:
		verbose_name='user agent accounts'
		verbose_name_plural='user agent accounts'

class bank_accounts(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	account_type=models.CharField(max_length=30,null=True,blank=True)
	account_number=models.CharField(max_length=60,null=True,blank=True)
	account_holder_name=models.CharField(max_length=40,blank=True,null=True)
	bank_name = models.CharField(max_length=40,blank=True,null=True)
	branch_name=models.CharField(max_length=30,blank=True,null=True)
	ifsc_code = models.CharField(max_length=40,blank=True,null=True)
	description = models.CharField(max_length=100,blank=True,null=True)




	def __str__(self):
		return self.user.email

	class Meta:
		verbose_name='user bank accounts'
		verbose_name_plural='user bank accounts'




class withdraw_requests(models.Model):
	date=models.DateField(default=timezone.now)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	method=models.CharField(max_length=40)
	amount=models.FloatField()
	payment_done=models.BooleanField(default=False)
	payment_error=models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.email)

	class Meta:
		verbose_name='user withdraw requests'
		verbose_name_plural='user withdraw requests'



class deposit_history(models.Model):
	date=models.DateField(default=timezone.now)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	method=models.CharField(max_length=40,default='PerfectMoney')
	amount=models.FloatField()
	

	def __str__(self):
		return str(self.user.email)

	class Meta:
		verbose_name='user deposit history'
		verbose_name_plural='user deposit history'


class send_money_history(models.Model):
	date=models.DateField(default=timezone.now)
	sent_from = models.ForeignKey(User,on_delete=models.CASCADE)
	sent_to = models.EmailField(blank=False,null=False)
	sent_amount = models.FloatField(blank=False,null=False)

	def __str__(self):
		return str(self.sent_from)



class bkash_accounts(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	bkash_number = models.CharField(max_length=25,blank=True,null=True)


	def __str__(self):
		return self.user.email

	class Meta:
		verbose_name='user bkash numbers'
		verbose_name_plural='user bkash numbers'



class rocket_accounts(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	rocket_number = models.CharField(max_length=25,blank=True,null=True)


	def __str__(self):
		return self.user.email

	class Meta:
		verbose_name='user rocket numbers'
		verbose_name_plural='user rocket numbers'


class nagad_accounts(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	nagad_number = models.CharField(max_length=25,blank=True,null=True)


	def __str__(self):
		return self.user.email

	class Meta:
		verbose_name='user nagad numbers'
		verbose_name_plural='user nagad numbers'
		
class PremiumPlan(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	plan = models.BooleanField(default=False)

	def __str__(self):
		return self.user.email
		


