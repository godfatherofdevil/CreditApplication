from django.urls import path
from django.conf.urls import include
from credit import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "credit"

urlpatterns = format_suffix_patterns([
    path("", views.api_root, name='partner'),
    path("customer-list/", views.CustomerListView.as_view(), name="customerprofile-list"),
    path("proposal-list/", views.CreditProposalView.as_view(), name="creditproposal-list"),
    path("application-list/", views.CreditApplicationView.as_view(), name="creditapplication-list"),
    path("user-list/", views.CreditUserListView.as_view(), name="credituser-list"),
    path("user-list/<int:id>/", views.CreditUserDetailView.as_view(), name="credituser-detail"),
    path("create-application/", views.CreateApplicationView.as_view(), name="create-application"),
    path("create-application/<int:pk>/", views.ModifyApplicationView.as_view(), name="modify-application"),
    path('create-customer/', views.CreateCustomerView.as_view(), name='create-customer'),
    path('create-customer/<int:pk>/', views.ModifyCustomerView.as_view(), name="modify-customer"),
    path('create-proposal/', views.CreateProposalView.as_view(), name="create-proposal"),
    path('create-proposal/<int:pk>/', views.ModifyProposalView.as_view(), name='modify-proposal'),
    path('create-user/', views.CreateCreditUserView.as_view(), name="create-user"),
    path('credit-organization/', views.CreditOrganizationView.as_view(), name="credit-organization"),
    path('credit-organization/<int:pk>', views.CreditOrganizationModify.as_view(), name="modify-status"),
])
