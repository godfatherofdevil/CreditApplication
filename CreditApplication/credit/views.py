from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework import filters
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from credit.models import CustomerProfile, CreditProposal, CreditApplication
from credit.serializers import (
    CustomerProfileSerializer, CreditUserSerializer, CreditProposalSerializer, CreditApplicationSerializer,
    CreateApplicationSerializer, CreateCustomerSerializer, CreateProposalSerializer, CreateCreditUserSerializer,
    CreditOrganizationSerializer
)
from credit.permissions import HasGroupPermission

@api_view(['GET'])
@authentication_classes((SessionAuthentication,BasicAuthentication))
def api_root(request, format=None):
    if request.user.is_staff:
        context = {
        'customers': reverse('credit:customerprofile-list', request=request, format=format),
        'proposals': reverse('credit:creditproposal-list', request=request, format=format),
        'applications': reverse('credit:creditapplication-list', request=request, format=format),
        'users': reverse('credit:credituser-list', request=request, format=format),
        'create-application': reverse('credit:create-application', request=request, format=format),
        'create-customer': reverse('credit:create-customer', request=request, format=format),
        'create-proposal': reverse('credit:create-proposal', request=request, format=format),
        'create-user': reverse('credit:create-user', request=request, format=format)
        }
    elif request.user.groups.all().filter(name="partner"):
        context = {
        'customers': reverse('credit:customerprofile-list', request=request, format=format),
        'proposals': reverse('credit:creditproposal-list', request=request, format=format),
        'applications': reverse('credit:creditapplication-list', request=request, format=format),
        'create-application': reverse('credit:create-application', request=request, format=format),
        'create-customer': reverse('credit:create-customer', request=request, format=format),
        'create-proposal': reverse('credit:create-proposal', request=request, format=format),
        }
    elif request.user.groups.all().filter(name="credit_organization"):
        context ={
            'view-applications': reverse('credit:credit-organization', request=request, format=format)
        }
    else:
        context = {
            'Unauthorised': "You are not permitted to access this API, login to continue"
        }
    
    return Response(context)

class CreditOrganizationView(generics.ListAPIView):
    queryset = CreditApplication.objects.all()
    serializer_class = CreditOrganizationSerializer
    permission_classes = (IsAuthenticated, HasGroupPermission)

    required_groups = {
        'GET': ['credit_organization'],
    }

class CreditOrganizationModify(generics.RetrieveUpdateAPIView):
    queryset = CreditApplication.objects.all()
    serializer_class = CreditOrganizationSerializer
    permission_classes = (IsAuthenticated,HasGroupPermission)

    required_groups = {
        'GET': ['credit_organization'],
        'PUT': ['credit_organization'],
    }

# This view returns customer profiles in system based on current logged in user
class CustomerListView(generics.ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = (IsAuthenticated, HasGroupPermission)
    required_groups = {
        'GET': ['partner'],
    }

    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('id', 'first_name', 'last_name')
    ordering_fields = ('id', 'first_name', 'last_name')

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CustomerProfile.objects.all()
        return CustomerProfile.objects.all().filter(owner=self.request.user)

class CreditUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = CreditUserSerializer
    permission_classes = (IsAdminUser,)

class CreditUserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CreditUserSerializer
    permission_classes = (IsAdminUser,)

    lookup_field = "id"

# This view returns list of all proposal based on current logged in user
class CreditProposalView(generics.ListAPIView):
    queryset = CreditProposal.objects.all()
    serializer_class = CreditProposalSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CreditProposal.objects.all()
        return CreditProposal.objects.all().filter(owner=self.request.user)

class CreditApplicationView(generics.ListAPIView):
    queryset = CreditApplication.objects.all()
    serializer_class = CreditApplicationSerializer
    permission_classes = (IsAuthenticated, HasGroupPermission)
    required_groups = {
        'GET': ['partner'],
    }
    """
    TO DO - CreditApplication Model don't have an owner which is going to make trouble
    Add owner field for this model so that appropriate permissions and authentications can be applied
    on the objects of this model
    """
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CreditApplication.objects.all()
        elif self.request.user.groups.all().filter(name="credit_organization"):
            assigned_organization = User.objects.filter(username=self.request.user)[0]
            return CreditApplication.objects.filter(
                credit_proposal__credit_agency=assigned_organization
            )
        
        return CreditApplication.objects.all().filter(owner=self.request.user)

class CreateApplicationView(generics.ListCreateAPIView):
    queryset = CreditApplication.objects.all()
    serializer_class = CreateApplicationSerializer
    permission_classes = (IsAuthenticated, HasGroupPermission)
    required_groups = {
        'GET': ['partner'],
        'POST': ['partner'],
    }

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CreditApplication.objects.all()
        return CreditApplication.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        return super(CreateApplicationView, self).perform_create(serializer)

class ModifyApplicationView(generics.RetrieveUpdateAPIView):
    queryset = CreditApplication.objects.all()
    serializer_class = CreateApplicationSerializer
    permission_classes = (IsAuthenticated, HasGroupPermission)
    required_groups = {
        'GET': ['partner'],
        'PUT': ['partner']
    }

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CreditApplication.objects.all()
        return CreditApplication.objects.all().filter(owner=self.request.user)

class CreateCustomerView(generics.ListCreateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CreateCustomerSerializer
    permission_classes = (IsAuthenticated,HasGroupPermission)
    required_groups = {
        'GET': ['partner'],
        'POST': ['partner'],
    }
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CustomerProfile.objects.all()
        return CustomerProfile.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        return super(CreateCustomerView, self).perform_create(serializer)

class ModifyCustomerView(generics.RetrieveUpdateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CreateCustomerSerializer
    permission_classes = (IsAuthenticated, HasGroupPermission)
    required_groups = {
        'GET': ['partner'],
        'PUT': ['partner'],
    }

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CustomerProfile.objects.all()
        return CustomerProfile.objects.all().filter(owner=self.request.user)

class CreateProposalView(generics.ListCreateAPIView):
    queryset = CreditProposal.objects.all()
    serializer_class = CreateProposalSerializer
    permission_classes = (IsAuthenticated, HasGroupPermission)
    required_groups = {
        'GET': ['partner'],
        'POST': ['partner'],
    }

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CreditProposal.objects.all()
        return CreditProposal.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        return super(CreateProposalView, self).perform_create(serializer)

class ModifyProposalView(generics.RetrieveUpdateAPIView):
    queryset = CreditProposal.objects.all()
    serializer_class = CreateProposalSerializer
    permission_classes = (IsAuthenticated, HasGroupPermission)
    required_groups = {
        'GET': ['partner'],
        'PUT': ['partner'],
    }

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CreditProposal.objects.all()
        return CreditProposal.objects.all().filter(owner=self.request.user)


class CreateCreditUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateCreditUserSerializer
    permission_classes = (IsAdminUser,)