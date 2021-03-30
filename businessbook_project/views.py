from django.shortcuts import render,redirect

import requests
import json
from django.contrib import auth
from dashboard.models import bought_adpack,balance
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password
from django.db.models import Q,Avg,Sum

def home(request):
    expired_adpacks = bought_adpack.objects.filter(
        Q(expiration_date__lt=datetime.now())

    )
    for ob in expired_adpacks:
        ob.delete()

    total_active_adpacks1 = bought_adpack.objects.filter(Q(expiration_date__gt=datetime.now()) )
    if (total_active_adpacks1.exists()):
        for obje in total_active_adpacks1:
            # bal+=obje.everyday_revenue
            try:
                if (obje.last_benefit_date != datetime.now().date()):
                    # print('in home @@@@@',obje.user)
                    balll = balance.objects.get(user=obje.user)

                    balll.current_balance = round(balll.current_balance + obje.everyday_revenue, 2)
                    balll.save()
                    obje.last_benefit_date = datetime.now().date()
                    obje.save()
            except:
                balll = 0

    return render(request,'index.html',{})