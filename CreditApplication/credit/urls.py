from django.urls import path
from django.conf.urls import include
from credit import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "credit"

urlpatterns = format_suffix_patterns([
    path("", views.api_root, name='root'),
    path("customer-list/", views.CustomerListView.as_view(), name="customerprofile-list"),
    path("customer-list/<int:id>/", views.CustomerDetailView.as_view(), name="customerprofile-detail"),
    path("proposal-list/", views.CreditProposalView.as_view(), name="creditproposal-list"),
    path("proposal-list/<int:id>/", views.CreditProposalDetailView.as_view(), name="creditproposal-detail"),
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
])
