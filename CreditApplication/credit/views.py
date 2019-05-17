from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q

from rest_framework import filters
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from credit.models import CustomerProfile, CreditProposal, CreditApplication, CreditUser
from credit.serializers import (
    CustomerProfileSerializer, CreditUserSerializer, CreditProposalSerializer, CreditApplicationSerializer,
    CreateApplicationSerializer, CreateCustomerSerializer, CreateProposalSerializer, CreateCreditUserSerializer
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
        context = {
        'applications': reverse('credit:creditapplication-list', request=request, format=format)
        }
    else:
        context = {
            'Message': "You are not permitted to access this API, login to continue"
        }
    
    return Response(context)

# This view returns customer profiles in system based on current logged in user
class CustomerListView(generics.ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('id', 'first_name', 'last_name')
    ordering_fields = ('id', 'first_name', 'last_name')

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CustomerProfile.objects.all()
        return CustomerProfile.objects.all().filter(owner=self.request.user)

# This view returns the detail of a particular customer profile based on current logged in user
class CustomerDetailView(generics.RetrieveAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes=(IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CustomerProfile.objects.all()
        return CustomerProfile.objects.all().filter(owner=self.request.user)


class CreditUserListView(generics.ListAPIView):
    queryset = CreditUser.objects.all()
    serializer_class = CreditUserSerializer

class CreditUserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CreditUser.objects.all()
    serializer_class = CreditUserSerializer

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

# This view returns details of a particular proposal based on current logged in user
class CreditProposalDetailView(generics.RetrieveAPIView):
    queryset = CreditProposal.objects.all()
    serializer_class = CreditProposalSerializer

    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CreditProposal.objects.all()
        return CreditProposal.objects.all().filter(owner=self.request.user)

class CreditApplicationView(generics.ListAPIView):
    queryset = CreditApplication.objects.all()
    serializer_class = CreditApplicationSerializer
    """
    TO DO - CreditApplication Model don't have an owner which is going to make trouble
    Add owner field for this model so that appropriate permissions and authentications can be applied
    on the objects of this model
    """
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return CreditApplication.objects.all()
        return CreditApplication.objects.all().filter(owner=self.request.user)

class CreditApplicationDetailView(generics.RetrieveUpdateAPIView):
    queryset = CreditApplication.objects.all()
    serializer_class = CreditApplicationSerializer

class CreateApplicationView(generics.ListCreateAPIView):
    queryset = CreditApplication.objects.all()
    serializer_class = CreateApplicationSerializer

class ModifyApplicationView(generics.RetrieveUpdateAPIView):
    queryset = CreditApplication.objects.all()
    serializer_class = CreateApplicationSerializer

class CreateCustomerView(generics.ListCreateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CreateCustomerSerializer

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        return super(CreateCustomerView, self).perform_create(serializer)

class ModifyCustomerView(generics.RetrieveUpdateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CreateCustomerSerializer

class CreateProposalView(generics.ListCreateAPIView):
    queryset = CreditProposal.objects.all()
    serializer_class = CreateProposalSerializer

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        return super(CreateProposalView, self).perform_create(serializer)

class ModifyProposalView(generics.RetrieveUpdateAPIView):
    queryset = CreditProposal.objects.all()
    serializer_class = CreateProposalSerializer

class CreateCreditUserView(generics.ListCreateAPIView):
    queryset = CreditUser.objects.all()
    serializer_class = CreateCreditUserSerializer