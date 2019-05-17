from django.contrib import admin
from django.contrib.auth import get_user_model

from credit.models import CreditUser, CreditProposal, CustomerProfile, CreditApplication

admin.site.register(CreditUser)
admin.site.register(CreditApplication)
admin.site.register(CreditProposal)
admin.site.register(CustomerProfile)
