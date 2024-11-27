from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name = "home"),
    path('login/', views.loginpage, name = "login"),
    path('signup/', views.sign_up, name = "sign_up"),  
    path('verify_email/<slug:username>', views.verify_email, name = "verify_email"),
    path('user/', views.user_home, name = "user"),   
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path('loan-application/', views.loan_application, name='loan_application'), # Path for the loan prediction API (using POST request to get prediction)
  


    ]