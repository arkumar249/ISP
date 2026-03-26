import json
import numpy as np
from predict import predict

def get_json_prediction(file_path):
    try:
        raw_result = predict(file_path)
        
        # FIX: Convert NumPy array to a standard Python list
        if isinstance(raw_result, np.ndarray):
            raw_result = raw_result.tolist()
        
        output = {
            "status": "success",
            "input_file": file_path,
            "prediction": raw_result
        }
        
        return json.dumps(output, indent=4)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, indent=4)

# Usage
json_output = get_json_prediction("data/session_20/physio.csv")
print(json_output)