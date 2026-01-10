import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

print(f"Connecting to {url}...")

try:
    supabase: Client = create_client(url, key)
    # Try one simple read (e.g. users or just health)
    # Since we can't query tables that don't exist, we can try auth or basic check
    print("Client initialized. Checking Auth...")
    
    # Check if we can list users (requires service role)
    # users = supabase.auth.admin.list_users()
    # print(f"Connection Successful! Found {len(users.users)} users in Auth.")
    
    # Or try to select from a non-existent table to spark a specific error (404 vs 401)
    res = supabase.table("users").select("*").execute()
    print("Table 'users' query result:", res)
    
except Exception as e:
    print(f"Connection Failed: {e}")
