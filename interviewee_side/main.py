#!/usr/bin/env python3
"""
AI Hiring Assistant - Application Entry Point

A PyQt6 desktop application for AI-powered recruitment workflow
with real-time computer vision capabilities.

All data is stored locally in ./user_data/{session_id}/
No external services or cloud storage are used.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import run_app


if __name__ == "__main__":
    run_app()
