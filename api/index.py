import os
import sys

# Ensure parent directory is in sys.path so server.py and modules can be imported
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from server import app
