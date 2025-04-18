import sys
import os

# Adds get_launches Lambda directory to PYTHONPATH
lambda_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../aws_lambda/get_launches'))
if lambda_path not in sys.path:
    sys.path.insert(0, lambda_path)
