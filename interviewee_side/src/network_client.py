import os
import sys
import shutil
import time
from pathlib import Path
from typing import Tuple
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from the correct location
_env_candidates = []
if getattr(sys, 'frozen', False):
    _env_candidates.append(Path(sys._MEIPASS) / "src" / ".env")
    _env_candidates.append(Path(sys.executable).parent / ".env")
    _env_candidates.append(Path(sys.executable).parent / "src" / ".env")
_env_candidates.append(Path(__file__).resolve().parent / ".env")
_env_candidates.append(Path.cwd() / ".env")
_env_candidates.append(Path.cwd() / "src" / ".env")

for _env_path in _env_candidates:
    if _env_path.exists():
        load_dotenv(str(_env_path))
        break

# Setup Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def zip_session_data(session_path: str) -> str:
    """Compresses the session folder into a .zip file."""
    base_name = str(session_path)
    zip_path = shutil.make_archive(base_name, 'zip', session_path)
    return zip_path

def send_session_to_cloud(session_path: str) -> Tuple[bool, str]:
    """
    Zips the session data and uploads it to Supabase Storage.
    
    Args:
        session_path: Path to the session folder to send.
        
    Returns:
        (success_boolean, message_string)
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return False, "Cloud Storage keys missing. Check your .env file."
        
    if not os.path.exists(session_path):
        return False, "Session data not found."
        
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 1. Zip the folder
        zip_file_path = zip_session_data(session_path)
        
        # Unique remote filename
        filename = os.path.basename(zip_file_path)
        timestamp = str(int(time.time()))
        remote_path = f"uploads/{timestamp}_{filename}"
        
        # 2. Upload it to the "sessions" bucket
        with open(zip_file_path, 'rb') as f:
            res = supabase.storage.from_("sessions").upload(
                file=f,
                path=remote_path,
                file_options={"content-type": "application/zip"}
            )
            
        # 3. Clean up the zip file after sending
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
            
        return True, "Session securely uploaded to cloud successfully!"
            
    except Exception as e:
        # Cleanup zip if error occurs mid-way
        if 'zip_file_path' in locals() and os.path.exists(zip_file_path):
            os.remove(zip_file_path)
        return False, f"Upload failed: {str(e)}"
