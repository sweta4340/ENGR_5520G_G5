import pandas as pd
import numpy as np
import joblib



class LoanProcessor:
     def __init__(self, encoder, loan_scaler_x, loan_scaler_y, defaultprob_scaler_x, defaultprob_scaler_y, expreturn_scaler_x, expreturn_scaler_y, interest_scaler_x, interest_scaler_y):
        # Initializing the required encoders and scalers.
        self.encoder = encoder
        self.loan_scaler_x = loan_scaler_x
        self.loan_scaler_y = loan_scaler_y
        self.defaultprob_scaler_x = defaultprob_scaler_x
        self.defaultprob_scaler_y = defaultprob_scaler_y
        self.expreturn_scaler_x = expreturn_scaler_x
        self.expreturn_scaler_y = expreturn_scaler_y
        self.interest_scaler_x = interest_scaler_x
        self.interest_scaler_y = interest_scaler_y
        
        # Loading the models.
        self.loan_model = joblib.load('Models/loan_model.joblib')
        #self.defaultprob_model = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/Project/Models/defaultprob_model.joblib')
        #self.expreturn_model = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/Project/Models/expreturn_model.joblib')
        #self.interest_model = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/Project/Models/interest_model.joblib')
        
    # Function to preprocess the data. This function will handle the encoding and skewwness of the data.
     def data_preprocessor(self, data):
        
        df = pd.DataFrame([data])
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        for column in categorical_columns:
            if column in self.encoder:
                encoder = self.encoder[column]
                df[column] = encoder.transform(df[column])  # Use the specific encoder for each column

        
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
    
    # Defining the function for predicting the loan.
     def predict_loan(self, df):
        loan_features = ['NewCreditCustomer', 'VerificationType', 'Age', 'Gender',
           'AppliedAmount', 'UseOfLoan', 'EmploymentStatus',
           'EmploymentDurationCurrentEmployer', 'OccupationArea',
           'HomeOwnershipType', 'TotalIncome', 'TotalLiabilities', 'DebtToIncome',
           'FreeCash', 'Rating', 'CreditScoreEsMicroL', 'CreditScoreEeMini',
           'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan']
        
        loan_df = df[loan_features]
        X = pd.DataFrame(self.loan_scaler_x.transform(loan_df), columns=loan_df.columns)
        y_pred = self.loan_model.predict(X).reshape(-1, 1)
        loan_amount = self.loan_scaler_y.inverse_transform(y_pred)
        
        #print("Loan Amount: " + str(loan_amount))
        return loan_amount
    
   # Defining the fucntion for predicting the Default Probability.  
     def predict_prob(self, df):
        prob_features = ['AppliedAmount', 'Amount', 'UseOfLoan', 'TotalLiabilities', 'TotalIncome', 
                         'DebtToIncome', 'FreeCash', 'NewCreditCustomer', 'CreditScoreEsMicroL', 
                         'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
                         'Age', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'HomeOwnershipType', 
                         'Rating', 'Restructured']
        
        prob_df = df[prob_features]
        X = pd.DataFrame(self.defaultprob_scaler_x.transform(prob_df), columns=prob_df.columns)
        y_pred = self.defaultprob_model.predict(X).reshape(-1, 1)
        default_prob = self.defaultprob_scaler_y.inverse_transform(y_pred)
        
        return default_prob
    
    # Defining the function for predicting the Expected Return.

     def predict_expreturn(self, df):
        expreturn_features = ['AppliedAmount', 'Amount', 'ProbabilityOfDefault', 'UseOfLoan', 'TotalLiabilities', 
                              'TotalIncome', 'DebtToIncome', 'FreeCash', 'NewCreditCustomer', 'CreditScoreEsMicroL', 
                              'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
                              'Age', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'HomeOwnershipType', 
                              'Rating', 'Restructured']
        
        expreturn_df = df[expreturn_features]
        X = pd.DataFrame(self.expreturn_scaler_x.transform(expreturn_df), columns=expreturn_df.columns)
        y_pred = self.expreturn_model.predict(X).reshape(-1, 1)
        exp_return = self.expreturn_scaler_y.inverse_transform(y_pred)
        
        return np.log1p(exp_return)
    
    # Defining the fucntion for predicting the interest rate.

     def predict_interest(self, df):
        interest_features = ['AppliedAmount', 'Amount', 'UseOfLoan', 'NewCreditCustomer', 'Age', 'Gender', 
                             'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'OccupationArea', 
                             'TotalIncome', 'TotalLiabilities', 'DebtToIncome', 'FreeCash', 'HomeOwnershipType', 
                             'CreditScoreEsMicroL', 'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 
                             'AmountOfPreviousLoansBeforeLoan', 'ExpectedReturn', 'ProbabilityOfDefault', 'Rating', 
                             'Restructured']
        
        interest_df = df[interest_features]
        X = pd.DataFrame(self.interest_scaler_x.transform(interest_df), columns=interest_df.columns)
        y_pred = self.interest_model.predict(X).reshape(-1, 1)
        interest = self.interest_scaler_y.inverse_transform(y_pred)
        
        print("Interest Amount: " + str(interest))
        return interest
    
    # Defining the function for taking the input and giving the predictions for loan and interest.
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





