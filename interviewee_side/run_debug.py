import sys
import traceback
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        from src.app import run_app
        run_app()
    except Exception as e:
        with open("crash_debug.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        print("CRASH LOGGED TO crash_debug.txt")
