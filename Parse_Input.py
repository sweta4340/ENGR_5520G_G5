#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import joblib


# In[2]:


encoder = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/data_encoder.pkl')
loan_scaler_x = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Loan_Amount_Prediction/loan_scaler_X.pkl')
loan_scaler_y = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Loan_Amount_Prediction/loan_scaler_y.pkl')

defaultprob_scaler_x = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Default_Probability_Prediction/defaultprob_scaler_X.pkl')
defaultprob_scaler_y = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Default_Probability_Prediction/defaultprob_scaler_y.pkl')

expreturn_scaler_x = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Expected_Return_Prediction/expreturn_scaler_X.pkl')
expreturn_scaler_y = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Expected_Return_Prediction/expreturn_scaler_y.pkl')

interest_scaler_x = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Interest_Rate_Prediction/interest_scaler_X.pkl')
interest_scaler_y = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Interest_Rate_Prediction/interest_scaler_y.pkl')


# In[3]:


# Loading the cleaned data after preprocessing.
df = pd.read_csv("C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Cleaned_Loan_approval_dataset.csv")


# In[20]:


df.head()


# In[4]:


record = df.loc[0, ['NewCreditCustomer', 'VerificationType', 'LanguageCode', 'Age',
       'Gender', 'Country', 'AppliedAmount', 'UseOfLoan',
       'Education', 'MaritalStatus', 'EmploymentStatus',
       'EmploymentDurationCurrentEmployer', 'OccupationArea',
       'HomeOwnershipType', 'DebtToIncome', 'FreeCash','Rating', 'Restructured', 'CreditScoreEsMicroL',
       'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan',
       'AmountOfPreviousLoansBeforeLoan', 'TotalIncome', 'TotalLiabilities']] 


# In[5]:


record


# In[ ]:


test_case_1 = {
    'NewCreditCustomer': 0,                # No new credit customer, but no data on previous credit
    'VerificationType': 'Income_unverified',             # No verification type specified
    'Age': 0,                              # Age as zero (unrealistic, but tests edge case handling)
    'Gender': 'Unknown',                   # Gender not specified
    'AppliedAmount': 0,                     # No loan amount applied for
    'UseOfLoan': 'None',                    # No loan purpose specified
    'EmploymentStatus': 'Unknown',          # Employment status unknown
    'EmploymentDurationCurrentEmployer': 'Not_known', # No employment duration
    'OccupationArea': 'Not_specified',            # Occupation area not specified
    'HomeOwnershipType': 'Unknown',        # Homeownership type not specified
    'TotalIncome': 0,                       # No income reported
    'TotalLiabilities': 0,                  # No liabilities reported
    'DebtToIncome': 0,                      # No debt-to-income ratio (effectively zero debt and zero income)
    'FreeCash': 0,                          # No free cash
    'Rating': 0,                            # No credit rating
    'CreditScoreEsMicroL': 'M9',               # No credit score
    'CreditScoreEeMini': 0,                 # No credit score
    'NoOfPreviousLoansBeforeLoan': 0,       # No previous loans
    'AmountOfPreviousLoansBeforeLoan': 0    # No previous loan amounts
}


# In[27]:


class LoanProcessor:
     def __init__(self, encoder, loan_scaler_x, loan_scaler_y, defaultprob_scaler_x, defaultprob_scaler_y, expreturn_scaler_x, expreturn_scaler_y, interest_scaler_x, interest_scaler_y):
        # Initialize with all required encoders and scalers
        self.encoder = encoder
        self.loan_scaler_x = loan_scaler_x
        self.loan_scaler_y = loan_scaler_y
        self.defaultprob_scaler_x = defaultprob_scaler_x
        self.defaultprob_scaler_y = defaultprob_scaler_y
        self.expreturn_scaler_x = expreturn_scaler_x
        self.expreturn_scaler_y = expreturn_scaler_y
        self.interest_scaler_x = interest_scaler_x
        self.interest_scaler_y = interest_scaler_y
        
        # Load models
        self.loan_model = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/Project/Models/loan_model.joblib')
        self.defaultprob_model = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/Project/Models/defaultprob_model.joblib')
        self.expreturn_model = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/Project/Models/expreturn_model.joblib')
        self.interest_model = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/Project/Models/interest_model.joblib')
        
    
     def data_preprocessor(self, data):
        """Converts JSON data to DataFrame, encodes categorical features, and handles skewness."""
        df = pd.DataFrame([data])
        
        # Encode categorical columns
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        for column in categorical_columns:
            df[column] = self.encoder.fit_transform(df[column])
        
        # Handle skewed features
        skewed_features = df.apply(lambda x: x.skew()).sort_values(ascending=False)
        threshold = 2
        features_to_transform = skewed_features[skewed_features.abs() > threshold].index.tolist()
        
        for column in features_to_transform:
            if skewed_features[column] > 0:
                if (df[column] >= 0).all():
                    df[column] = np.log1p(df[column])
                else:
                    min_value = df[column].min()
                    df[column] = df[column] + abs(min_value) + 1
                    df[column] = np.log1p(df[column])
        
        return df
     def predict_loan(self, df):
        loan_features = ['NewCreditCustomer', 'VerificationType', 'Age', 'Gender',
           'AppliedAmount', 'UseOfLoan', 'EmploymentStatus',
           'EmploymentDurationCurrentEmployer', 'OccupationArea',
           'HomeOwnershipType', 'TotalIncome', 'TotalLiabilities', 'DebtToIncome',
           'FreeCash', 'Rating', 'CreditScoreEsMicroL', 'CreditScoreEeMini',
           'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan']
        
        loan_df = df[loan_features]
        X = pd.DataFrame(self.loan_scaler_x.fit_transform(loan_df), columns=loan_df.columns)
        X = X.values.reshape(1, -1)
        
        y_pred = self.loan_model.predict(X).reshape(-1, 1)
        loan_amount = self.loan_scaler_y.inverse_transform(y_pred)
        
        print("Loan Amount: " + str(loan_amount))
        return loan_amount

     def predict_prob(self, df):
        prob_features = ['AppliedAmount', 'Amount', 'UseOfLoan', 'TotalLiabilities', 'TotalIncome', 
                         'DebtToIncome', 'FreeCash', 'NewCreditCustomer', 'CreditScoreEsMicroL', 
                         'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
                         'Age', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'HomeOwnershipType', 
                         'Rating', 'Restructured']
        
        prob_df = df[prob_features]
        X = pd.DataFrame(self.defaultprob_scaler_x.fit_transform(prob_df), columns=prob_df.columns)
        X = X.values.reshape(1, -1)
        
        y_pred = self.defaultprob_model.predict(X).reshape(-1, 1)
        default_prob = self.defaultprob_scaler_y.inverse_transform(y_pred)
        
        return default_prob

     def predict_expreturn(self, df):
        expreturn_features = ['AppliedAmount', 'Amount', 'ProbabilityOfDefault', 'UseOfLoan', 'TotalLiabilities', 
                              'TotalIncome', 'DebtToIncome', 'FreeCash', 'NewCreditCustomer', 'CreditScoreEsMicroL', 
                              'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
                              'Age', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'HomeOwnershipType', 
                              'Rating', 'Restructured']
        
        expreturn_df = df[expreturn_features]
        X = pd.DataFrame(self.expreturn_scaler_x.fit_transform(expreturn_df), columns=expreturn_df.columns)
        X = X.values.reshape(1, -1)
        
        y_pred = self.expreturn_model.predict(X).reshape(-1, 1)
        exp_return = self.expreturn_scaler_y.inverse_transform(y_pred)
        
        return np.log1p(exp_return)

     def predict_interest(self, df):
        interest_features = ['AppliedAmount', 'Amount', 'UseOfLoan', 'NewCreditCustomer', 'Age', 'Gender', 
                             'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'OccupationArea', 
                             'TotalIncome', 'TotalLiabilities', 'DebtToIncome', 'FreeCash', 'HomeOwnershipType', 
                             'CreditScoreEsMicroL', 'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 
                             'AmountOfPreviousLoansBeforeLoan', 'ExpectedReturn', 'ProbabilityOfDefault', 'Rating', 
                             'Restructured']
        
        interest_df = df[interest_features]
        X = pd.DataFrame(self.interest_scaler_x.fit_transform(interest_df), columns=interest_df.columns)
        X = X.values.reshape(1, -1)
        
        y_pred = self.interest_model.predict(X).reshape(-1, 1)
        interest = self.interest_scaler_y.inverse_transform(y_pred)
        
        print("Interest Amount: " + str(interest))
        return interest
    
     def parse_input(self, request):
        """Processes input data, makes predictions, and returns a DataFrame with results."""
        df = self.preprocess_data(request)
        
        # Make predictions
        df['Amount'] = self.predict_loan(df)
        df['ProbabilityOfDefault'] = self.predict_prob(df)
        df['ExpectedReturn'] = self.predict_expreturn(df)
        df['Interest'] = self.predict_interest(df)
        
        # Insert into database
        # self.insert_to_database(df)
        
        return df
   


# In[ ]:





# In[ ]:




