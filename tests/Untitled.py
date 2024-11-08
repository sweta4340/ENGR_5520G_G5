#!/usr/bin/env python
# coding: utf-8

# In[7]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import sys
sys.path.append("C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5")  # Only the directory
from Parse_Input import LoanProcessor
import unittest
class TestLoanAmountTolerance(unittest.TestCase):
    def tolerenace_test(self):
        #self.assertEqual(3, 3)
        #self.assertEqual(-1,0)
        
        test_case_1 = {
            'NewCreditCustomer': 0,                # No new credit customer, but no data on previous credit
            'VerificationType': 'Income_unverified',             # No verification type specified
            'Age': 0,                              # Age as zero (unrealistic, but tests edge case handling)
            'Gender': 'Unknown',                   # Gender not specified
            'AppliedAmount': 0,                     # No loan amount applied for
            'UseOfLoan': 'Not_set',                    # No loan purpose specified
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

        encoder = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/data_encoder.pkl')
        loan_scaler_x = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Loan_Amount_Prediction/loan_scaler_X.pkl')
        loan_scaler_y = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Loan_Amount_Prediction/loan_scaler_y.pkl')

        defaultprob_scaler_x = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Default_Probability_Prediction/defaultprob_scaler_X.pkl')
        defaultprob_scaler_y = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Default_Probability_Prediction/defaultprob_scaler_y.pkl')

        expreturn_scaler_x = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Expected_Return_Prediction/expreturn_scaler_X.pkl')
        expreturn_scaler_y = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Expected_Return_Prediction/expreturn_scaler_y.pkl')

        interest_scaler_x = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Interest_Rate_Prediction/interest_scaler_X.pkl')
        interest_scaler_y = joblib.load('C:/Users/KRISHNA/Desktop/SHWETA/Fall 2024/ENGR_5520G_G5/Interest_Rate_Prediction/interest_scaler_y.pkl')



        loan_processor = LoanProcessor(encoder, loan_scaler_x, loan_scaler_y, defaultprob_scaler_x, defaultprob_scaler_y, expreturn_scaler_x,       expreturn_scaler_y, interest_scaler_x, interest_scaler_y)

        df = loan_processor.data_preprocessor(test_case_1)
        loan_amount = loan_processor.predict_loan(df)

        min_amount = 740
        max_amount = 3825
        
        self.assertGreaterEqual(loan_amount, min_amount, 
                                f"Loan amount is below the minimum expected: {loan_amount}")
        self.assertLessEqual(loan_amount, max_amount, 
                             f"Loan amount is above the maximum expected: {loan_amount}")

if __name__ == '__main__':
    unittest.main()



# In[ ]:




