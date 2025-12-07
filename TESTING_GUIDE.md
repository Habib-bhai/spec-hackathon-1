# Local Testing Guide

This guide walks you through testing the Physical AI Textbook MVP on your local machine.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.12+ installed (`python --version`)
- [ ] Node.js 20+ installed (`node --version`)
- [ ] Git installed
- [ ] Text editor (VS Code recommended)

## Step 1: Get API Credentials (15 minutes)

### A. Neon Postgres Database

1. Go to https://neon.tech
2. Sign up (free tier available)
3. Create a new project
4. **Important**: Use the **pooled connection string**
   - In your Neon dashboard, look for "Connection String"
   - Select "Pooled connection" option
   - The URL should end with `-pooler.neon.tech`
5. Copy the connection string (looks like):
   ```
   postgresql://user:pass@ep-xxx-pooler.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```

### B. Qdrant Vector Database

1. Go to https://cloud.qdrant.io
2. Sign up (free tier: 1GB storage)
3. Create a cluster
   - Choose free tier
   - Select region closest to you
4. Get credentials:
   - **API Key**: In cluster settings
   - **URL**: Something like `https://xxx-yyy.aws.cloud.qdrant.io:6333`

### C. Google Gemini API

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)
5. **Note**: Free tier includes:
   - 15 requests per minute
   - 1500 requests per day
   - More than enough for MVP testing

## Step 2: Setup Environment (5 minutes)

```bash
# 1. Navigate to project
cd d:/spec-hackathon-1

# 2. Copy environment template
cp .env.example .env

# 3. Open .env in your editor
code .env  # or: notepad .env

# 4. Fill in the following (paste your actual values):
DATABASE_URL="postgresql://..."  # From Neon
QDRANT_URL="https://..."         # From Qdrant
QDRANT_API_KEY="..."             # From Qdrant
GEMINI_API_KEY="AIza..."         # From Google

# 5. Save the file
```

## Step 3: Install Dependencies (5-10 minutes)

### Frontend (Docusaurus)

```bash
cd book
npm install
cd ..
```

Expected output: `added 1427 packages` (may take 5-10 minutes)

### Backend (FastAPI)

```bash
cd api
pip install -r requirements.txt
cd ..
```

Expected output: Successfully installed ~15 packages

## Step 4: Initialize Database (30 seconds)

```bash
python scripts/seed_db.py
```

**Expected output:**
```
Connecting to database...
✓ Connected to database

Creating tables...
✓ Created users table
✓ Created user_profiles table
✓ Created chat_sessions table
✓ Created chat_messages table
✓ Created translation_cache table
✓ Created indexes

✅ Database initialization complete!
✓ Database connection closed
```

**If you see errors:**
- Check `DATABASE_URL` is correct
- Ensure connection string ends with `-pooler.neon.tech`
- Verify `sslmode=require` is in the URL

## Step 5: Index Content (2-3 minutes)

```bash
python scripts/index_content.py
```

**Expected output:**
```
🚀 Starting content indexing for Physical AI Textbook

🔧 Initializing services...
📊 Setting up Qdrant collection...
✅ Collection ready

📚 Found 14 MDX files

[1/14] 📄 Processing: book/docs/intro.mdx
  📌 Slug: intro
  📦 Module: intro
  ✂️  Created 3 chunks
  🧠 Generating embeddings...
  💾 Upserting to Qdrant...
  ✅ Indexed 3 chunks

... (continues for all files) ...

============================================================
✨ Indexing complete!
📊 Total files processed: 14
📦 Total chunks indexed: 52
🎯 Average chunks per file: 3.7
============================================================
```

**If you see errors:**
- Check `QDRANT_URL` and `QDRANT_API_KEY`
- Verify Qdrant cluster is running
- Check `GEMINI_API_KEY` is valid
- Wait 1 minute if rate limited, then retry

## Step 6: Start API Server (Terminal 1)

**Important**: Run from the project root directory (not inside `api/`):

```bash
# Make sure you're in the project root
cd d:/spec-hackathon-1

# Start the API server
python -m uvicorn api.main:app --reload
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['D:\\spec-hackathon-1']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Starting up Physical AI Textbook API...
INFO:     ✓ Database pool initialized
INFO:     ✓ Vector service initialized
INFO:     ✓ Qdrant collection verified
INFO:     🚀 Application startup complete
INFO:     Application startup complete.
```

**Keep this terminal running!**

**Note**: The command is `api.main:app` (with dot), not `main:app`. This is because we use absolute imports.

### Quick API Test

Open in browser: http://localhost:8000/health

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "vector_store": "connected"
  }
}
```

### API Documentation

Open: http://localhost:8000/docs

You should see Swagger UI with endpoints:
- `POST /api/chat` - Chat endpoint
- `GET /api/chat/sessions/{id}` - Get history
- `POST /api/chat/search` - Search content

## Step 7: Start Frontend (Terminal 2 - New Terminal)

```bash
cd book
npm start
```

**Expected output:**
```
Starting the development server...
Docusaurus website is running at: http://localhost:3000/

✔ Client
  Compiled successfully in X.XXs
```

Browser should auto-open to http://localhost:3000

**Keep this terminal running!**

## Step 8: Test User Story 1 - Navigation ✅

### Test: Landing Page

1. You should see: "Physical AI Textbook"
2. Three feature cards: 🤖 ROS 2, 🎮 Simulation, 🧠 AI Integration
3. Four module cards with "Start Module X →" links

### Test: Chapter Navigation

1. Click "Start Learning" button
2. Sidebar shows:
   - Introduction
   - Module 1: Introduction to ROS 2 (5 chapters)
   - Module 2: Robot Simulation (2 chapters)
   - Module 3: NVIDIA Isaac (3 chapters)
   - Module 4: VLA Models (3 chapters)
3. Click "Week 1: Introduction to ROS 2"
4. Page should load with content about ROS 2

✅ **Success criteria**: All pages load, no 404 errors

## Step 9: Test User Story 2 - RAG Chatbot ✅

### Test: Basic Chat

1. **Open any chapter** (e.g., "Week 1: Introduction to ROS 2")
2. **Look for chat button** (💬) in bottom-right corner
3. **Click the button** - Chat window should slide up
4. **Type**: "What is ROS 2?"
5. **Press Enter** or click send button (➤)

**Expected behavior:**
- Loading indicator appears (3 dots bouncing)
- Response appears within 5 seconds
- Answer mentions "Robot Operating System"
- Sources section shows: "module-1-ros2/week-01-intro"

### Test: Text Selection Context

1. **Select text** on the page (highlight any paragraph)
2. **Click chat button**
3. **Notice** the selected text appears at the top
4. **Ask**: "Explain this in simpler terms"
5. **Expected**: Response references your selected text

### Test: Conversation History

1. Ask: "What is ROS 2?"
2. Follow up: "What are nodes in ROS 2?"
3. Follow up: "How do nodes communicate?"
4. **Expected**: Answers build on previous context

### Test: Clear Chat

1. Click trash icon (🗑️) in header
2. **Expected**: Messages clear, new session starts

✅ **Success criteria**: 
- Responses are relevant and grounded
- Source citations are shown
- Conversation flows naturally
- Response time < 5 seconds

## Step 10: Test Search Endpoint (Optional)

Open: http://localhost:8000/docs

1. Expand `POST /api/chat/search`
2. Click "Try it out"
3. Set body:
   ```json
   {
     "query": "inverse kinematics",
     "limit": 5
   }
   ```
4. Click "Execute"
5. **Expected**: JSON response with matching chunks

## Troubleshooting

### Chat widget not visible

**Check:**
1. API server running? (Terminal 1)
2. Frontend server running? (Terminal 2)
3. Browser console for errors? (F12)

**Fix:**
- Restart frontend: Ctrl+C in Terminal 2, then `npm start`

### Chat gives empty response

**Check:**
1. Did you run `python scripts/index_content.py`?
2. Qdrant has data? (Check Qdrant Cloud dashboard)

**Fix:**
- Re-run indexing: `python scripts/index_content.py --force-recreate`

### API won't start

**Error**: "DATABASE_URL environment variable is not set"

**Fix:**
- Check `.env` file exists
- Verify `.env` has `DATABASE_URL=...`
- Try: `export $(cat .env | xargs)` (Linux/Mac)

### CORS errors in browser console

**Error**: "Access to fetch at 'http://localhost:8000' ... has been blocked by CORS"

**Fix:**
- Check `CORS_ORIGINS` in `.env` includes `http://localhost:3000`
- Restart API server

### Gemini rate limit error

**Error**: "429 Resource has been exhausted"

**Fix:**
- Wait 1 minute
- Free tier: 15 requests/minute, 1500/day
- For indexing, this should be fine

## Performance Benchmarks

Expected performance on decent hardware:

| Operation | Time | Notes |
|-----------|------|-------|
| npm install | 5-10 min | First time only |
| pip install | 1-2 min | First time only |
| Database init | <30 sec | One-time setup |
| Content indexing | 2-3 min | 14 files, ~52 chunks |
| API startup | <5 sec | Includes Qdrant connection |
| Frontend build | 30-60 sec | Production build |
| Frontend dev start | 10-20 sec | Watch mode |
| Chat response | 2-5 sec | Includes vector search + LLM |

## Next Steps

✅ **All tests passed?** Congratulations! Your MVP is working.

**What to do next:**

1. **Add more content**: Create new MDX files in `book/docs/`
2. **Customize styling**: Edit `book/src/css/custom.css`
3. **Deploy**: See `README.md` for deployment guide
4. **Extend features**: See `IMPLEMENTATION_SUMMARY.md` for ideas

## Getting Help

**Check these first:**
- `README.md` - Quick start and deployment
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `scripts/README.md` - Script documentation
- `specs/001-physical-ai-textbook-platform/tasks.md` - Implementation checklist

**Still stuck?**
- Check API docs: http://localhost:8000/docs
- Review error logs in terminals
- Verify all environment variables in `.env`

---

**Happy testing! 🎉**
