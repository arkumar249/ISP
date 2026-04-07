import os
import zipfile
import shutil
from dotenv import load_dotenv
from supabase import create_client, Client

def sync_sessions_from_cloud() -> int:
    """
    Connects securely to Supabase Storage, checks for newly uploaded .zip
    candidates, downloads them to the local Interviewer '/user_data/' directory,
    and unzips them for processing.
    
    Returns:
        Number of new candidate sessions synced.
    """
    load_dotenv()
    
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Missing Supabase credentials in .env file.")
        return 0

    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Base user data directory
        base_dir = "user_data"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            
        # Get all files in the "sessions" bucket under "uploads/"
        response = supabase.storage.from_("sessions").list("uploads")
        files = response if isinstance(response, list) else []
        
        new_sessions_synced = 0
        
        for file_meta in files:
            filename = file_meta.get("name")
            if not filename or not filename.endswith(".zip"):
                continue
                
            remote_path = f"uploads/{filename}"
            # Use the part after the timestamp as the desired folder name, minus the .zip
            # e.g. 1712391290_session_20260330_123456.zip -> session_20260330_123456
            if "_" in filename:
                folder_name = filename.split("_", 1)[1].replace(".zip", "")
            else:
                folder_name = filename.replace(".zip", "")
                
            local_folder = os.path.join(base_dir, folder_name)
            local_zip_path = os.path.join(base_dir, filename)
            
            # Check if we already grabbed it
            if os.path.exists(local_folder):
                continue
                
            # Download the file
            print(f"Downloading {filename} from cloud...")
            with open(local_zip_path, 'wb') as f:
                res = supabase.storage.from_("sessions").download(remote_path)
                f.write(res)
                
            # Extract
            print(f"Extracting to {local_folder}...")
            with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
                # To prevent creating double folders, we pass base_dir
                # But if the zip already contains the folder, extracting directly to base_dir gets us user_data/session_xxx
                zip_ref.extractall(base_dir)
                
            new_sessions_synced += 1
            
            # Cleanup local zip
            if os.path.exists(local_zip_path):
                os.remove(local_zip_path)
                
        return new_sessions_synced
        
    except Exception as e:
        print(f"Failed to sync from Supabase: {e}")
        return 0
