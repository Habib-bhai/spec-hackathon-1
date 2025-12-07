# Scripts

Utility scripts for the Physical AI Textbook Platform.

## Available Scripts

### `seed_db.py`

Initialize the Neon Postgres database with the required schema.

**Tables created:**
- `users` - User accounts
- `user_profiles` - User experience levels and preferences
- `chat_sessions` - Conversation sessions
- `chat_messages` - Individual chat messages
- `translation_cache` - Cached translations

**Usage:**
```bash
# Make sure DATABASE_URL is set in .env
python scripts/seed_db.py
```

**Prerequisites:**
- Neon Postgres database created
- `DATABASE_URL` environment variable set
- `asyncpg` package installed

### `index_content.py`

Index textbook content for RAG chatbot functionality.

**What it does:**
1. Parses all MDX files in `book/docs/`
2. Extracts plain text (strips MDX/JSX syntax)
3. Chunks content into semantic pieces (~500 words)
4. Generates embeddings using Gemini `text-embedding-004`
5. Upserts chunks to Qdrant vector database

**Usage:**
```bash
# Index all content
python scripts/index_content.py

# Force recreate collection (deletes all existing data)
python scripts/index_content.py --force-recreate

# Custom docs directory
python scripts/index_content.py --docs-dir /path/to/docs
```

**Prerequisites:**
- Qdrant cluster created (Cloud or local)
- `QDRANT_URL` and `QDRANT_API_KEY` environment variables set
- `GEMINI_API_KEY` environment variable set
- All dependencies installed (`qdrant-client`, `google-generativeai`)

**Output:**
- Prints progress for each file
- Shows total files, chunks, and average chunks per file
- Creates/updates Qdrant collection `physical_ai_textbook`

**Rate Limits:**
- Adds 1-second delay between files to avoid Gemini API rate limits
- Free tier: 1500 requests/day (should handle ~100 chapters)

## Development

To add a new script:

1. Create the script file in `scripts/`
2. Add shebang and docstring
3. Import from parent directory: `sys.path.insert(0, str(Path(__file__).parent.parent))`
4. Add to this README with usage instructions
5. Make it executable: `chmod +x scripts/your_script.py`

## Environment Variables

All scripts use environment variables from `.env` file. See `.env.example` for required variables.
