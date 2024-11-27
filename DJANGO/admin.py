from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry  # Import the LogEntry model
from .models import *

# Unregister the LogEntry model from the admin site
# admin.site.unregister(LogEntry)



class OtpTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code")

admin.site.register(OtpToken, OtpTokenAdmin)

from django.contrib import admin
from .models import LoanApplication

class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'new_credit_customer', 'verification_type', 'age', 'gender', 'applied_amount', 'amount', 'use_of_loan',
        'employment_status', 'employment_duration', 'occupation_area', 'home_ownership_type', 'total_income',
        'total_liabilities', 'debt_to_income', 'free_cash', 'rating', 'credit_score_es_micro_l', 'credit_score_ee_mini',
        'no_of_previous_loans', 'amount_of_previous_loans', 'id'
    )
    search_fields = ('new_credit_customer', 'verification_type', 'gender', 'use_of_loan', 'rating')
    list_filter = ('new_credit_customer', 'verification_type', 'employment_status', 'rating', 'gender')
    ordering = ('-id',)  # Show the most recent loan applications first
    list_per_page = 20  # Limit the number of items per page

# Register the model with the custom admin interface
admin.site.register(LoanApplication, LoanApplicationAdmin)

