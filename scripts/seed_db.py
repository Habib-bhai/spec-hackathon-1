"""
Database schema initialization script for Neon Postgres.

This script creates all necessary tables for the Physical AI Textbook Platform:
- users: User accounts
- user_profiles: User background and preferences
- chat_sessions: Conversation sessions
- chat_messages: Individual messages
- translation_cache: Cached translations
"""

import asyncio
import os
import sys
from typing import Optional

import asyncpg
from dotenv import load_dotenv

load_dotenv()


async def create_tables(conn: asyncpg.Connection) -> None:
    """Create all database tables."""
    
    # Users table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("✓ Created users table")
    
    # User profiles table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            programming_experience_level VARCHAR(50),
            robotics_experience_level VARCHAR(50),
            available_hardware VARCHAR(100),
            preferred_language VARCHAR(10) DEFAULT 'en',
            last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("✓ Created user_profiles table")
    
    # Chat sessions table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("✓ Created chat_sessions table")
    
    # Chat messages table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id SERIAL PRIMARY KEY,
            session_id INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            selected_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSONB
        );
    """)
    print("✓ Created chat_messages table")
    
    # Translation cache table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS translation_cache (
            id SERIAL PRIMARY KEY,
            chapter_slug VARCHAR(255) NOT NULL,
            target_language VARCHAR(10) NOT NULL,
            translated_content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(chapter_slug, target_language)
        );
    """)
    print("✓ Created translation_cache table")
    
    # Create indexes for performance
    await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_chat_messages_session 
        ON chat_messages(session_id);
    """)
    
    await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_chat_messages_created 
        ON chat_messages(created_at DESC);
    """)
    
    await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_translation_cache_lookup 
        ON translation_cache(chapter_slug, target_language);
    """)
    print("✓ Created indexes")


async def seed_data(conn: asyncpg.Connection) -> None:
    """Optionally seed initial data."""
    # Check if we already have data
    count = await conn.fetchval("SELECT COUNT(*) FROM users")
    
    if count == 0:
        print("\nSeeding initial data...")
        # Add a demo user (optional)
        await conn.execute("""
            INSERT INTO users (email) 
            VALUES ('demo@example.com')
            ON CONFLICT (email) DO NOTHING;
        """)
        print("✓ Added demo user")
    else:
        print(f"\nDatabase already has {count} user(s), skipping seed data")


async def main() -> None:
    """Main function to initialize database."""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ Error: DATABASE_URL environment variable not set")
        print("Please set it in your .env file or environment")
        sys.exit(1)
    
    print(f"Connecting to database...")
    
    try:
        conn = await asyncpg.connect(database_url)
        print("✓ Connected to database\n")
        
        print("Creating tables...")
        await create_tables(conn)
        
        await seed_data(conn)
        
        print("\n✅ Database initialization complete!")
        
    except asyncpg.PostgresError as e:
        print(f"\n❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        if conn:
            await conn.close()
            print("✓ Database connection closed")


if __name__ == "__main__":
    asyncio.run(main())
