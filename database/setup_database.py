"""
Database setup and example usage script for Supabase integration.
Run this script to create the necessary database tables and see example usage.
"""

import os
from .database_operations import ChatDatabase, save_chat_interaction, create_new_chat
from .supabase_client import get_supabase_client


def create_database_tables():
    """
    Create the necessary database tables in Supabase.
    Note: You can also create these tables directly in the Supabase dashboard.
    """
    
    # SQL commands to create tables
    chat_sessions_sql = """
    CREATE TABLE IF NOT EXISTS chat_sessions (
        id SERIAL PRIMARY KEY,
        session_id UUID UNIQUE NOT NULL,
        user_id TEXT NOT NULL DEFAULT 'anonymous',
        session_name TEXT NOT NULL,
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    chat_messages_sql = """
    CREATE TABLE IF NOT EXISTS chat_messages (
        id SERIAL PRIMARY KEY,
        message_id UUID UNIQUE NOT NULL,
        session_id UUID NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
        content TEXT NOT NULL,
        metadata JSONB DEFAULT '{}',
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
    );
    """
    
    # Create indexes for better performance
    indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_chat_sessions_updated_at ON chat_sessions(updated_at);",
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);",
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp ON chat_messages(timestamp);"
    ]
    
    try:
        client = get_supabase_client()
        
        # Execute table creation
        print("Creating chat_sessions table...")
        client.rpc('exec_sql', {'sql': chat_sessions_sql}).execute()
        
        print("Creating chat_messages table...")
        client.rpc('exec_sql', {'sql': chat_messages_sql}).execute()
        
        # Create indexes
        for index_sql in indexes_sql:
            print(f"Creating index...")
            client.rpc('exec_sql', {'sql': index_sql}).execute()
            
        print("✅ Database tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        print("\nAlternatively, you can create these tables manually in your Supabase dashboard:")
        print("\n" + "="*50)
        print("CHAT_SESSIONS TABLE SQL:")
        print("="*50)
        print(chat_sessions_sql)
        print("\n" + "="*50)
        print("CHAT_MESSAGES TABLE SQL:")
        print("="*50)
        print(chat_messages_sql)


def example_usage():
    """Demonstrate how to use the database operations."""
    
    print("\n" + "="*50)
    print("EXAMPLE USAGE")
    print("="*50)
    
    try:
        # Create a new chat session
        print("1. Creating a new chat session...")
        session_id = create_new_chat()
        print(f"   Created session: {session_id}")
        
        # Save some chat interactions
        print("\n2. Saving chat interactions...")
        user_msg1 = "שלום, מה שלומך?"
        assistant_msg1 = "שלום! אני בסדר, תודה. איך אני יכול לעזור לך היום?"
        
        user_id1, assistant_id1 = save_chat_interaction(session_id, user_msg1, assistant_msg1)
        print(f"   Saved interaction 1: {user_id1[:8]}... / {assistant_id1[:8]}...")
        
        user_msg2 = "אני צריך עזרה עם פייתון"
        assistant_msg2 = "בוודאי! אני אשמח לעזור לך עם פייתון. מה הבעיה הספציפית?"
        
        user_id2, assistant_id2 = save_chat_interaction(session_id, user_msg2, assistant_msg2)
        print(f"   Saved interaction 2: {user_id2[:8]}... / {assistant_id2[:8]}...")
        
        # Retrieve chat history
        print("\n3. Retrieving chat history...")
        db = ChatDatabase()
        history = db.get_chat_history(session_id)
        
        print(f"   Found {len(history)} messages:")
        for msg in history:
            role = msg['role']
            content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            print(f"   {role}: {content}")
        
        # Get user sessions
        print("\n4. Getting user sessions...")
        sessions = db.get_user_sessions('anonymous')
        print(f"   Found {len(sessions)} sessions for user 'anonymous'")
        
        print("\n✅ Example usage completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in example usage: {e}")


def check_environment():
    """Check if environment variables are set."""
    
    print("Checking environment variables...")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url:
        print("❌ SUPABASE_URL environment variable not set")
        return False
        
    if not supabase_key:
        print("❌ SUPABASE_KEY environment variable not set")
        return False
    
    print("✅ Environment variables are set")
    return True


if __name__ == "__main__":
    print("Supabase Database Setup and Example Usage")
    print("="*50)
    
    # Check environment
    if not check_environment():
        print("\nPlease set your Supabase environment variables:")
        print("export SUPABASE_URL='your-supabase-url'")
        print("export SUPABASE_KEY='your-supabase-anon-key'")
        exit(1)
    
    # Create tables
    create_database_tables()
    
    # Run example
    example_usage()
    
    print("\n" + "="*50)
    print("Setup complete! You can now use the database operations in your chatbot.")