import sys
import os

print("Verifying imports for main.py...")

try:
    # Mimic main.py imports
    from ui.ml_result_page import MlResultPage
    print("SUCCESS: Imported ui.ml_result_page.MlResultPage")
    
    from ml_stage.predict import predict_personality
    print("SUCCESS: Imported ml_stage.predict.predict_personality")
    
except ImportError as e:
    print(f"FAILURE: ImportError - {e}")
except Exception as e:
    print(f"FAILURE: Exception - {e}")
