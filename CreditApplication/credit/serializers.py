from rest_framework import serializers
from django.contrib.auth.models import User

from credit.models import CreditApplication, CreditProposal, CreditUser, CustomerProfile

class CustomerProfileSerializer(serializers.ModelSerializer):
    
    partner = serializers.HyperlinkedRelatedField(
        view_name='credit:credituser-detail', read_only=True, lookup_field="id"
        )
    class Meta:
        model = CustomerProfile
        fields = (
            "id", "created_on", "modified_on", "last_name", "first_name", "middle_name",
            "date_birth", "passport_number", "score", "partner"
            )

class CreditUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditUser
        fields = ("user", "user_type")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

class CreditProposalSerializer(serializers.ModelSerializer):

    # create custom field for hyeprlinking credit agency details associated with any particular proposal
    credit_agency = serializers.HyperlinkedRelatedField(
        view_name="credit:credituser-detail", read_only=True, lookup_field="id"
        )
    class Meta:
        model = CreditProposal

        fields = (
            "rotation_start", "rotation_end","name", "credit_type", 
            "min_score", "max_score", "credit_agency", "owner"
        )

class CreditApplicationSerializer(serializers.ModelSerializer):

    customer_profile = serializers.HyperlinkedRelatedField(
        view_name="credit:customerprofile-detail", read_only=True, lookup_field="id"
    )
    credit_proposal = serializers.HyperlinkedRelatedField(
        view_name="credit:creditproposal-detail", read_only=True, lookup_field="id"
    )
    class Meta:
        model = CreditApplication

        fields = ( 
            "sent_on", "customer_profile", "credit_proposal", "status",
        )

class CreateApplicationSerializer(serializers.ModelSerializer):

    application_detail = serializers.HyperlinkedIdentityField(view_name="credit:modify-application")
    class Meta:
        model = CreditApplication

        fields = ("application_detail", "sent_on", "customer_profile", "credit_proposal", "status")

class CreateCustomerSerializer(serializers.ModelSerializer):

    customer_detail = serializers.HyperlinkedIdentityField(view_name="credit:modify-customer")

    class Meta:
        model = CustomerProfile

        fields = (
            'customer_detail', 'last_name', 'first_name', 'middle_name', 'date_birth',
            'passport_number', 'score', 'partner'
            )

class CreateProposalSerializer(serializers.ModelSerializer):

    proposal_detail = serializers.HyperlinkedIdentityField(view_name="credit:modify-proposal")
    class Meta:
        model = CreditProposal

        fields = (
            "proposal_detail", "rotation_start", "rotation_end", "name", "credit_type",
            "min_score", "max_score", "credit_agency"
        )

class CreateCreditUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditUser

        fields = ('user', 'user_type')