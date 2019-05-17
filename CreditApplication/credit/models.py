from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from CreditApplication.middleware import local

# model for credit proposal
class CreditProposal(models.Model):
    CREDIT_TYPE_CHOICES = (
        ('0', 'consumption'), 
        ('1', 'mortgage'), 
        ('2','car'),
        )

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    rotation_start = models.DateTimeField()
    rotation_end = models.DateTimeField()
    name = models.CharField(max_length=200)
    credit_type = models.CharField(max_length=50, choices=CREDIT_TYPE_CHOICES, default='0')
    min_score = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    credit_agency = models.ForeignKey('CreditUser', null=True, on_delete=models.SET_NULL, related_name="credit_agency")
    # set the owner of the proposal
    owner = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, related_name="owner")

    def get_absolute_url(self):
        return reverse("credit:creditproposal-detail", args=[str(self.id)])

    # def save(self, *args, **kwargs):
    #     if self.pk is None and hasattr(local, 'credituser'):
    #         self.owner = local.credituser
    #     return super(CreditProposal, self).save(*args, **kwargs)
    

class CustomerProfile(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    last_name = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, blank=True)
    date_birth = models.DateField(blank=False)
    passport_number = models.CharField(max_length=15, blank=False)
    score = models.PositiveIntegerField()
    partner = models.ForeignKey('CreditUser', null=True, on_delete=models.SET_NULL, related_name='credituser')
    # set the owner of the customer
    owner = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, related_name="owner_customer")

    def get_absolute_url(self):
        return reverse("credit:customerprofile-detail", args=[str(self.id)])
    

class CreditApplication(models.Model):
    STATUS_CHOICES = (
        ('0', 'new'), 
        ('1', 'sent'), 
        ('2', 'recieved'), 
        ('3', 'approved'), 
        ('4', 'refused'), 
        ('5', 'issued'),
        )

    created_on = models.DateTimeField(auto_now_add=True)
    sent_on = models.DateTimeField(null=True, default=None)
    customer_profile = models.ForeignKey('CustomerProfile', null=True, on_delete=models.SET_NULL, related_name='customer_profile')
    credit_proposal = models.ForeignKey('CreditProposal', null=True, on_delete=models.SET_NULL, related_name='credit_proposal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='0')

# CreditUser model is our custom user model which will be used for role seperation
# of our users (superuser, partners, credit organizations)

class CreditUser(models.Model):
    CREDIT_USER_TYPES = (
        ('0', 'superuser'), 
        ('1', 'partner'), 
        ('2', 'credit_organization'),
        )
    
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=CREDIT_USER_TYPES, blank=False, default='0')

    def get_absolute_url(self):
        return reverse("credit:credituser-detail", args=[str(self.id)])

    def __str__(self):
        return self.user.username
    
    

