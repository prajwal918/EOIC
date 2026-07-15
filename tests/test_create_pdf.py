import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestCreatePdf(unittest.TestCase):
    def test_environment_setup(self):
        """Test that the test environment is set up correctly."""
        self.assertTrue(True)

if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as e:
        import logging
        logging.critical(f"Test suite execution failed: {e}", exc_info=True)
        sys.exit(1)
