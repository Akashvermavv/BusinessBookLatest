from django.db import models
from accounts.models import User

from decimal import Decimal

# Create your models here.

class CampaignCategory(models.Model):
  title = models.CharField(max_length=30)

class Campaign(models.Model):
  user = models.ForeignKey(User,null=True,blank=True,on_delete = models.CASCADE)
  category = models.ForeignKey(CampaignCategory, on_delete = models.CASCADE)
  topic = models.IntegerField(null=True,blank=True)
  title = models.CharField(max_length=30)
  description = models.TextField()
  required_proof = models.TextField()
  cam_image = models.ImageField(upload_to='campaign_images', blank=True,default='abc')
  earn = models.DecimalField(max_digits=20, decimal_places=4, default=0.0)
  
  need_worker_amount = models.IntegerField()
  STATUS_CHOICES = [
      ('Completed', 'Approaved'),
      ('Declined', 'Declined'),
      ('Waiting for confirmation', 'Waiting for confirmation'),
      ('Running', 'Running'),

  ]
  status = models.CharField(choices=STATUS_CHOICES, max_length=100, default='Waiting for confirmation')

  def __str__(self):
      return f'{self.user.first_name+" "+self.user.last_name} Applied'


class Applicants(models.Model):
    STATUS_CHOICES = [
    ('Approaved', 'Approaved'),
    ('Declined', 'Declined'),
    ('Waiting for confirmation', 'Waiting for confirmation'),
    ('Not applied', 'Not applied'),

    ]
    user = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign,null=True,blank=True, on_delete=models.CASCADE, related_name='applicants')
    document = models.FileField(upload_to='documents/', null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default='Not applied')
    def __str__(self):
      return f'{self.user.first_name+" "+self.user.last_name} Applied'
