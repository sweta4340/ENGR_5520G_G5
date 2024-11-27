from sqlite3 import IntegrityError
import time
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache


from .forms import SignUpForm
# from .models import CustomUser
import random
from django.utils import timezone
# Create your views here.

# @login_required(login_url='login')
def home(request):
    return render(request, "index.html")

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user")
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils import timezone
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            # Generate OTP code
            otp_code = get_random_string(length=6, allowed_chars='0123456789')
            # Set OTP expiration time (e.g., 5 minutes from now)
            otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
            # Save OTP token in the database
            OtpToken.objects.create(user=user, otp_code=otp_code, otp_expires_at=otp_expires_at)
            # Send OTP email
            subject = "Email Verification"
            message = render_to_string('otp_email.html', {'otp_code': otp_code})
            sender = "your_email@example.com"  # Update with your sender email address
            receiver = [user.email]
            send_mail(subject, message, sender, receiver)
            # Redirect to the verify-email page
            return redirect('verify_email', username=user.username)
        else:
            messages.warning(request, 'username or email are already taken')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form ,'error_message': 'Invalid username or password'})
         

def success(request):
    return render(request, 'success.html')

def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

from django.utils.crypto import get_random_string
from django.utils import timezone
from .models import OtpToken

def verify_email(request, username):
    user = User.objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code', '')  # Get entered OTP from the form
        stored_otp = user_otp.otp_code  # Get stored OTP from the database
        
        if entered_otp == stored_otp:  # Compare entered and stored OTPs
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect('login')
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify_email", username=user.username)
        else:
            print("User OTP:", user_otp)
            print("Stored OTP:", user_otp.otp_code)
            print("OTP Expiry:", user_otp.otp_expires_at)
            print("Current Time:", timezone.now())
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify_email", username=user.username)
        
    context = {}
    return render(request, "verify_token.html", context)
 
# def verify_email(request, username):
#     user = User.objects.get(username=username)
#     user_otp = OtpToken.objects.filter(user=user).last()           
    
#     if request.method == 'POST':
#         if user_otp.otp_code == request.POST['otp_code']:
#             if user_otp.otp_expires_at > timezone.now():
#                 user.is_active = True
#                 user.save()
#                 messages.success(request, "Account activated successfully!! You can Login.")


#                 return redirect("signin")
#             else:
#                 messages.warning(request, "The OTP has expired, get a new OTP!")
#                 return redirect("verify_ email", username=user.username)
#         else:
#             print("User OTP:", user_otp)
#             print("Stored OTP:", user_otp.otp_code)
#             print("OTP Expiry:", user_otp.otp_expires_at)
#             print("Current Time:", timezone.now())
#             messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
#             return redirect("verify_email", username=user.username)
#     context = {}
#     return render(request, "verify_token.html", context)
from django.contrib.auth import get_user_model
import random

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        try:
            user = get_user_model().objects.get(email=user_email)
        except get_user_model().DoesNotExist:
            messages.warning(request, "This email doesn't exist in the database")
            return redirect("resend-otp")

        # Check if an OTP token already exists for the user
        try:
            otp = OtpToken.objects.get(user=user)
            # Update the existing OTP token or delete it if necessary
            otp.otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a new OTP
            otp.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
            otp.save()
        except OtpToken.DoesNotExist:
            # Create a new OTP token if it doesn't exist
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5),
                                           otp_code=''.join([str(random.randint(0, 9)) for _ in range(6)]))
        except IntegrityError:
            # Handle the case where multiple OTP tokens exist for the same user
            messages.error(request, "Multiple OTP tokens found for this user. Please contact support.")
            return redirect("resend-otp")

        subject = "Email Verification"
        message = f"""
Hi {user.username}, here is your OTP {otp.otp_code} 
it expires in 5 minute, use the URL below to redirect back to the website
http://127.0.0.1:8000/verify-email/{user.username}
"""
        sender = "heetpatel20@gnu.ac.in"
        receiver = [user.email, ]

        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )
        messages.success(request, "A new OTP has been sent to your email address")
        return redirect("verify_email", username=user.username)

    context = {}
    return render(request, "resend_otp.html", context)


def user_home(request):
    return render(request, "index2.html", {'user': request.user})
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import numpy as np
import joblib
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import numpy as np
import joblib
from django.shortcuts import render
from django.http import JsonResponse
import joblib
from .loan_processor import LoanProcessor
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import LoanApplicationForm  # Assuming you have this form created
from .models import LoanApplication  # Assuming LoanProcessor is in loan_processor.py
import joblib
import pandas as pd
from .loan_processor import LoanProcessor  # Import LoanProcessor
from django.shortcuts import render
from django.http import JsonResponse
from .forms import LoanApplicationForm
import joblib

# # Function to map form data keys to the expected model column names
# def map_form_to_model_data(form_data):
#     mapping = {
#         'new_credit_customer': 'NewCreditCustomer',
#         'verification_type': 'VerificationType',
#         'age': 'Age',
#         'gender': 'Gender',
#         'applied_amount': 'AppliedAmount',
#         'amount': 'Amount',
#         'use_of_loan': 'UseOfLoan',
#         'employment_status': 'EmploymentStatus',
#         'employment_duration': 'EmploymentDurationCurrentEmployer',
#         'occupation_area': 'OccupationArea',
#         'home_ownership_type': 'HomeOwnershipType',
#         'total_income': 'TotalIncome',
#         'total_liabilities': 'TotalLiabilities',
#         'debt_to_income': 'DebtToIncome',
#         'free_cash': 'FreeCash',
#         'rating': 'Rating',
#         'credit_score_es_micro_l': 'CreditScoreEsMicroL',
#         'credit_score_ee_mini': 'CreditScoreEeMini',
#         'no_of_previous_loans': 'NoOfPreviousLoansBeforeLoan',
#         'amount_of_previous_loans': 'AmountOfPreviousLoansBeforeLoan'
#     }

#     # Map the form data to the model columns
#     mapped_data = {mapping[key]: value for key, value in form_data.items() if key in mapping}
#     return mapped_data

# def loan_application(request):
#     if request.method == 'POST':
#         form_data = {
#             'new_credit_customer': request.POST['new_credit_customer'],
#             'verification_type': request.POST['verification_type'],
#             'age': request.POST['age'],
#             'gender': request.POST['gender'],
#             'applied_amount': request.POST['applied_amount'],
#             'amount': request.POST['amount'],
#             'use_of_loan': request.POST['use_of_loan'],
#             'employment_status': request.POST['employment_status'],
#             'employment_duration': request.POST['employment_duration'],
#             'occupation_area': request.POST['occupation_area'],
#             'home_ownership_type': request.POST['home_ownership_type'],
#             'total_income': request.POST['total_income'],
#             'total_liabilities': request.POST['total_liabilities'],
#             'debt_to_income': request.POST['debt_to_income'],
#             'free_cash': request.POST['free_cash'],
#             'rating': request.POST['rating'],
#             'credit_score_es_micro_l': request.POST['credit_score_es_micro_l'],
#             'credit_score_ee_mini': request.POST['credit_score_ee_mini'],
#             'no_of_previous_loans': request.POST['no_of_previous_loans'],
#             'amount_of_previous_loans': request.POST['amount_of_previous_loans']
#         }

#         # Map the form data to match the model columns
#         mapped_data = map_form_to_model_data(form_data)

#         # Load the necessary encoder and scaler models
#         encoder = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\label_encoders.pkl")
#         loan_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_scaler_X.pkl")
#         loan_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_scaler_y.pkl")

#         # Initialize the loan processor
#         loan_processor = LoanProcessor(encoder, loan_scaler_x, loan_scaler_y)
        
#         # Preprocess data and get predictions
#         preprocessed_data = loan_processor.parse_input(mapped_data)

#         # Return the predicted loan amount as JSON response
#         return JsonResponse({
#             'loan_amount': preprocessed_data['Amount'].tolist()
#         })

#     return render(request, 'loan_application_form.html', {'form': LoanApplicationForm()})

# from django.http import JsonResponse
# from django.shortcuts import render
# import joblib
# from .forms import LoanApplicationForm
# from .loan_processor import LoanProcessor  # Assuming LoanProcessor is in a file named loan_processor.py

# def map_form_to_model_data(form_data):
#     mapping = {
#         'new_credit_customer': 'NewCreditCustomer',
#         'verification_type': 'VerificationType',
#         'age': 'Age',
#         'gender': 'Gender',
#         'applied_amount': 'AppliedAmount',
#         'amount': 'Amount',
#         'use_of_loan': 'UseOfLoan',
#         'employment_status': 'EmploymentStatus',
#         'employment_duration': 'EmploymentDurationCurrentEmployer',
#         'occupation_area': 'OccupationArea',
#         'home_ownership_type': 'HomeOwnershipType',
#         'total_income': 'TotalIncome',
#         'total_liabilities': 'TotalLiabilities',
#         'debt_to_income': 'DebtToIncome',
#         'free_cash': 'FreeCash',
#         'rating': 'Rating',
#         'credit_score_es_micro_l': 'CreditScoreEsMicroL',
#         'credit_score_ee_mini': 'CreditScoreEeMini',
#         'no_of_previous_loans': 'NoOfPreviousLoansBeforeLoan',
#         'amount_of_previous_loans': 'AmountOfPreviousLoansBeforeLoan',
#         'restructure': 'Restructured'
#     }

#     # Map the form data to the model columns
#     mapped_data = {mapping[key]: value for key, value in form_data.items() if key in mapping}
#     return mapped_data

# def loan_application(request):
#     if request.method == 'POST':
#         form_data = {
#             'new_credit_customer': request.POST['new_credit_customer'],
#             'verification_type': request.POST['verification_type'],
#             'age': request.POST['age'],
#             'gender': request.POST['gender'],
#             'applied_amount': request.POST['applied_amount'],
#             'amount': request.POST['amount'],   
#             'use_of_loan': request.POST['use_of_loan'],
#             'employment_status': request.POST['employment_status'],
#             'employment_duration': request.POST['employment_duration'],
#             'occupation_area': request.POST['occupation_area'],
#             'home_ownership_type': request.POST['home_ownership_type'],
#             'total_income': request.POST['total_income'],
#             'total_liabilities': request.POST['total_liabilities'],
#             'debt_to_income': request.POST['debt_to_income'],
#             'free_cash': request.POST['free_cash'],
#             'rating': request.POST['rating'],
#             'credit_score_es_micro_l': request.POST['credit_score_es_micro_l'],
#             'credit_score_ee_mini': request.POST['credit_score_ee_mini'],
#             'no_of_previous_loans': request.POST['no_of_previous_loans'],
#             'amount_of_previous_loans': request.POST['amount_of_previous_loans'],
#             'restructure': request.POST['restructure'] 
            
#         }

#         # Map the form data to match the model columns
#         mapped_data = map_form_to_model_data(form_data)

#         # Load the necessary encoder and scaler models
#         encoder = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\label_encoders.pkl")
#         loan_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_scaler_X.pkl")
#         loan_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_scaler_y.pkl")
#         defaultprob_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\defaultprob_scaler_X.pkl")
#         defaultprob_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\defaultprob_scaler_y.pkl")
#         expreturn_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\expreturn_scaler_X.pkl")
#         expreturn_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\expreturn_scaler_y.pkl")

#         # Initialize the LoanProcessor with additional models
#         loan_processor = LoanProcessor(
#             encoder, loan_scaler_x, loan_scaler_y,
#             defaultprob_scaler_x, defaultprob_scaler_y,
#             expreturn_scaler_x, expreturn_scaler_y
#         )

#         # Preprocess data and get predictions
#         preprocessed_data = loan_processor.parse_input(mapped_data)

#         # Return the predicted loan amount, default probability, and expected return as JSON response
#         return JsonResponse({
#             'loan_amount': preprocessed_data['Amount'].tolist(),
#             'default_probability': preprocessed_data['ProbabilityOfDefault'].tolist(),
#             'expected_return': preprocessed_data['ExpectedReturn'].tolist()
#         })

#     return render(request, 'loan_application_form.html', {'form': LoanApplicationForm()})
# from django.http import JsonResponse
# from django.shortcuts import render
# import joblib
# from .forms import LoanApplicationForm
# from .loan_processor import LoanProcessor

# def map_form_to_model_data(form_data):
#     mapping = {
#         'new_credit_customer': 'NewCreditCustomer',
#         'verification_type': 'VerificationType',
#         'age': 'Age',
#         'gender': 'Gender',
#         'applied_amount': 'AppliedAmount',
#         'amount': 'Amount',
#         'use_of_loan': 'UseOfLoan',
#         'employment_status': 'EmploymentStatus',
#         'employment_duration': 'EmploymentDurationCurrentEmployer',
#         'occupation_area': 'OccupationArea',
#         'home_ownership_type': 'HomeOwnershipType',
#         'total_income': 'TotalIncome',
#         'total_liabilities': 'TotalLiabilities',
#         'debt_to_income': 'DebtToIncome',
#         'free_cash': 'FreeCash',
#         'rating': 'Rating',
#         'credit_score_es_micro_l': 'CreditScoreEsMicroL',
#         'credit_score_ee_mini': 'CreditScoreEeMini',
#         'no_of_previous_loans': 'NoOfPreviousLoansBeforeLoan',
#         'amount_of_previous_loans': 'AmountOfPreviousLoansBeforeLoan',
#         'restructure': 'Restructured'
#     }

#     mapped_data = {mapping[key]: value for key, value in form_data.items() if key in mapping}
#     return mapped_data

# def loan_application(request):
#     if request.method == 'POST':
#         form_data = {
#             'new_credit_customer': request.POST['new_credit_customer'],
#             'verification_type': request.POST['verification_type'],
#             'age': request.POST['age'],
#             'gender': request.POST['gender'],
#             'applied_amount': request.POST['applied_amount'],
#             'amount': request.POST['amount'],
#             'use_of_loan': request.POST['use_of_loan'],
#             'employment_status': request.POST['employment_status'],
#             'employment_duration': request.POST['employment_duration'],
#             'occupation_area': request.POST['occupation_area'],
#             'home_ownership_type': request.POST['home_ownership_type'],
#             'total_income': request.POST['total_income'],
#             'total_liabilities': request.POST['total_liabilities'],
#             'debt_to_income': request.POST['debt_to_income'],
#             'free_cash': request.POST['free_cash'],
#             'rating': request.POST['rating'],
#             'credit_score_es_micro_l': request.POST['credit_score_es_micro_l'],
#             'credit_score_ee_mini': request.POST['credit_score_ee_mini'],
#             'no_of_previous_loans': request.POST['no_of_previous_loans'],
#             'amount_of_previous_loans': request.POST['amount_of_previous_loans'],
#             'restructure': request.POST['restructure']
#         }

#         # Map the form data to match the model columns
#         mapped_data = map_form_to_model_data(form_data)

#         # Load the necessary encoder and scaler models
#         encoder = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\label_encoders.pkl")
#         loan_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\data\\loan_scaler_X.pkl")
#         loan_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_scaler_y.pkl")
#         defaultprob_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\defaultprob_scaler_X.pkl")
#         defaultprob_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\defaultprob_scaler_y.pkl")
#         expreturn_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\expreturn_scaler_X.pkl")
#         expreturn_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\expreturn_scaler_y.pkl")
#         interest_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\interest_scaler_X.pkl")
#         interest_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\interest_scaler_y.pkl")

#         # Create a LoanProcessor instance
#         loan_processor = LoanProcessor(encoder, loan_scaler_x, loan_scaler_y, defaultprob_scaler_x, defaultprob_scaler_y,
#                                        expreturn_scaler_x, expreturn_scaler_y, interest_scaler_x, interest_scaler_y)

#         # Make predictions
#         prediction_results = loan_processor.parse_input(mapped_data)

#         # Prepare JSON response
#         response_data = {
#             'loan_amount': float(prediction_results['Amount'].iloc[0]),
#             'default_probability': float(prediction_results['ProbabilityOfDefault'].iloc[0]),
#             'expected_return': float(prediction_results['ExpectedReturn'].iloc[0]),
#             'interest': float(prediction_results['Interest'].iloc[0])
#         }
#         return JsonResponse(response_data)

#     else:
#         form = LoanApplicationForm()
#         return render(request, 'loan_application_form.html', {'form': form})
from django.http import JsonResponse
from django.shortcuts import render
import joblib
from .forms import LoanApplicationForm
from .loan_processor import LoanProcessor

# Mapping function to map form data to model columns
def map_form_to_model_data(form_data):
    mapping = {
        'new_credit_customer': 'NewCreditCustomer',
        'verification_type': 'VerificationType',
        'age': 'Age',
        'gender': 'Gender',
        'applied_amount': 'AppliedAmount',
        'amount': 'Amount',
        'use_of_loan': 'UseOfLoan',
        'employment_status': 'EmploymentStatus',
        'employment_duration': 'EmploymentDurationCurrentEmployer',
        'occupation_area': 'OccupationArea',
        'home_ownership_type': 'HomeOwnershipType',
        'total_income': 'TotalIncome',
        'total_liabilities': 'TotalLiabilities',
        'debt_to_income': 'DebtToIncome',
        'free_cash': 'FreeCash',
        'rating': 'Rating',
        'credit_score_es_micro_l': 'CreditScoreEsMicroL',
        'credit_score_ee_mini': 'CreditScoreEeMini',
        'no_of_previous_loans': 'NoOfPreviousLoansBeforeLoan',
        'amount_of_previous_loans': 'AmountOfPreviousLoansBeforeLoan',
        'restructure': 'Restructured',
    }

    mapped_data = {mapping[key]: value for key, value in form_data.items() if key in mapping}
    return mapped_data

def loan_application(request):
    if request.method == 'POST':
        # Get form data from the request
        form_data = {
            'new_credit_customer': request.POST['new_credit_customer'],
            'verification_type': request.POST['verification_type'],
            'age': request.POST['age'],
            'gender': request.POST['gender'],
            'applied_amount': request.POST['applied_amount'],
            'amount': request.POST['amount'],
            'use_of_loan': request.POST['use_of_loan'],
            'employment_status': request.POST['employment_status'],
            'employment_duration': request.POST['employment_duration'],
            'occupation_area': request.POST['occupation_area'],
            'home_ownership_type': request.POST['home_ownership_type'],
            'total_income': request.POST['total_income'],
            'total_liabilities': request.POST['total_liabilities'],
            'debt_to_income': request.POST['debt_to_income'],
            'free_cash': request.POST['free_cash'],
            'rating': request.POST['rating'],
            'credit_score_es_micro_l': request.POST['credit_score_es_micro_l'],
            'credit_score_ee_mini': request.POST['credit_score_ee_mini'],
            'no_of_previous_loans': request.POST['no_of_previous_loans'],
            'amount_of_previous_loans': request.POST['amount_of_previous_loans'],
            'restructure': request.POST['restructure']
        }

        # Map form data to match the model column names
        mapped_data = map_form_to_model_data(form_data)

        # Load the necessary encoders and scalers for prediction
        encoder = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\label_encoders.pkl")
        loan_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_scaler_X.pkl")
        loan_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_scaler_y.pkl")
        defaultprob_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\defaultprob_scaler_X.pkl")
        defaultprob_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\defaultprob_scaler_y.pkl")
        expreturn_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\expreturn_scaler_X.pkl")
        expreturn_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\expreturn_scaler_y.pkl")
        interest_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\interest_scaler_X.pkl")
        interest_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\interest_scaler_y.pkl")

        # Create a LoanProcessor instance
        loan_processor = LoanProcessor(
            encoder, loan_scaler_x, loan_scaler_y,
            defaultprob_scaler_x, defaultprob_scaler_y,
            expreturn_scaler_x, expreturn_scaler_y,
            interest_scaler_x, interest_scaler_y
        )

        # Make predictions using the processed data
        prediction_results = loan_processor.parse_input(mapped_data)

        # Prepare JSON response with prediction results
        response_data = {
            'loan_amount': float(prediction_results['Amount'].iloc[0]),
            'default_probability': float(prediction_results['ProbabilityOfDefault'].iloc[0]),
            'expected_return': float(prediction_results['ExpectedReturn'].iloc[0]),
            'predict_interest': float(prediction_results['InterestRate'].iloc[0])
        }

        # Return the response as JSON
        return JsonResponse(response_data)

    else:
        # If the request is GET, display the form
        form = LoanApplicationForm()
        return render(request, 'loan_application_form.html', {'form': form})

#def loan_application(request):
#     if request.method == 'POST':
#         # Collect form data
#         form_data = {
#             'new_credit_customer': request.POST['new_credit_customer'],
#             'verification_type': request.POST['verification_type'],
#             'age': request.POST['age'],
#             'gender': request.POST['gender'],
#             'applied_amount': request.POST['applied_amount'],
#             'amount': request.POST['amount'],
#             'use_of_loan': request.POST['use_of_loan'],
#             'employment_status': request.POST['employment_status'],
#             'employment_duration': request.POST['employment_duration'],
#             'occupation_area': request.POST['occupation_area'],
#             'home_ownership_type': request.POST['home_ownership_type'],
#             'total_income': request.POST['total_income'],
#             'total_liabilities': request.POST['total_liabilities'],
#             'debt_to_income': request.POST['debt_to_income'],
#             'free_cash': request.POST['free_cash'],
#             'rating': request.POST['rating'],
#             'credit_score_es_micro_l': request.POST['credit_score_es_micro_l'],
#             'credit_score_ee_mini': request.POST['credit_score_ee_mini'],
#             'no_of_previous_loans': request.POST['no_of_previous_loans'],
#             'amount_of_previous_loans': request.POST['amount_of_previous_loans']
#         }

#         # Debugging: print the collected form data
#         print("Form Data:", form_data)

#         # Load the necessary encoder and scaler models
#         encoder = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\label_encoders.pkl")
#         loan_scaler_x = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_scaler_X.pkl")
#         loan_scaler_y = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_scaler_y.pkl")

#         # Initialize the loan processor
#         loan_processor = LoanProcessor(encoder, loan_scaler_x, loan_scaler_y)
        
#         # Preprocess data and get predictions
#         preprocessed_data = loan_processor.parse_input(form_data)

#         # Debugging: check if the preprocessed data is correct
#         print("Preprocessed Data:", preprocessed_data)

#         # Return the predicted loan amount as JSON response
#         return JsonResponse({
#             'loan_amount': preprocessed_data['Amount'].tolist()
#         })

#     return render(request, 'loan_application_form.html', {'form': LoanApplicationForm()})

# Initialize LoanProcessor insta \\Load your pre-trained loan prediction model
# loan_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_model.joblib")  # Path to your pre-trained model

# class LoanProcessor:
#     def __init__(self, loan_model):
#         self.loan_model = loan_model
        
#     def preprocess_data(self, data):
#         df = pd.DataFrame([data])

#         # Handle categorical columns manually using label encoding
#         categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
#         for column in categorical_columns:
#             df[column] = df[column].astype('category').cat.codes  # Label encoding for categorical features

#         # Handle skewness: Apply log transformation for skewed data
#         skewed_features = df.apply(lambda x: x.skew()).sort_values(ascending=False)
#         threshold = 2
#         features_to_transform = skewed_features[skewed_features.abs() > threshold].index.tolist()
        
#         for column in features_to_transform:
#             if skewed_features[column] > 0:
#                 if (df[column] >= 0).all():
#                     df[column] = np.log1p(df[column])  # Apply log transformation to skewed data
#                 else:
#                     min_value = df[column].min()
#                     df[column] = df[column] + abs(min_value) + 1
#                     df[column] = np.log1p(df[column])
        
#         return df
    
#     def predict_loan(self, df):
#         # Define the loan features
#         loan_features = ['NewCreditCustomer', 'VerificationType', 'Age', 'Gender',
#                          'AppliedAmount', 'UseOfLoan', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer',
#                          'OccupationArea', 'HomeOwnershipType', 'TotalIncome', 'TotalLiabilities', 'DebtToIncome',
#                          'FreeCash', 'Rating', 'CreditScoreEsMicroL', 'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 
#                          'AmountOfPreviousLoansBeforeLoan']
                         
#         loan_df = df[loan_features]
#         y_pred = self.loan_model.predict(loan_df)  # Direct prediction without scaling
#         return y_pred

#     def parse_input(self, data):
#         """Processes input data, makes predictions, and returns a DataFrame with results."""
#         df = self.preprocess_data(data)  # Preprocess the input data
        
#         # Make predictions
#         df['Amount'] = self.predict_loan(df)
#         return df

# # View to handle the loan prediction and display result
# def loan_prediction(request):
#     if request.method == 'POST':
#         try:
#             # Get data from the POST request, with default values if missing
#             data = {
#                 'NewCreditCustomer': int(request.POST.get('NewCreditCustomer', 0)),
#                 'VerificationType': request.POST.get('VerificationType', ''),
#                 'Age': int(request.POST.get('Age', 0)),
#                 'Gender': request.POST.get('Gender', ''),
#                 'AppliedAmount': float(request.POST.get('AppliedAmount', 0.0)),
#                 'UseOfLoan': request.POST.get('UseOfLoan', ''),
#                 'EmploymentStatus': request.POST.get('EmploymentStatus', ''),
#                 'EmploymentDurationCurrentEmployer': int(request.POST.get('EmploymentDurationCurrentEmployer', 0)),
#                 'OccupationArea': request.POST.get('OccupationArea', ''),
#                 'HomeOwnershipType': request.POST.get('HomeOwnershipType', ''),
#                 'TotalIncome': float(request.POST.get('TotalIncome', 0.0)),
#                 'TotalLiabilities': float(request.POST.get('TotalLiabilities', 0.0)),
#                 'DebtToIncome': float(request.POST.get('DebtToIncome', 0.0)),
#                 'FreeCash': float(request.POST.get('FreeCash', 0.0)),
#                 'Rating': int(request.POST.get('Rating', 0)),
#                 'CreditScoreEsMicroL': float(request.POST.get('CreditScoreEsMicroL', 0.0)),
#                 'CreditScoreEeMini': float(request.POST.get('CreditScoreEeMini', 0.0)),
#                 'NoOfPreviousLoansBeforeLoan': int(request.POST.get('NoOfPreviousLoansBeforeLoan', 0)),
#                 'AmountOfPreviousLoansBeforeLoan': float(request.POST.get('AmountOfPreviousLoansBeforeLoan', 0.0))
#             }

#             # Initialize the loan processor
#             loan_processor = LoanProcessor(loan_model)
            
#             # Convert the input dictionary to a DataFrame for prediction
#             predictions_df = loan_processor.parse_input(data)  # Get predictions
            
#             # Prepare the response (you can adjust this part to show relevant results)
#             predictions = predictions_df[['Amount']].to_dict(orient="records")[0]
            
#             # Return result as JsonResponse or render the result in a template
#             return JsonResponse(predictions, safe=False)
        
#         except Exception as e:
#             # Catch any exception and return a meaningful error message
#             return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=400)
    
#     return render(request, 'loan_prediction_form.html')  # Render your HTML template


def logoutuser(request):
        
    logout(request)
    return redirect('home')
