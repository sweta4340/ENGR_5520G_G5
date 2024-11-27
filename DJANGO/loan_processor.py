# import pandas as pd
# import numpy as np
# import joblib

# class LoanProcessor:
#     def __init__(self, encoder, loan_scaler_x, loan_scaler_y):
#         # Initializing the encoder and scalers.
#         self.encoder = encoder
#         self.loan_scaler_x = loan_scaler_x
#         self.loan_scaler_y = loan_scaler_y
        
#         # Loading the loan prediction model.
#         self.loan_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_model.joblib")
        
#     def data_preprocessor(self, data):
#         """Process input data (encoding and skewness correction)."""
#         df = pd.DataFrame([data])

#         # Debugging: Check the data received in the preprocessor
#         print("Raw Data for Preprocessing:", df)

#         # Identify categorical columns
#         categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        
#         # Apply specific encoding for each categorical column
#         for column in categorical_columns:
#             if column in self.encoder:
#                 # Use the encoder for the specific column
#                 encoder = self.encoder[column]
#                 df[column] = encoder.transform(df[column])  # Using the specific encoder for each column
#             else:
#                 # If no encoder is available, convert categorical values to numeric codes
#                 df[column] = df[column].astype('category').cat.codes
        
#         # Skewness correction for features
#         skewed_features = df.apply(lambda x: x.skew()).sort_values(ascending=False)
#         threshold = 2
#         features_to_transform = skewed_features[skewed_features.abs() > threshold].index.tolist()

#         for column in features_to_transform:
#             if skewed_features[column] > 0:
#                 if (df[column] >= 0).all():
#                     df[column] = np.log1p(df[column])
#                 else:
#                     min_value = df[column].min()
#                     df[column] = df[column] + abs(min_value) + 1
#                     df[column] = np.log1p(df[column])
        
#         return df
    
#     def predict_loan(self, df):
#         """Predict loan amount."""
#         loan_features = ['NewCreditCustomer', 'VerificationType', 'Age', 'Gender',
#                          'AppliedAmount', 'UseOfLoan', 'EmploymentStatus', 
#                          'EmploymentDurationCurrentEmployer', 'OccupationArea', 
#                          'HomeOwnershipType', 'TotalIncome', 'TotalLiabilities', 
#                          'DebtToIncome', 'FreeCash', 'Rating', 'CreditScoreEsMicroL', 
#                          'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 
#                          'AmountOfPreviousLoansBeforeLoan']
        
#         # Debugging: Print missing columns before raising an error
#         missing_columns = set(loan_features) - set(df.columns)
#         if missing_columns:
#             print(f"Missing columns: {missing_columns}")
#             raise KeyError(f"Missing columns: {missing_columns}")

#         loan_df = df[loan_features]
#         X = pd.DataFrame(self.loan_scaler_x.transform(loan_df), columns=loan_df.columns)
#         y_pred = self.loan_model.predict(X).reshape(-1, 1)
#         loan_amount = self.loan_scaler_y.inverse_transform(y_pred)
        
#         return loan_amount

#     def parse_input(self, request):
#         """Process input data, make loan predictions, and return the results."""
#         df = self.data_preprocessor(request)

#         # Debugging: check the data after preprocessing
#         print("Data after Preprocessing:", df)
        
#         # Make predictions
#         df['Amount'] = self.predict_loan(df)
        
#         return df
# import pandas as pd
# import numpy as np
# import joblib

# class LoanProcessor:
#     def __init__(self, encoder, loan_scaler_x, loan_scaler_y, defaultprob_scaler_x, defaultprob_scaler_y, expreturn_scaler_x, expreturn_scaler_y):
#         # Initialize encoders and scalers
#         self.encoder = encoder
#         self.loan_scaler_x = loan_scaler_x
#         self.loan_scaler_y = loan_scaler_y
#         self.defaultprob_scaler_x = defaultprob_scaler_x
#         self.defaultprob_scaler_y = defaultprob_scaler_y
#         self.expreturn_scaler_x = expreturn_scaler_x
#         self.expreturn_scaler_y = expreturn_scaler_y

#         # Load models
#         self.loan_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_model.joblib")
#         self.defaultprob_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\defaultprob_model.joblib")
#         self.expreturn_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\expreturn_model.joblib")

#     def data_preprocessor(self, data):
#         """Process input data (encoding and skewness correction)."""
#         df = pd.DataFrame([data])
#         print("Raw Data for Preprocessing:", df)

#         # Encoding categorical columns
#         categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
#         for column in categorical_columns:
#             if column in self.encoder:
#                 encoder = self.encoder[column]
#                 df[column] = encoder.transform(df[column])
#             else:
#                 df[column] = df[column].astype('category').cat.codes

#         # Skewness correction
#         skewed_features = df.apply(lambda x: x.skew()).sort_values(ascending=False)
#         threshold = 2
#         features_to_transform = skewed_features[skewed_features.abs() > threshold].index.tolist()
#         for column in features_to_transform:
#             if skewed_features[column] > 0:
#                 if (df[column] >= 0).all():
#                     df[column] = np.log1p(df[column])
#                 else:
#                     min_value = df[column].min()
#                     df[column] = df[column] + abs(min_value) + 1
#                     df[column] = np.log1p(df[column])

#         return df

#     def predict_loan(self, df):
#         """Predict loan amount."""
#         loan_features = ['NewCreditCustomer', 'VerificationType', 'Age', 'Gender',
#                          'AppliedAmount', 'UseOfLoan', 'EmploymentStatus', 
#                          'EmploymentDurationCurrentEmployer', 'OccupationArea', 
#                          'HomeOwnershipType', 'TotalIncome', 'TotalLiabilities', 
#                          'DebtToIncome', 'FreeCash', 'Rating', 'CreditScoreEsMicroL', 
#                          'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 
#                          'AmountOfPreviousLoansBeforeLoan']

#         missing_columns = set(loan_features) - set(df.columns)
#         if missing_columns:
#             raise KeyError(f"Missing columns: {missing_columns}")

#         loan_df = df[loan_features]
#         X = pd.DataFrame(self.loan_scaler_x.transform(loan_df), columns=loan_df.columns)
#         y_pred = self.loan_model.predict(X).reshape(-1, 1)
#         loan_amount = self.loan_scaler_y.inverse_transform(y_pred)
#         return loan_amount

#     def predict_prob(self, df):
#         """Predict default probability."""
#         prob_features = ['AppliedAmount', 'Amount', 'UseOfLoan', 'TotalLiabilities', 'TotalIncome', 
#                          'DebtToIncome', 'FreeCash', 'NewCreditCustomer', 'CreditScoreEsMicroL', 
#                          'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
#                          'Age', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'HomeOwnershipType', 
#                          'Rating', 'Restructured']

#         prob_df = df[prob_features]
#         X = pd.DataFrame(self.defaultprob_scaler_x.transform(prob_df), columns=prob_df.columns)
#         y_pred = self.defaultprob_model.predict(X).reshape(-1, 1)
#         default_prob = self.defaultprob_scaler_y.inverse_transform(y_pred)
#         return default_prob

#     def predict_expreturn(self, df):
#         """Predict expected return."""
#         expreturn_features = ['AppliedAmount', 'Amount', 'ProbabilityOfDefault', 'UseOfLoan', 'TotalLiabilities', 
#                               'TotalIncome', 'DebtToIncome', 'FreeCash', 'NewCreditCustomer', 'CreditScoreEsMicroL', 
#                               'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
#                               'Age', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'HomeOwnershipType', 
#                               'Rating', 'Restructured']

#         expreturn_df = df[expreturn_features]
#         X = pd.DataFrame(self.expreturn_scaler_x.transform(expreturn_df), columns=expreturn_df.columns)
#         y_pred = self.expreturn_model.predict(X).reshape(-1, 1)
#         exp_return = self.expreturn_scaler_y.inverse_transform(y_pred)
#         return exp_return

#     def parse_input(self, request):
#         """Process input data and make predictions for loan, default probability, and expected return."""
#         df = self.data_preprocessor(request)
#         print("Data after Preprocessing:", df)

#         # Make predictions
#         df['Amount'] = self.predict_loan(df)
#         df['ProbabilityOfDefault'] = self.predict_prob(df)
#         df['ExpectedReturn'] = self.predict_expreturn(df)

#         return df

import pandas as pd
import numpy as np
import joblib

class LoanProcessor:
    def __init__(self, encoder, loan_scaler_x, loan_scaler_y, defaultprob_scaler_x, defaultprob_scaler_y,
                 expreturn_scaler_x, expreturn_scaler_y, interest_scaler_x, interest_scaler_y):
        # Initialize encoders and scalers
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
        self.loan_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_model.joblib")
        self.defaultprob_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\defaultprob_model.joblib")
        self.expreturn_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\expreturn_model.joblib")
        self.interest_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\interest_model_NEW.joblib")

    def data_preprocessor(self, data):
        """Process input data (encoding and skewness correction)."""
        df = pd.DataFrame([data])
        
        # Encoding categorical columns
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        for column in categorical_columns:
            if column in self.encoder:
                encoder = self.encoder[column]
                df[column] = encoder.transform(df[column])
            else:
                df[column] = df[column].astype('category').cat.codes

        # Skewness correction
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
        """Predict loan amount."""
        loan_features = ['NewCreditCustomer', 'VerificationType', 'Age', 'Gender',
                         'AppliedAmount', 'UseOfLoan', 'EmploymentStatus', 
                         'EmploymentDurationCurrentEmployer', 'OccupationArea', 
                         'HomeOwnershipType', 'TotalIncome', 'TotalLiabilities', 
                         'DebtToIncome', 'FreeCash', 'Rating', 'CreditScoreEsMicroL', 
                         'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 
                         'AmountOfPreviousLoansBeforeLoan']

        loan_df = df[loan_features]
        X = pd.DataFrame(self.loan_scaler_x.transform(loan_df), columns=loan_df.columns)
        y_pred = self.loan_model.predict(X).reshape(-1, 1)
        loan_amount = self.loan_scaler_y.inverse_transform(y_pred)
        return loan_amount

    def predict_prob(self, df):
        """Predict default probability."""
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

    def predict_expreturn(self, df):
        """Predict expected return."""
        expreturn_features = ['AppliedAmount', 'Amount', 'ProbabilityOfDefault', 'UseOfLoan', 'TotalLiabilities', 
                              'TotalIncome', 'DebtToIncome', 'FreeCash', 'NewCreditCustomer', 'CreditScoreEsMicroL', 
                              'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
                              'Age', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'HomeOwnershipType', 
                              'Rating', 'Restructured']

        expreturn_df = df[expreturn_features]
        X = pd.DataFrame(self.expreturn_scaler_x.transform(expreturn_df), columns=expreturn_df.columns)
        y_pred = self.expreturn_model.predict(X).reshape(-1, 1)
        exp_return = self.expreturn_scaler_y.inverse_transform(y_pred)
        return exp_return

    # def predict_interest(self, df):
    #     """Predict interest rate."""
    #     interest_features = [
    #     'AppliedAmount', 'Amount', 'Interest', 'LoanDuration', 'UseOfLoan', 'NewCreditCustomer', 
    #     'Age', 'Gender', 'EmploymentStatus', 'Education', 'EmploymentDurationCurrentEmployer',
    #     'OccupationArea', 'TotalIncome', 'TotalLiabilities', 'DebtToIncome', 'FreeCash', 
    #     'HomeOwnershipType', 'CreditScoreEsMicroL', 'CreditScoreEeMini', 
    #     'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 'ExpectedReturn', 
    #     'ProbabilityOfDefault', 'Rating', 'Restructured'
    # ]
    #     missing_columns = [col for col in interest_features if col not in df.columns]
    #     if missing_columns:
    #         raise ValueError(f"Missing columns in input data: {', '.join(missing_columns)}")

    #     print(df.columns)  # This will help you check if any columns are missing
     
    #     interest_df = df[interest_features]
    #     X = pd.DataFrame(self.interest_scaler_x.transform(interest_df), columns=interest_df.columns)
    #     y_pred = self.interest_model.predict(X).reshape(-1, 1)
    #     interest_rate = self.interest_scaler_y.inverse_transform(y_pred)
    # #     return interest_rate
    def predict_interest(self, df):
        """
        Predict the interest rate based on the input DataFrame containing loan application features.
        """

        # Define the required feature names for the model
        interest_features = [
            'AppliedAmount', 'Amount', 'UseOfLoan','NewCreditCustomer', 'Age', 'Gender',
            'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'OccupationArea', 
            'TotalIncome', 'TotalLiabilities', 'DebtToIncome', 'FreeCash','HomeOwnershipType','CreditScoreEsMicroL', 
            'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
            'ExpectedReturn','ProbabilityOfDefault', 'Rating', 'Restructured'
        ]
        
        # Check for missing or extra columns in input data
        missing_columns = [col for col in interest_features if col not in df.columns]
        extra_columns = [col for col in df.columns if col not in interest_features]
        
        if missing_columns:
            raise ValueError(f"Missing columns in input data: {', '.join(missing_columns)}")
        if extra_columns:
            print(f"Extra columns in input data: {', '.join(extra_columns)}")
        
        # Subset the DataFrame to include only the required columns, discarding extra ones
        df = df[interest_features]

        # Ensure the columns are in the correct order (use the predefined list)
        df = df[interest_features]

        try:
            # Scale the input features using the fitted scaler
            X_scaled = pd.DataFrame(self.interest_scaler_x.transform(df), columns=df.columns)

            # Debug: Print the scaled input data to verify it's correctly processed
            print("Scaled Input Data:\n", X_scaled)

            # Predict interest rate using the model
            y_pred = self.interest_model.predict(X_scaled).reshape(-1, 1)

            # Debug: Print the predicted values before inverse transformation
            print("Predicted Interest Rate (before inverse transformation):\n", y_pred)

            # Inverse transform the predicted interest rate if needed
            interest_rate = self.interest_scaler_y.inverse_transform(y_pred)

            # Debug: Print the final predicted interest rate
            print("Final Predicted Interest Rate (after inverse transformation):\n", interest_rate)

            return interest_rate[0][0]  # Return the interest rate as a scalar value

        except Exception as e:
            print(f"Error in prediction process: {e}")
            raise e 
    # def predict_interest(self, df):
    #     """Predict interest rate."""
    #     interest_features = [
    #         'NewCreditCustomer', 'Age', 'Gender','AppliedAmount', 'Amount', 'UseOfLoan', 
    #         'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'OccupationArea', 'HomeOwnershipType',
    #         'TotalIncome', 'TotalLiabilities', 'DebtToIncome', 'FreeCash', 'CreditScoreEsMicroL', 
    #         'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
    #         'Rating','Restructured', 'ProbabilityOfDefault', 'ExpectedReturn'
    #     ]
        
    #     # Check for missing or extra columns in input data
    #     missing_columns = [col for col in interest_features if col not in df.columns]
    #     extra_columns = [col for col in df.columns if col not in interest_features]
        
    #     if missing_columns:
    #         raise ValueError(f"Missing columns in input data: {', '.join(missing_columns)}")
    #     if extra_columns:
    #         print(f"Extra columns in input data: {', '.join(extra_columns)}")
            
    #     # Subset the DataFrame to include only the required columns, discarding extra ones
    #     df = df[interest_features]

    #     # Ensure the columns are in the correct order (use the predefined list)
    #     df = df[interest_features]

    #     try:
    #         # Scale the input features using the fitted scaler
    #         X_scaled = pd.DataFrame(self.interest_scaler_x.transform(df), columns=df.columns)

    #         # Predict interest rate using the model
    #         y_pred = self.interest_model.predict(X_scaled).reshape(-1, 1)

    #         # Inverse transform the predicted interest rate if needed
    #         interest_rate = self.interest_scaler_y.inverse_transform(y_pred)

    #         return interest_rate[0][0]  # Return the interest rate as a scalar value
            
    #     except Exception as e:
    #         print(f"Error in prediction process: {e}")
    #         raise e



    def parse_input(self, request):
        """Process input data and make predictions for loan, default probability, expected return, and interest."""
        df = self.data_preprocessor(request)
        
        # Make predictions
        df['Amount'] = self.predict_loan(df)
        df['ProbabilityOfDefault'] = self.predict_prob(df)
        df['ExpectedReturn'] = self.predict_expreturn(df)
        df['InterestRate'] = self.predict_interest(df)

        return df

# import pandas as pd
# import numpy as np
# import joblib

# class LoanProcessor:
#     def __init__(self, encoder, loan_scaler_x, loan_scaler_y, defaultprob_scaler_x, defaultprob_scaler_y,
#                  expreturn_scaler_x, expreturn_scaler_y, interest_scaler_x, interest_scaler_y):
#         # Initialize encoders and scalers
#         self.encoder = encoder
#         self.loan_scaler_x = loan_scaler_x
#         self.loan_scaler_y = loan_scaler_y
#         self.defaultprob_scaler_x = defaultprob_scaler_x
#         self.defaultprob_scaler_y = defaultprob_scaler_y
#         self.expreturn_scaler_x = expreturn_scaler_x
#         self.expreturn_scaler_y = expreturn_scaler_y
#         self.interest_scaler_x = interest_scaler_x
#         self.interest_scaler_y = interest_scaler_y

#         # Load models
#         self.loan_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\loan_model.joblib")
#         self.defaultprob_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\defaultprob_model.joblib")
#         self.expreturn_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\expreturn_model.joblib")
#         self.interest_model = joblib.load("E:\\DEV AND METHOD\\FSE\\data\\interest_model.joblib")

#     def data_preprocessor(self, data):
#         """Process input data (encoding and skewness correction)."""
#         df = pd.DataFrame([data])
        
#         # Encoding categorical columns
#         categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
#         for column in categorical_columns:
#             if column in self.encoder:
#                 encoder = self.encoder[column]
#                 df[column] = encoder.transform(df[column])
#             else:
#                 df[column] = df[column].astype('category').cat.codes

#         # Skewness correction
#         skewed_features = df.apply(lambda x: x.skew()).sort_values(ascending=False)
#         threshold = 2
#         features_to_transform = skewed_features[skewed_features.abs() > threshold].index.tolist()
#         for column in features_to_transform:
#             if skewed_features[column] > 0:
#                 if (df[column] >= 0).all():
#                     df[column] = np.log1p(df[column])
#                 else:
#                     min_value = df[column].min()
#                     df[column] = df[column] + abs(min_value) + 1
#                     df[column] = np.log1p(df[column])

#         return df

#     def predict_loan(self, df):
#         """Predict loan amount."""
#         loan_features = ['NewCreditCustomer', 'VerificationType', 'Age', 'Gender',
#                          'AppliedAmount', 'UseOfLoan', 'EmploymentStatus', 
#                          'EmploymentDurationCurrentEmployer', 'OccupationArea', 
#                          'HomeOwnershipType', 'TotalIncome', 'TotalLiabilities', 
#                          'DebtToIncome', 'FreeCash', 'Rating', 'CreditScoreEsMicroL', 
#                          'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 
#                          'AmountOfPreviousLoansBeforeLoan']

#         loan_df = df[loan_features]
#         X = pd.DataFrame(self.loan_scaler_x.transform(loan_df), columns=loan_df.columns)
#         y_pred = self.loan_model.predict(X).reshape(-1, 1)
#         loan_amount = self.loan_scaler_y.inverse_transform(y_pred)
#         return loan_amount

#     def predict_prob(self, df):
#         """Predict default probability."""
#         prob_features = ['AppliedAmount', 'Amount', 'UseOfLoan', 'TotalLiabilities', 'TotalIncome', 
#                          'DebtToIncome', 'FreeCash', 'NewCreditCustomer', 'CreditScoreEsMicroL', 
#                          'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
#                          'Age', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'HomeOwnershipType', 
#                          'Rating', 'Restructured']

#         prob_df = df[prob_features]
#         X = pd.DataFrame(self.defaultprob_scaler_x.transform(prob_df), columns=prob_df.columns)
#         y_pred = self.defaultprob_model.predict(X).reshape(-1, 1)
#         default_prob = self.defaultprob_scaler_y.inverse_transform(y_pred)
#         return default_prob

#     def predict_expreturn(self, df):
#         """Predict expected return."""
#         expreturn_features = ['AppliedAmount', 'Amount', 'ProbabilityOfDefault', 'UseOfLoan', 'TotalLiabilities', 
#                               'TotalIncome', 'DebtToIncome', 'FreeCash', 'NewCreditCustomer', 'CreditScoreEsMicroL', 
#                               'CreditScoreEeMini', 'NoOfPreviousLoansBeforeLoan', 'AmountOfPreviousLoansBeforeLoan', 
#                               'Age', 'EmploymentStatus', 'EmploymentDurationCurrentEmployer', 'HomeOwnershipType', 
#                               'Rating', 'Restructured']

#         expreturn_df = df[expreturn_features]
#         X = pd.DataFrame(self.expreturn_scaler_x.transform(expreturn_df), columns=expreturn_df.columns)
#         y_pred = self.expreturn_model.predict(X).reshape(-1, 1)
#         exp_return = self.expreturn_scaler_y.inverse_transform(y_pred)
#         return exp_return

#     def predict_interest(self, df):
#         """Predict interest."""
#         interest_features = ['AppliedAmount', 'Amount', 'UseOfLoan', 'TotalIncome', 'DebtToIncome', 
#                              'FreeCash', 'CreditScoreEsMicroL', 'EmploymentStatus', 'Rating', 
#                              'NoOfPreviousLoansBeforeLoan','Age','AmountOfPreviousLoansBeforeLoan','CreditScoreEeMini', 'EmploymentDurationCurrentEmployer',
#                              'exp_return' ]

#         interest_df = df[interest_features]
#         X = pd.DataFrame(self.interest_scaler_x.transform(interest_df), columns=interest_df.columns)
#         y_pred = self.interest_model.predict(X).reshape(-1, 1)
#         interest = self.interest_scaler_y.inverse_transform(y_pred)
#         return interest

#     def parse_input(self, request):
#         """Process input data and make predictions for loan, default probability, expected return, and interest."""
#         df = self.data_preprocessor(request)

#         # Make predictions
#         df['Amount'] = self.predict_loan(df)
#         df['ProbabilityOfDefault'] = self.predict_prob(df)
#         df['ExpectedReturn'] = self.predict_expreturn(df)
#         df['Interest'] = self.predict_interest(df)

#         return df
