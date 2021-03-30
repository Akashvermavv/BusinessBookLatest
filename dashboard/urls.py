
from django.urls import path,include
from django.views.generic import TemplateView
from . import views


urlpatterns = [
	path('',views.dashboard,name='dashboard'),
	path('test',views.test,name='test'),
	path('add_fund/',views.add_fund,name='add_fund'),
	path('add_premium_plan/',views.add_premium_plan,name='add_premium_plan'),
	path('premium_plan_success/',views.premium_plan_success,name='premium_plan_success'),
	path('payment_success/',views.payment_success,name='payment_success'),
	path('payment_failed/',views.payment_failed,name='payment_failed'),
	path('payment_status/',views.payment_status,name='payment_status'),
	# path('send_money/',TemplateView.as_view(template_name='dashboard/send-fund.html'),name='send_money'),
	path('send_money/',views.send_money,name='send_money'),
	path('balance_transfer/',views.balance_transfer,name='balance_transfer'),
	path('adpack_list/',views.adpack_list,name='adpack_list'),
	path('refer/',views.refer_page,name='refer'),
	path('buy_adpack/<int:level>/',views.buy_adpack,name='buy_adpack'),
	path('refer_list/',views.refer_list,name='refer_list'),
	path('revenue_history/',views.revenue_history,name='revenue_history'),
	path('adpack_history/',views.adpack_history,name='adpack_history'),
	path('personal_info/<int:pk>/',views.personal_info.as_view(),name='personal_info_update'),
	path('payment_info/',views.payment_info,name='payment_info'),
	path('pm_add/',views.pm_add,name='pm_add'),
	path('agent_account_add/',views.agent_account_add,name='agent_account_add'),
	path('bank_info_add/',views.bank_info_add,name='bank_info_add'),
	path('withdraw/',views.withdraw,name='withdraw'),
	path('withdraw/',views.withdraw_premium_plan,name='withdraw_premium_plan'),
	path('withdraw_request_premium/',views.withdraw_request_premium,name='withdraw_request_premium'),
	path('withdraw_request/',views.withdraw_request,name='withdraw_request'),
	path('change_password/',views.change_password,name='change_password'),
	path('withdraw_history/',views.withdraw_history,name='withdraw_history'),
	path('deposits_history/',views.deposits_history,name='deposits_history'),
	path('sendmoney_history/',views.send_Money_history,name='sendmoney_history'),
	path('receivedmoney_history/',views.receivedmoney_history,name='receivedmoney_history'),
	path('bkash_add/',views.bkash_add,name='bkash_add'),
	path('rocket_add/',views.rocket_add,name='rocket_add'),
	path('nagad_add/',views.nagad_add,name='nagad_add'),

	]
    
