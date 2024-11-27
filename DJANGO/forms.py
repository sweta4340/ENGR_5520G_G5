from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 


class SignUpForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter email-username", "class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))
    
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password1", "password2"]
from django import forms
from .models import LoanApplication

# Loan Application Form
# class LoanApplicationForm(forms.ModelForm):
#     class Meta:
#         model = LoanApplication
#         fields = [
#             'new_credit_customer', 'verification_type', 'age', 'gender', 
#             'applied_amount', 'amount', 'use_of_loan', 'employment_status', 
#             'employment_duration', 'occupation_area', 'home_ownership_type', 
#             'total_income', 'total_liabilities', 'debt_to_income', 'free_cash', 
#             'rating', 'credit_score_es_micro_l', 'credit_score_ee_mini', 
#             'no_of_previous_loans', 'amount_of_previous_loans'
#         ]

#         widgets = {
#             'new_credit_customer': forms.Select(choices=LoanApplication.NEW_CREDIT_CHOICES),
#             'verification_type': forms.Select(choices=LoanApplication.VERIFICATION_TYPE_CHOICES),
#             'gender': forms.Select(choices=LoanApplication.GENDER_CHOICES),
#             'use_of_loan': forms.Select(choices=LoanApplication.USE_OF_LOAN_CHOICES),
#             'employment_status': forms.Select(choices=LoanApplication.EMPLOYMENT_STATUS_CHOICES),
#             'employment_duration': forms.Select(choices=LoanApplication.EMPLOYMENT_DURATION_CHOICES),
#             'occupation_area': forms.Select(choices=LoanApplication.OCCUPATION_AREA_CHOICES),
#             'home_ownership_type': forms.Select(choices=LoanApplication.HOME_OWNERSHIP_CHOICES),
#             'rating': forms.Select(choices=LoanApplication.RATING_CHOICES),
#             'credit_score_es_micro_l': forms.Select(choices=LoanApplication.CREDIT_SCORE_MICROL_CHOICES),  # Categorical choice field
#             'credit_score_ee_mini': forms.NumberInput(attrs={'placeholder': 'Credit Score (Mini)', 'type': 'number'}),  # Float field
#             'age': forms.NumberInput(attrs={'placeholder': 'Age'}),
#             'applied_amount': forms.NumberInput(attrs={'placeholder': 'Applied Loan Amount'}),
#             'amount': forms.NumberInput(attrs={'placeholder': 'Loan Amount'}),
#             'total_income': forms.NumberInput(attrs={'placeholder': 'Total Income'}),
#             'total_liabilities': forms.NumberInput(attrs={'placeholder': 'Total Liabilities'}),
#             'debt_to_income': forms.NumberInput(attrs={'placeholder': 'Debt to Income'}),
#             'free_cash': forms.NumberInput(attrs={'placeholder': 'Free Cash'}),
#             'no_of_previous_loans': forms.NumberInput(attrs={'placeholder': 'Number of Previous Loans'}),
#             'amount_of_previous_loans': forms.NumberInput(attrs={'placeholder': 'Amount of Previous Loans'}),
#         }
#         # app1/forms.py
# from django import forms
# from .models import LoanApplication

# # Loan Application Form
# class LoanApplicationForm(forms.ModelForm):
#     class Meta:
#         model = LoanApplication
#         fields = [
#             'new_credit_customer', 'verification_type', 'age', 'gender', 
#             'applied_amount', 'amount', 'use_of_loan', 'employment_status', 
#             'employment_duration', 'occupation_area', 'home_ownership_type', 
#             'total_income', 'total_liabilities', 'debt_to_income', 'free_cash', 
#             'rating', 'credit_score_es_micro_l', 'credit_score_ee_mini', 
#             'no_of_previous_loans', 'amount_of_previous_loans','restructure'
#         ]

#         widgets = {
#             'restructure': forms.Select(choices=LoanApplication.RESTRUCTURE_CHOICES),            
#             'new_credit_customer': forms.Select(choices=LoanApplication.NEW_CREDIT_CHOICES),
#             'verification_type': forms.Select(choices=LoanApplication.VERIFICATION_TYPE_CHOICES),
#             'gender': forms.Select(choices=LoanApplication.GENDER_CHOICES),
#             'use_of_loan': forms.Select(choices=LoanApplication.USE_OF_LOAN_CHOICES),
#             'employment_status': forms.Select(choices=LoanApplication.EMPLOYMENT_STATUS_CHOICES),
#             'employment_duration': forms.Select(choices=LoanApplication.EMPLOYMENT_DURATION_CHOICES),
#             'occupation_area': forms.Select(choices=LoanApplication.OCCUPATION_AREA_CHOICES),
#             'home_ownership_type': forms.Select(choices=LoanApplication.HOME_OWNERSHIP_CHOICES),
#             'rating': forms.Select(choices=LoanApplication.RATING_CHOICES),
#             'credit_score_es_micro_l': forms.Select(choices=LoanApplication.CREDIT_SCORE_MICROL_CHOICES),
#             'credit_score_ee_mini': forms.NumberInput(attrs={'placeholder': 'Credit Score (Mini)', 'type': 'number'}),
#             'age': forms.NumberInput(attrs={'placeholder': 'Age', 'min': 18, 'max': 100}),
#             'applied_amount': forms.NumberInput(attrs={'placeholder': 'Applied Loan Amount', 'min': 0}),
#             'amount': forms.NumberInput(attrs={'placeholder': 'Loan Amount', 'min': 0}),
#             'total_income': forms.NumberInput(attrs={'placeholder': 'Total Income', 'min': 0}),
#             'total_liabilities': forms.NumberInput(attrs={'placeholder': 'Total Liabilities', 'min': 0}),
#             'debt_to_income': forms.NumberInput(attrs={'placeholder': 'Debt to Income', 'min': 0}),
#             'free_cash': forms.NumberInput(attrs={'placeholder': 'Free Cash', 'min': 0}),
#             'no_of_previous_loans': forms.NumberInput(attrs={'placeholder': 'Number of Previous Loans', 'min': 0}),
#             'amount_of_previous_loans': forms.NumberInput(attrs={'placeholder': 'Amount of Previous Loans', 'min': 0}),
#         }

#     # Custom validation for specific fields
#     def clean_age(self):
#         age = self.cleaned_data.get('age')
#         if age < 18:
#             raise forms.ValidationError("Age must be at least 18.")
#         return age

#     def clean_applied_amount(self):
#         applied_amount = self.cleaned_data.get('applied_amount')
#         if applied_amount <= 0:
#             raise forms.ValidationError("Applied amount must be greater than zero.")
#         return applied_amount

#     def clean_credit_score_ee_mini(self):
#         credit_score = self.cleaned_data.get('credit_score_ee_mini')
#         if credit_score is not None and (credit_score < 0 or credit_score > 1000):
#             raise forms.ValidationError("Credit score should be between 0 and 1000.")
#         return credit_score
from django import forms
from .models import LoanApplication

# Loan Application Form
class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'new_credit_customer', 'verification_type', 'age', 'gender', 
            'applied_amount', 'amount', 'use_of_loan', 
            'employment_status', 'employment_duration', 'occupation_area', 'home_ownership_type', 
            'total_income', 'total_liabilities', 'debt_to_income', 'free_cash', 
            'rating', 'credit_score_es_micro_l', 'credit_score_ee_mini', 
            'no_of_previous_loans', 'amount_of_previous_loans', 'restructure'
        ]

        widgets = {
            'restructure': forms.Select(choices=LoanApplication.RESTRUCTURE_CHOICES),            
            'new_credit_customer': forms.Select(choices=LoanApplication.NEW_CREDIT_CHOICES),
            'verification_type': forms.Select(choices=LoanApplication.VERIFICATION_TYPE_CHOICES),
            'gender': forms.Select(choices=LoanApplication.GENDER_CHOICES),
            'use_of_loan': forms.Select(choices=LoanApplication.USE_OF_LOAN_CHOICES),
            'employment_status': forms.Select(choices=LoanApplication.EMPLOYMENT_STATUS_CHOICES),
            'employment_duration': forms.Select(choices=LoanApplication.EMPLOYMENT_DURATION_CHOICES),
            'occupation_area': forms.Select(choices=LoanApplication.OCCUPATION_AREA_CHOICES),
            'home_ownership_type': forms.Select(choices=LoanApplication.HOME_OWNERSHIP_CHOICES),
            'rating': forms.Select(choices=LoanApplication.RATING_CHOICES),
            'credit_score_es_micro_l': forms.Select(choices=LoanApplication.CREDIT_SCORE_MICROL_CHOICES),
            'credit_score_ee_mini': forms.NumberInput(attrs={'placeholder': 'Credit Score (Mini)', 'type': 'number'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age', 'min': 18, 'max': 100}),
            'applied_amount': forms.NumberInput(attrs={'placeholder': 'Applied Loan Amount', 'min': 0}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Loan Amount', 'min': 0}),
            'total_income': forms.NumberInput(attrs={'placeholder': 'Total Income', 'min': 0}),
            'total_liabilities': forms.NumberInput(attrs={'placeholder': 'Total Liabilities', 'min': 0}),
            'debt_to_income': forms.NumberInput(attrs={'placeholder': 'Debt to Income', 'min': 0}),
            'free_cash': forms.NumberInput(attrs={'placeholder': 'Free Cash', 'min': 0}),
            'no_of_previous_loans': forms.NumberInput(attrs={'placeholder': 'Number of Previous Loans', 'min': 0}),
            'amount_of_previous_loans': forms.NumberInput(attrs={'placeholder': 'Amount of Previous Loans', 'min': 0}),
        }

    # Custom validation for specific fields
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError("Age must be at least 18.")
        return age

    def clean_applied_amount(self):
        applied_amount = self.cleaned_data.get('applied_amount')
        if applied_amount <= 0:
            raise forms.ValidationError("Applied amount must be greater than zero.")
        return applied_amount

    def clean_credit_score_ee_mini(self):
        credit_score = self.cleaned_data.get('credit_score_ee_mini')
        if credit_score is not None and (credit_score < 0 or credit_score > 1000):
            raise forms.ValidationError("Credit score should be between 0 and 1000.")
        return credit_score

    def clean_interest(self):
        interest = self.cleaned_data.get('interest')
        if interest < 0:
            raise forms.ValidationError("Interest must be a non-negative value.")
        return interest

    def clean_loan_duration(self):
        loan_duration = self.cleaned_data.get('loan_duration')
        if loan_duration <= 0:
            raise forms.ValidationError("Loan duration must be greater than zero.")
        return loan_duration
