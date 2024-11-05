#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import unittest
class TestMathFunctions(unittest.TestCase):
    def sample_test(self):
        self.assertEqual(3, 3)
        self.assertEqual(-1,0)

if __name__ == '__main__':
    unittest.main()

