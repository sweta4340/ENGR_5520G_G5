import unittest
import joblib
import pandas as pd
import numpy as np
import sys
from Parse_Input import LoanProcessor

class TestLoanAmountTolerance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Using this method to load all the necessary encoder and scalers.
        cls.encoder = joblib.load('label_encoders.pkl')
        cls.loan_scaler_x = joblib.load('Loan_Amount_Prediction/loan_scaler_X.pkl')
        cls.loan_scaler_y = joblib.load('Loan_Amount_Prediction/loan_scaler_y.pkl')
        cls.defaultprob_scaler_x = joblib.load('Default_Probability_Prediction/defaultprob_scaler_X.pkl')
        cls.defaultprob_scaler_y = joblib.load('Default_Probability_Prediction/defaultprob_scaler_y.pkl')
        cls.expreturn_scaler_x = joblib.load('Expected_Return_Prediction/expreturn_scaler_X.pkl')
        cls.expreturn_scaler_y = joblib.load('Expected_Return_Prediction/expreturn_scaler_y.pkl')
        cls.interest_scaler_x = joblib.load('Interest_Rate_Prediction/interest_scaler_X.pkl')
        cls.interest_scaler_y = joblib.load('Interest_Rate_Prediction/interest_scaler_y.pkl')

        
    # Defining the test case for testing the correctness of the loan amount prediction. To check if the predicted value falls within the expected range.
    
    
    # Edge case where all the inputs are either zero or unknown. Difficult to determine the prediction.
    '''
    def test_loan_with_zero_unknown(self):
        test_case_1 = {
            'NewCreditCustomer': 'New_credit_Customer',
            'VerificationType': 'Income_unverified',
            'Age': 0,
            'Gender': 'Unknown',
            'AppliedAmount': 0,
            'UseOfLoan': 'Not_set',
            'EmploymentStatus': 'Unknown',
            'EmploymentDurationCurrentEmployer': 'Not-known',
            'OccupationArea': 'Not_specified',
            'HomeOwnershipType': 'Unknown',
            'TotalIncome': 0,
            'TotalLiabilities': 0,
            'DebtToIncome': 0,
            'FreeCash': 0,
            'Rating': 'A',
            'CreditScoreEsMicroL': 'M9',
            'CreditScoreEeMini': 0,
            'NoOfPreviousLoansBeforeLoan': 0,
            'AmountOfPreviousLoansBeforeLoan': 0 }
            
        loan_processor = LoanProcessor(
        self.encoder, self.loan_scaler_x, self.loan_scaler_y,
        self.defaultprob_scaler_x, self.defaultprob_scaler_y,
        self.expreturn_scaler_x, self.expreturn_scaler_y,
        self.interest_scaler_x, self.interest_scaler_y)


        min_amount = 740
        max_amount = 3825
            
        # Edge case where the inputs are either zero or unknown
        df = loan_processor.data_preprocessor(test_case_1)
        loan_amount = loan_processor.predict_loan(df)

        print("Edge case where the inputs are either zero or unknown")
        self.assertGreaterEqual(loan_amount, min_amount,
                                    f"Loan amount is below the minimum expected: {loan_amount}")
        self.assertLessEqual(loan_amount, max_amount,
                                 f"Loan amount is above the maximum expected: {loan_amount}")
        
    # Case when person has high liabilites applying for high amount.
    def test_loan_with_high_appliedamount(self):
        test_case_2 = {
            'NewCreditCustomer': 'Existing_credit_customer',              
            'VerificationType': 'Income_verified',          
            'Age': 45,                             
            'Gender': 'Female',                    
            'AppliedAmount': 100000,               # Extremely high loan amount
            'UseOfLoan': 'Business',               
            'EmploymentStatus': 'Self-Employed',       
            'EmploymentDurationCurrentEmployer': 'UpTo5Years',
            'OccupationArea': 'Real_estate',             
            'HomeOwnershipType': 'Mortgage',           
            'TotalIncome': 200000,                
            'TotalLiabilities':  12400001,    # Extremely high liabilities         
            'DebtToIncome': 0.25,                  
            'FreeCash': 15.0,                     
            'Rating': 'F',                         
            'CreditScoreEsMicroL': 'M',           
            'CreditScoreEeMini': 730,             
            'NoOfPreviousLoansBeforeLoan': 2,    
            'AmountOfPreviousLoansBeforeLoan': 50000 }
        
        loan_processor = LoanProcessor(
        self.encoder, self.loan_scaler_x, self.loan_scaler_y,
        self.defaultprob_scaler_x, self.defaultprob_scaler_y,
        self.expreturn_scaler_x, self.expreturn_scaler_y,
        self.interest_scaler_x, self.interest_scaler_y)

        min_amount = 740
        max_amount = 3825
            
        # Predicting loan for person applying for high loan.
        df = loan_processor.data_preprocessor(test_case_2)
        loan_amount = loan_processor.predict_loan(df)

        print("Predicting loan for person applying for high loan.")
        self.assertGreaterEqual(loan_amount, min_amount,
                                    f"Loan amount is below the minimum expected: {loan_amount}")
        self.assertLessEqual(loan_amount, max_amount,
                                 f"Loan amount is above the maximum expected: {loan_amount}") 
      '''  
    # Ideal ouput scenario.        
    def test_loan_with_ideal_output(self):
        test_case_3 = {
            'NewCreditCustomer': 'Existing_credit_customer',              
            'VerificationType': 'Income_unverified',          
            'Age': 50,                             
            'Gender': 'Female',                    
            'AppliedAmount': 3000,               
            'UseOfLoan': 'Business',               
            'EmploymentStatus': 'Entrepreneur',       
            'EmploymentDurationCurrentEmployer': 'MoreThan5Years',
            'OccupationArea': 'Retail_and_wholesale',             
            'HomeOwnershipType': 'Owner',           
            'TotalIncome': 900,                
            'TotalLiabilities': 740.45,            
            'DebtToIncome': 30.58,                  
            'FreeCash': 78.8,                     
            'Rating': 'B',                         
            'CreditScoreEsMicroL': 'M',           
            'CreditScoreEeMini': 1000,             
            'NoOfPreviousLoansBeforeLoan': 1.0,    
            'AmountOfPreviousLoansBeforeLoan': 1800.0 }
        
        loan_processor = LoanProcessor(
        self.encoder, self.loan_scaler_x, self.loan_scaler_y,
        self.defaultprob_scaler_x, self.defaultprob_scaler_y,
        self.expreturn_scaler_x, self.expreturn_scaler_y,
        self.interest_scaler_x, self.interest_scaler_y)

        min_amount = 740
        max_amount = 3825
            
        # Predicting loan for ideal input.
        df = loan_processor.data_preprocessor(test_case_3)
        loan_amount = loan_processor.predict_loan(df)

        print("Predicting loan for ideal case.")
        self.assertGreaterEqual(loan_amount, min_amount,
                                    f"Loan amount is below the minimum expected: {loan_amount}")
        self.assertLessEqual(loan_amount, max_amount,
                                 f"Loan amount is above the maximum expected: {loan_amount}")   
        
if __name__ == '__main__':
    unittest.main()
