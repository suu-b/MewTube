import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Common supabase client for the app
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)