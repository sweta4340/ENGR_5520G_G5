import unittest
import joblib
import pandas as pd
import numpy as np
import sys
from Parse_Input import LoanProcessor

class TestLoanAmountTolerance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This method will run once before all tests in this class.
        Use this to load models and scalers.
        """
        cls.encoder = joblib.load('data_encoder.pkl')
        cls.loan_scaler_x = joblib.load('Loan_Amount_Prediction/loan_scaler_X.pkl')
        cls.loan_scaler_y = joblib.load('Loan_Amount_Prediction/loan_scaler_y.pkl')
        cls.defaultprob_scaler_x = joblib.load('Default_Probability_Prediction/defaultprob_scaler_X.pkl')
        cls.defaultprob_scaler_y = joblib.load('Default_Probability_Prediction/defaultprob_scaler_y.pkl')
        cls.expreturn_scaler_x = joblib.load('Expected_Return_Prediction/expreturn_scaler_X.pkl')
        cls.expreturn_scaler_y = joblib.load('Expected_Return_Prediction/expreturn_scaler_y.pkl')
        cls.interest_scaler_x = joblib.load('Interest_Rate_Prediction/interest_scaler_X.pkl')
        cls.interest_scaler_y = joblib.load('Interest_Rate_Prediction/interest_scaler_y.pkl')

    def test_loan(self):
        test_case_1 = {
            'NewCreditCustomer': 0,
            'VerificationType': 'Income_unverified',
            'Age': 0,
            'Gender': 'Unknown',
            'AppliedAmount': 0,
            'UseOfLoan': 'Not_set',
            'EmploymentStatus': 'Unknown',
            'EmploymentDurationCurrentEmployer': 'Not_known',
            'OccupationArea': 'Not_specified',
            'HomeOwnershipType': 'Unknown',
            'TotalIncome': 0,
            'TotalLiabilities': 0,
            'DebtToIncome': 0,
            'FreeCash': 0,
            'Rating': 0,
            'CreditScoreEsMicroL': 'M9',
            'CreditScoreEeMini': 0,
            'NoOfPreviousLoansBeforeLoan': 0,
            'AmountOfPreviousLoansBeforeLoan': 0
        }

        # Create loan processor instance
        loan_processor = LoanProcessor(
            self.encoder, self.loan_scaler_x, self.loan_scaler_y,
            self.defaultprob_scaler_x, self.defaultprob_scaler_y,
            self.expreturn_scaler_x, self.expreturn_scaler_y,
            self.interest_scaler_x, self.interest_scaler_y
        )

        df = loan_processor.data_preprocessor(test_case_1)
        loan_amount = loan_processor.predict_loan(df)

        min_amount = 740
        max_amount = 3825

        # Assert the loan amount is within the expected range
        self.assertGreaterEqual(loan_amount, min_amount,
                                f"Loan amount is below the minimum expected: {loan_amount}")
        self.assertLessEqual(loan_amount, max_amount,
                             f"Loan amount is above the maximum expected: {loan_amount}")

    @classmethod
    def tearDownClass(cls):
        """
        This method will run once after all tests in this class.
        You can use this to clean up any resources, if necessary.
        """
        pass


if __name__ == '__main__':
    unittest.main()
