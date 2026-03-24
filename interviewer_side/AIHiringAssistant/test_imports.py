print("Starting import test...")
try:
    import pandas
    print("Pandas imported")
    import numpy
    print("Numpy imported")
    import sklearn
    print("Sklearn imported")
except ImportError as e:
    print(f"Import Error: {e}")
except Exception as e:
    print(f"Error: {e}")
print("End.")
