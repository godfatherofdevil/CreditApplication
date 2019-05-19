from django.contrib import admin
from django.contrib.auth import get_user_model

from credit.models import CreditProposal, CustomerProfile, CreditApplication

admin.site.register(CreditApplication)
admin.site.register(CreditProposal)
admin.site.register(CustomerProfile)
