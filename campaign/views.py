from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator

from businessbook_project import settings
from .models import *
from accounts.models import User
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from campaign.models import CampaignCategory
from .forms import campaign_form,applicant_form
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

# Create your views here.

@login_required(login_url='/accounts/login/')
@csrf_exempt
def add_campaign(request):
    try:
        category = CampaignCategory.objects.all()
        if request.method == 'GET':
            form = campaign_form()
            return render(request, 'campaign/add_campaign.html', {"category": category,'form':form})
        if request.method == 'POST':

            form = campaign_form(request.POST,request.FILES or None)

            if form.is_valid():
                # fs=FileSystemStorage(location=settings.MEDIA_ROOT)
                # request_file = request.FILES['myfile'] if 'myfile' in request.FILES else None
                # file = fs.save(request_file.name, request_file)
                att=form.save(commit=False)
                att.category=CampaignCategory.objects.filter(id=request.POST.get('category')[0]).first()
                att.user=request.user
                # att.document=fs.url(file)
                att.title = request.POST.get('title')
                att.description = request.POST.get('description')
                att.required_proof = request.POST.get('required_proof')
                att.earn = request.POST.get('earn')

                att.topic=request.POST.get('topic')
                att.need_worker_amount=request.POST.get('need_worker_amount')
                att.save()
    except Exception as ex:
        print(ex)
    return render(request, 'campaign/add_campaign.html', {"category": category})


@login_required(login_url='/accounts/login/')
@csrf_exempt
def get_your_campaign(request):
    campaign = Campaign.objects.all()
    if request.method == 'GET':
        return render(request, 'campaign/your_campaign.html', {"campaign": campaign})


# @login_required(login_url='/accounts/login/')
# @csrf_exempt
# def get_jobs_list(request, slug='search'):
#     campaign = Campaign.objects.all()
#     if request.method == 'GET':
#         return render(request, 'campaign/post_list.html', {"campaign": campaign})
#




class ApplyCampaign(View):
    @method_decorator(csrf_exempt)
    def get(self, request, *args, **kwargs):

         # Applicants(user=request.user, campaign=Campaign.objects.filter(id=self.kwargs['pk']).first()).save()
         template_name="campaign/apply_campaign.html"
         context={"campaign":Campaign.objects.filter(id=self.kwargs['pk']).first()}
         print(context['campaign'].description)
         return render(request, template_name, context)

    def post(self,request,*args,**kwargs):
        fs=FileSystemStorage(location=settings.MEDIA_ROOT)
        request_file = request.FILES['myfile'] if 'myfile' in request.FILES else None
        file = fs.save(request_file.name, request_file)
        att = Applicants()
        att.category = CampaignCategory.objects.filter(id=self.kwargs['pk']).first()
        att.user = request.user
        att.campaign = Campaign.objects.get(id=kwargs["pk"])
        att.document=fs.url(file)
        att.save()
        return HttpResponseRedirect('/campaign/get_job_list/')

@login_required(login_url='/accounts/login/')
@csrf_exempt
def get_job_list(request):
    try:
        template_name = 'campaign/job_list.html'
        campaign_list = Campaign.objects.filter(~Q(applicants__user=request.user))
        query = request.GET.get('q', '')
        checked_category = request.GET.get('category', '')
        if query != '' and checked_category != '':
            campaign_list = Campaign.objects.filter(
                Q(title__icontains=query) | Q(category__title__icontains=checked_category)
            ).filter(~Q(applicants__user=request.user)).distinct()
        elif query!='' and checked_category=='':
            campaign_list = Campaign.objects.filter(
                Q(title__icontains=query)
            ).filter(~Q(applicants__user=request.user)).distinct()
        elif query =='' and checked_category!='':
            campaign_list = Campaign.objects.filter(
                Q(category__title__icontains=checked_category)
            ).filter(~Q(applicants__user=request.user)).distinct()
        paginator = Paginator(campaign_list, 6)
        page = request.GET.get('page', 1)

        try:
            campaign= paginator.page(page)
        except PageNotAnInteger:
            campaign = paginator.page(1)
        except EmptyPage:
            campaign = paginator.page(paginator.num_pages)

        context = {"campaign": campaign,'all_category':CampaignCategory.objects.all()}
        return render(request, template_name, context)
    except Exception as ex:
        print(ex)
        return None



class FinishedJobListView(ListView):
    model = Applicants      # shorthand for setting queryset = models.Car.objects.all()
    template_name = 'campaign/finished_job_list.html'  # optional (the default is app_name/modelNameInLowerCase_list.html; which will look into your templates folder for that path and file)
    context_object_name = "finished_job_list"    #default is object_list as well as model's_verbose_name_list and/or model's_verbose_name_plural_list, if defined in the model's inner Meta class
    paginate_by = 2  #and that's it !!

    def get_queryset(self):
        return Applicants.objects.filter(user=self.request.user)

class YourCampaignListView(ListView):
    model = Campaign      # shorthand for setting queryset = models.Car.objects.all()
    template_name = 'campaign/your_campaigncategory_list.html'  # optional (the default is app_name/modelNameInLowerCase_list.html; which will look into your templates folder for that path and file)
    context_object_name = "campaign_list"    #default is object_list as well as model's_verbose_name_list and/or model's_verbose_name_plural_list, if defined in the model's inner Meta class
    paginate_by = 2  #and that's it !!

    def get_queryset(self):
        campaign_list=Campaign.objects.filter(user=self.request.user)
        for campaign in campaign_list:
            print(campaign.title)
        return Campaign.objects.filter(user=self.request.user)

class JobApplicantListView(ListView):
    model = Applicants      # shorthand for setting queryset = models.Car.objects.all()
    template_name = 'campaign/applicant_list.html'  # optional (the default is app_name/modelNameInLowerCase_list.html; which will look into your templates folder for that path and file)
    context_object_name = "applicant_list"    #default is object_list as well as model's_verbose_name_list and/or model's_verbose_name_plural_list, if defined in the model's inner Meta class
    paginate_by = 10  #and that's it !!

    def get_queryset(self):
        applicant_list = Applicants.objects.filter(campaign=self.kwargs['pk']).values("user__email", "id", "document", "status")
        return applicant_list
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        status = request.POST.get("status")
        if(status == "Not applied"):
            status = "Approved"
        elif(status == "Approved"):
            status = "Declined"
        elif(status == "Declined"):
            status = "Approved"


        applicant = Applicants.objects.get(id=request.POST.get("id"))
        applicant.status = status
        applicant.save()
     
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


