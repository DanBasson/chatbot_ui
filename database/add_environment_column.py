#!/usr/bin/env python3
"""
Script to add environment column to existing database tables.
Run this once to update your existing Supabase tables.
"""

from dotenv import load_dotenv
from supabase_client import get_supabase_client

# Load environment variables
load_dotenv()

def add_environment_columns():
    """Add environment columns to existing tables."""
    try:
        client = get_supabase_client()
        
        # SQL commands to add environment columns
        sql_commands = [
            "ALTER TABLE chat_sessions ADD COLUMN IF NOT EXISTS environment TEXT NOT NULL DEFAULT 'local';",
            "ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS environment TEXT NOT NULL DEFAULT 'local';",
            "CREATE INDEX IF NOT EXISTS idx_chat_sessions_environment ON chat_sessions(environment);",
            "CREATE INDEX IF NOT EXISTS idx_chat_messages_environment ON chat_messages(environment);"
        ]
        
        for sql in sql_commands:
            print(f"Executing: {sql}")
            client.rpc('exec_sql', {'sql': sql}).execute()
            print("✅ Success")
        
        print("\n🎉 All environment columns added successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPlease run these SQL commands manually in Supabase SQL Editor:")
        for sql in sql_commands:
            print(f"  {sql}")

if __name__ == "__main__":
    add_environment_columns()