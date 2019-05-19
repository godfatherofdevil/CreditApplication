from rest_framework import serializers
from django.contrib.auth.models import User, Group

from credit.models import CreditApplication, CreditProposal, CustomerProfile

class CustomerProfileSerializer(serializers.ModelSerializer):
    customer_detail = serializers.HyperlinkedIdentityField(view_name="credit:modify-customer")
    partner = serializers.HyperlinkedRelatedField(
        view_name='credit:credituser-detail', read_only=True, lookup_field="id"
        )
    class Meta:
        model = CustomerProfile
        fields = (
            "customer_detail","id", "created_on", "modified_on", "last_name", "first_name", "middle_name",
            "date_birth", "passport_number", "score", "partner"
            )

class CreditUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "is_staff")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

class CreditProposalSerializer(serializers.ModelSerializer):
    proposal_detail = serializers.HyperlinkedIdentityField(view_name="credit:modify-proposal")
    # create custom field for hyeprlinking credit agency details associated with any particular proposal
    credit_agency = serializers.HyperlinkedRelatedField(
        view_name="credit:credituser-detail", read_only=True, lookup_field="id"
        )
    class Meta:
        model = CreditProposal

        fields = (
            "proposal_detail", "rotation_start", "rotation_end","name", "credit_type", 
            "min_score", "max_score", "credit_agency", "owner"
        )

class CreditApplicationSerializer(serializers.ModelSerializer):
    application_detail = serializers.HyperlinkedIdentityField(view_name="credit:modify-application")
    customer_profile = serializers.HyperlinkedRelatedField(
        view_name="credit:modify-customer" , read_only=True
    )
    credit_proposal = serializers.HyperlinkedRelatedField(
        view_name="credit:modify-proposal" , read_only=True
    )
    class Meta:
        model = CreditApplication

        fields = ( 
            "application_detail", "sent_on", "customer_profile", "credit_proposal", "status",
        )

class CreateApplicationSerializer(serializers.ModelSerializer):

    application_detail = serializers.HyperlinkedIdentityField(view_name="credit:modify-application")
    class Meta:
        model = CreditApplication

        fields = ("application_detail", "sent_on", "customer_profile", "credit_proposal", "status")

class CreateCustomerSerializer(serializers.ModelSerializer):

    customer_detail = serializers.HyperlinkedIdentityField(view_name="credit:modify-customer")
    """
    While adding a new customer, we want only those users who belong to 'partner' group
    We do this below by overriding __init__ method
    """
    def __init__(self, *args, **kwargs):
        # get the users who belong to 'partner' group
        partner = User.objects.filter(groups__name='partner')

        super(CreateCustomerSerializer, self).__init__(*args, **kwargs)
        self.fields['partner'].queryset = partner
    
    class Meta:
        model = CustomerProfile

        fields = (
            'customer_detail', 'last_name', 'first_name', 'middle_name', 'date_birth',
            'passport_number', 'score', 'partner'
            )

class CreateProposalSerializer(serializers.ModelSerializer):

    proposal_detail = serializers.HyperlinkedIdentityField(view_name="credit:modify-proposal")

    """
    While adding a proposal we only want the users which are part of 'credit_organization' group
    We do this by overriding __init__ method below
    """
    def __init__(self, *args, **kwargs):
        # get the users who belong to 'credit_organization' group
        credit_agency = User.objects.filter(groups__name='credit_organization')

        super(CreateProposalSerializer, self).__init__(*args, **kwargs)
        self.fields['credit_agency'].queryset = credit_agency
    
    class Meta:
        model = CreditProposal

        fields = (
            "proposal_detail", "rotation_start", "rotation_end", "name", "credit_type",
            "min_score", "max_score", "credit_agency"
        )

class CreateCreditUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = ('username', 'first_name', "last_name", "is_staff")

class CreditOrganizationSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedRelatedField(view_name="credit:modify-status", read_only=True)
    class Meta:
        model = CreditApplication
        fields = ("id", "sent_on", "customer_profile", "credit_proposal", "status")
        depth = 1
        read_only_fields = ("sent_on","customer_profile", "credit_proposal")