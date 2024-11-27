from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import secrets



from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
import secrets
import datetime


class OtpToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otp_token")
    otp_code = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField()

    def __str__(self):
        return self.user.username
class LoanApplication(models.Model):
    NEW_CREDIT_CHOICES = [
        ('Existing_credit_customer', 'Existing_credit_customer'),
        ('New_credit_customer', 'New_credit_customer'),
    ]
    
    VERIFICATION_TYPE_CHOICES = [
        ('Income_expenses_verified', 'Income_expenses_verified'),
        ('Income_unverified', 'Income_unverified'),
        ('Income_verified', 'Income_verified'),
        ('Income_unverified_crossref_phone', 'Income_unverified_crossref_phone'),
        ('Not_set', 'Not_set'),
    ]
    
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Unknown', 'Unknown'),
    ]
    
    USE_OF_LOAN_CHOICES = [
        ('Home_improvement', 'Home_improvement'),
        ('Business', 'Business'),
        ('Other', 'Other'),
        ('Health', 'Health'),
        ('Vehicle', 'Vehicle'),
        ('Loan_consolidation', 'Loan_consolidation'),
        ('Travel', 'Travel'),
        ('Education', 'Education'),
        ('Real_estate', 'Real_estate'),
        ('Working_capital_financing', 'Working_capital_financing'),
        ('Accounts_receivable_financing', 'Accounts_receivable_financing'),
        ('Purchase_of_machinery_equipment', 'Purchase_of_machinery_equipment'),
        ('Other_business', 'Other_business'),
        ('Acquisition_of_real_estate', 'Acquisition_of_real_estate'),
        ('Construction_finance', 'Construction_finance'),
        ('Acquisition_of_stocks', 'Acquisition_of_stocks'),
        ('Not_set', 'Not_set'),
    ]
    
    EMPLOYMENT_STATUS_CHOICES = [
        ('Retiree', 'Retiree'),
        ('Entrepreneur', 'Entrepreneur'),
        ('Fully-Employed', 'Fully-Employed'),
        ('Partially-Employed', 'Partially-Employed'),
        ('Self-Employed', 'Self-Employed'),
        ('Unknown', 'Unknown'),
    ]
    
    EMPLOYMENT_DURATION_CHOICES = [
        ('0', '0'),
        ('MoreThan5Years', 'MoreThan5Years'),
        ('UpTo3Years', 'UpTo3Years'),
        ('UpTo5Years', 'UpTo5Years'),
        ('UpTo1Year', 'UpTo1Year'),
        ('UpTo2Years', 'UpTo2Years'),
        ('UpTo4Years', 'UpTo4Years'),
        ('TrialPeriod', 'TrialPeriod'),
    ]
    
    OCCUPATION_AREA_CHOICES = [
        ('Other', 'Other'),
        ('Retail_and_wholesale', 'Retail_and_wholesale'),
        ('Transport_and_warehousing', 'Transport_and_warehousing'),
        ('Hospitality_and_catering', 'Hospitality_and_catering'),
        ('Finance_and_insurance', 'Finance_and_insurance'),
        ('Research', 'Research'),
        ('Agriculture_forestry_and_fishing', 'Agriculture_forestry_and_fishing'),
        ('Healthcare_and_social_help', 'Healthcare_and_social_help'),
        ('Processing', 'Processing'),
        ('Construction', 'Construction'),
        ('Administrative', 'Administrative'),
        ('Real_estate', 'Real_estate'),
        ('Energy', 'Energy'),
        ('Education', 'Education'),
        ('Info_and_telecom', 'Info_and_telecom'),
        ('Civil_service_and_military', 'Civil_service_and_military'),
        ('Utilities', 'Utilities'),
        ('Art_and_entertainment', 'Art_and_entertainment'),
        ('Mining', 'Mining'),
        ('Not_specified', 'Not_specified'),
    ]
    
    HOME_OWNERSHIP_CHOICES = [
        ('Owner', 'Owner'),
        ('Mortgage', 'Mortgage'),
        ('Living_with_parents', 'Living_with_parents'),
        ('Tenant_pre_furnished_property', 'Tenant_pre_furnished_property'),
        ('Tenant_unfurnished_property', 'Tenant_unfurnished_property'),
        ('Joint_tenant', 'Joint_tenant'),
        ('Owner_with_encumbrance', 'Owner_with_encumbrance'),
        ('Joint_Ownership', 'Joint_Ownership'),
        ('Council_house', 'Council_house'),
        ('Unknown', 'Unknown'),
        ('Homeless', 'Homeless'),
        ('Other', 'Other'),
    ]
    
    RATING_CHOICES = [
        ('C', 'C'),
        ('B', 'B'),
        ('A', 'A'),
        ('F', 'F'),
        ('HR', 'HR'),
        ('E', 'E'),
        ('D', 'D'),
        ('AA', 'AA'),
    ]
    
    CREDIT_SCORE_MICROL_CHOICES = [
        ('M', 'M'),
        ('M3', 'M3'),
        ('M5', 'M5'),
        ('M4', 'M4'),
        ('M1', 'M1'),
        ('M2', 'M2'),
        ('M6', 'M6'),
        ('M7', 'M7'),
        ('M8', 'M8'),
        ('M10', 'M10'),
        ('M9', 'M9'),
    ]
    RESTRUCTURE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    restructure = models.CharField(max_length=3, choices=RESTRUCTURE_CHOICES, default='No')

    # Updated the field type to FloatField
    credit_score_ee_mini = models.FloatField()

    new_credit_customer = models.CharField(max_length=50, choices=NEW_CREDIT_CHOICES)
    verification_type = models.CharField(max_length=50, choices=VERIFICATION_TYPE_CHOICES)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    applied_amount = models.FloatField()
    amount = models.FloatField()
    use_of_loan = models.CharField(max_length=50, choices=USE_OF_LOAN_CHOICES)
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENT_STATUS_CHOICES)
    employment_duration = models.CharField(max_length=50, choices=EMPLOYMENT_DURATION_CHOICES)
    occupation_area = models.CharField(max_length=50, choices=OCCUPATION_AREA_CHOICES)
    home_ownership_type = models.CharField(max_length=50, choices=HOME_OWNERSHIP_CHOICES)
    total_income = models.FloatField()
    total_liabilities = models.FloatField()
    debt_to_income = models.FloatField()
    free_cash = models.FloatField()
    rating = models.CharField(max_length=5, choices=RATING_CHOICES)
    credit_score_es_micro_l = models.CharField(max_length=5, choices=CREDIT_SCORE_MICROL_CHOICES)
    
    no_of_previous_loans = models.FloatField()
    amount_of_previous_loans = models.FloatField()
    

# class LoanApplication(models.Model):
#     NEW_CREDIT_CHOICES = [
#         ('Existing_credit_customer', 'Existing_credit_customer'),
#         ('New_credit_customer', 'New_credit_customer'),
#     ]
    
#     VERIFICATION_TYPE_CHOICES = [
#         ('Income_expenses_verified', 'Income_expenses_verified'),
#         ('Income_unverified', 'Income_unverified'),
#         ('Income_verified', 'Income_verified'),
#         ('Income_unverified_crossref_phone', 'Income_unverified_crossref_phone'),
#         ('Not_set', 'Not_set'),
#     ]
    
#     GENDER_CHOICES = [
#         ('Female', 'Female'),
#         ('Male', 'Male'),
#         ('Unknown', 'Unknown'),
#     ]
    
#     USE_OF_LOAN_CHOICES = [
#         ('Home_improvement', 'Home_improvement'),
#         ('Business', 'Business'),
#         ('Other', 'Other'),
#         ('Health', 'Health'),
#         ('Vehicle', 'Vehicle'),
#         ('Loan_consolidation', 'Loan_consolidation'),
#         ('Travel', 'Travel'),
#         ('Education', 'Education'),
#         ('Real_estate', 'Real_estate'),
#         ('Working_capital_financing', 'Working_capital_financing'),
#         ('Accounts_receivable_financing', 'Accounts_receivable_financing'),
#         ('Purchase_of_machinery_equipment', 'Purchase_of_machinery_equipment'),
#         ('Other_business', 'Other_business'),
#         ('Acquisition_of_real_estate', 'Acquisition_of_real_estate'),
#         ('Construction_finance', 'Construction_finance'),
#         ('Acquisition_of_stocks', 'Acquisition_of_stocks'),
#         ('Not_set', 'Not_set'),
#     ]
    
#     EMPLOYMENT_STATUS_CHOICES = [
#         ('Retiree', 'Retiree'),
#         ('Entrepreneur', 'Entrepreneur'),
#         ('Fully-Employed', 'Fully-Employed'),
#         ('Partially-Employed', 'Partially-Employed'),
#         ('Self-Employed', 'Self-Employed'),
#         ('Unknown', 'Unknown'),
#     ]
    
#     EMPLOYMENT_DURATION_CHOICES = [
#         ('0', '0'),
#         ('MoreThan5Years', 'MoreThan5Years'),
#         ('UpTo3Years', 'UpTo3Years'),
#         ('UpTo5Years', 'UpTo5Years'),
#         ('UpTo1Year', 'UpTo1Year'),
#         ('UpTo2Years', 'UpTo2Years'),
#         ('UpTo4Years', 'UpTo4Years'),
#         ('TrialPeriod', 'TrialPeriod'),
#     ]
    
#     OCCUPATION_AREA_CHOICES = [
#         ('Other', 'Other'),
#         ('Retail_and_wholesale', 'Retail_and_wholesale'),
#         ('Transport_and_warehousing', 'Transport_and_warehousing'),
#         ('Hospitality_and_catering', 'Hospitality_and_catering'),
#         ('Finance_and_insurance', 'Finance_and_insurance'),
#         ('Research', 'Research'),
#         ('Agriculture_forestry_and_fishing', 'Agriculture_forestry_and_fishing'),
#         ('Healthcare_and_social_help', 'Healthcare_and_social_help'),
#         ('Processing', 'Processing'),
#         ('Construction', 'Construction'),
#         ('Administrative', 'Administrative'),
#         ('Real_estate', 'Real_estate'),
#         ('Energy', 'Energy'),
#         ('Education', 'Education'),
#         ('Info_and_telecom', 'Info_and_telecom'),
#         ('Civil_service_and_military', 'Civil_service_and_military'),
#         ('Utilities', 'Utilities'),
#         ('Art_and_entertainment', 'Art_and_entertainment'),
#         ('Mining', 'Mining'),
#         ('Not_specified', 'Not_specified'),
#     ]
    
#     HOME_OWNERSHIP_CHOICES = [
#         ('Owner', 'Owner'),
#         ('Mortgage', 'Mortgage'),
#         ('Living_with_parents', 'Living_with_parents'),
#         ('Tenant_pre_furnished_property', 'Tenant_pre_furnished_property'),
#         ('Tenant_unfurnished_property', 'Tenant_unfurnished_property'),
#         ('Joint_tenant', 'Joint_tenant'),
#         ('Owner_with_encumbrance', 'Owner_with_encumbrance'),
#         ('Joint_Ownership', 'Joint_Ownership'),
#         ('Council_house', 'Council_house'),
#         ('Unknown', 'Unknown'),
#         ('Homeless', 'Homeless'),
#         ('Other', 'Other'),
#     ]
    
#     RATING_CHOICES = [
#         ('C', 'C'),
#         ('B', 'B'),
#         ('A', 'A'),
#         ('F', 'F'),
#         ('HR', 'HR'),
#         ('E', 'E'),
#         ('D', 'D'),
#         ('AA', 'AA'),
#     ]
    
#     CREDIT_SCORE_MICROL_CHOICES = [
#         ('M', 'M'),
#         ('M3', 'M3'),
#         ('M5', 'M5'),
#         ('M4', 'M4'),
#         ('M1', 'M1'),
#         ('M2', 'M2'),
#         ('M6', 'M6'),
#         ('M7', 'M7'),
#         ('M8', 'M8'),
#         ('M10', 'M10'),
#         ('M9', 'M9'),
#     ]
#     RESTRUCTURE_CHOICES = [
#         ('Yes', 'Yes'),
#         ('No', 'No'),
#     ]
#     restructure = models.CharField(max_length=3, choices=RESTRUCTURE_CHOICES, default='No')

#     # Updated the field type to FloatField
#     credit_score_ee_mini = models.FloatField()

#     new_credit_customer = models.CharField(max_length=50, choices=NEW_CREDIT_CHOICES)
#     verification_type = models.CharField(max_length=50, choices=VERIFICATION_TYPE_CHOICES)
#     age = models.IntegerField()
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
#     applied_amount = models.FloatField()
#     amount = models.FloatField()
#     use_of_loan = models.CharField(max_length=50, choices=USE_OF_LOAN_CHOICES)
#     employment_status = models.CharField(max_length=50, choices=EMPLOYMENT_STATUS_CHOICES)
#     employment_duration = models.CharField(max_length=50, choices=EMPLOYMENT_DURATION_CHOICES)
#     occupation_area = models.CharField(max_length=50, choices=OCCUPATION_AREA_CHOICES)
#     home_ownership_type = models.CharField(max_length=50, choices=HOME_OWNERSHIP_CHOICES)
#     total_income = models.FloatField()
#     total_liabilities = models.FloatField()
#     debt_to_income = models.FloatField()
#     free_cash = models.FloatField()
#     rating = models.CharField(max_length=5, choices=RATING_CHOICES)
#     credit_score_es_micro_l = models.CharField(max_length=5, choices=CREDIT_SCORE_MICROL_CHOICES)
    
#     no_of_previous_loans = models.FloatField()
#     amount_of_previous_loans = models.FloatField()

    def __str__(self):
        return f"LoanApplication({self.id}) - {self.new_credit_customer}"
# app1/models.py
