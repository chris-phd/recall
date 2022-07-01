from .context import recall
import unittest

class TestIsEven(unittest.TestCase):
    
    def testIsEven(self):
        self.assertTrue(recall.example.iseven(2))

if __name__ == "__main__":
    unittest.main()
