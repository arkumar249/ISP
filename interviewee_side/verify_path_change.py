
import sys
import os
from pathlib import Path

# Add src to path just like main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_manager import DataManager

def verify():
    dm = DataManager()
    print(f"Base Path: {dm.base_path}")
    print(f"Resolved Path: {dm.base_path.resolve()}")
    
    expected_part = "interviewer_side"
    if expected_part in str(dm.base_path) and "user_data" in str(dm.base_path):
        print("SUCCESS: Path contains expected components.")
    else:
        print("FAILURE: Path does not look right.")

if __name__ == "__main__":
    verify()
