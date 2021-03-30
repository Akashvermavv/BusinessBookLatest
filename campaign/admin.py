from django.contrib import admin

# Register your models here.
from .models import CampaignCategory,Campaign,Applicants

admin.site.register(CampaignCategory)
admin.site.register(Campaign)
admin.site.register(Applicants)
