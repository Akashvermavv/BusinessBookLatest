
from django.urls import path,include
from django.views.generic import TemplateView
from . import views


urlpatterns = [
	path('add_campaign/',views.add_campaign, name='add_campaign'),
	path('get_your_campaign/',views.get_your_campaign, name='get_your_campaign'),
	path('get_job_list/',views.get_job_list, name='get_job_list'),
	path('get_finished_job_list/',views.FinishedJobListView.as_view(), name='get_finished_job_list'),
	path('get_your_campaign_list/',views.YourCampaignListView.as_view(), name='get_your_campaign_list'),
	path('apply_campaign/<int:pk>/',views.ApplyCampaign.as_view(), name='apply_campaign'),
	path('job-applicant-list/<int:pk>/',views.JobApplicantListView.as_view(), name='job-applicant-list'),

	]
    
