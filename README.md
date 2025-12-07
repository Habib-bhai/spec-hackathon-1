# Physical AI Textbook Platform - MVP Complete! 🎉

A modern, interactive textbook platform for learning robotics and Physical AI, featuring:
- 📚 **Docusaurus-based textbook** with 4 modules and 13 chapters
- 🤖 **RAG-powered chatbot** using Gemini AI and Qdrant vector database
- 💬 **Interactive features** including text selection context and conversation history

## 🏗️ Architecture

### Frontend (`book/`)
- **Framework**: Docusaurus 3.1.0 + React 18 + TypeScript
- **Features**: 
  - Responsive textbook layout
  - Custom landing page
  - Integrated chat widget
- **Build**: Static site generation for GitHub Pages

### Backend (`api/`)
- **Framework**: FastAPI + Python 3.12
- **AI**: Google Gemini (text-embedding-004 + gemini-1.5-flash) - **Free tier**
- **Vector DB**: Qdrant Cloud for semantic search
- **Database**: Neon Postgres (serverless) for chat history
- **Features**: RAG chatbot, chat history, content search

## 🚀 Quick Start

### Prerequisites

1. **Python 3.12+** and **Node.js 20+**
2. **Accounts** (all have free tiers):
   - [Neon](https://neon.tech) - Serverless Postgres
   - [Qdrant Cloud](https://cloud.qdrant.io) - Vector database
   - [Google AI Studio](https://makersuite.google.com/app/apikey) - Gemini API

### Setup Steps

#### 1. Clone and Install Dependencies

```bash
# Install frontend dependencies
cd book
npm install
cd ..

# Install backend dependencies
cd api
pip install -e .
# or: pip install -r requirements.txt (if you create one)
cd ..
```

#### 2. Configure Environment Variables

```bash
# Copy the example
cp .env.example .env

# Edit .env and fill in your credentials:
# - DATABASE_URL from Neon (use the pooled connection string)
# - QDRANT_URL and QDRANT_API_KEY from Qdrant Cloud
# - GEMINI_API_KEY from Google AI Studio
```

#### 3. Initialize Database

```bash
python scripts/seed_db.py
```

This creates the required tables in your Neon database.

#### 4. Index Textbook Content

```bash
python scripts/index_content.py
```

This:
- Parses all MDX files
- Generates embeddings
- Populates Qdrant vector database

**Expected output**: ~50-80 chunks from 14 files (intro + 13 chapters)

#### 5. Start the API Server

```bash
cd api
python -m uvicorn main:app --reload
```

API will be available at `http://localhost:8000`
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

#### 6. Start the Frontend

```bash
cd book
npm start
```

Site will be available at `http://localhost:3000`

## 🧪 Testing the MVP

### Test User Story 1: Navigation

1. Open http://localhost:3000
2. Click "Start Learning" button
3. Navigate through modules in the sidebar
4. Verify all 13 chapters load correctly

**Success criteria**: ✅ All chapters accessible, no 404 errors

### Test User Story 2: RAG Chatbot

1. Open any chapter (e.g., "Week 1: Introduction to ROS 2")
2. Click the chat bubble (💬) in bottom-right
3. Ask: "What is ROS 2?"
4. Verify you get a response with:
   - ✅ Grounded answer from textbook content
   - ✅ Source citations showing the chapter
   - ✅ Response time < 5 seconds

**Advanced tests**:
- Select text in the chapter → chat icon shows selection
- Ask about the selected text
- Continue conversation (history is maintained)

## 📊 Project Status

### ✅ Completed (47/51 MVP tasks)

**Phase 1**: Setup & Configuration (10/10)
**Phase 2**: Foundation (14/14)
**Phase 3**: User Story 1 - Navigation (7/8)
- ⏳ Pending: GitHub Pages deployment (requires repo setup)

**Phase 4**: User Story 2 - RAG Chatbot (16/16)
- ✅ Content indexing pipeline
- ✅ RAG service with Gemini + Qdrant
- ✅ Chat API with history
- ✅ React chat widget

### 📝 Key Files Created

**Configuration** (9 files)
- `.gitignore`, `.env.example`, `docker-compose.yml`
- `book/package.json`, `book/tsconfig.json`, `book/docusaurus.config.js`
- `api/pyproject.toml`, `api/config.py`

**Backend API** (16 files)
- `api/main.py` - FastAPI app
- `api/db/connection.py` - Database pool
- `api/models/chat.py`, `api/models/user.py` - Pydantic models
- `api/services/vector_service.py` - Qdrant wrapper
- `api/services/gemini_service.py` - Gemini AI client
- `api/services/rag_service.py` - RAG pipeline
- `api/routers/chat.py` - Chat endpoints

**Scripts** (2 files)
- `scripts/seed_db.py` - Database initialization
- `scripts/index_content.py` - Content indexing

**Frontend** (21 files)
- `book/docs/intro.mdx` - Introduction
- `book/docs/module-*/` - 4 modules, 13 chapters
- `book/src/pages/index.tsx` - Landing page
- `book/src/components/ChatWidget/` - Chat widget component
- `book/src/theme/Root.tsx` - Docusaurus integration

**CI/CD** (2 files)
- `.github/workflows/deploy-book.yml` - GitHub Pages deployment
- `.github/workflows/test-api.yml` - API testing

## 🎯 Next Steps (Optional)

### For Production Deployment

1. **Deploy Frontend**:
   ```bash
   cd book
   npm run build
   # Deploy to GitHub Pages, Vercel, or Netlify
   ```

2. **Deploy Backend**:
   - Railway, Render, or Fly.io
   - Update `REACT_APP_API_URL` in `.env`

3. **Set up CORS**:
   - Update `CORS_ORIGINS` in `.env` with your production URL

### Enhancements (Beyond MVP)

- [ ] User authentication (Better-Auth integration prepared in T000-F)
- [ ] User profiles with experience levels (models ready in `api/models/user.py`)
- [ ] Content translation (schema ready in `translation_cache` table)
- [ ] More chapters and modules
- [ ] Code execution environments
- [ ] Progress tracking
- [ ] Quizzes and exercises

## 🐛 Troubleshooting

### API won't start

**Error**: `DATABASE_URL not set`
- **Fix**: Check your `.env` file has all required variables

**Error**: `qdrant_client` import error
- **Fix**: `pip install qdrant-client google-generativeai`

### Chat widget not loading

**Error**: Chat button visible but no response
- **Fix**: Check API is running at `http://localhost:8000`
- **Fix**: Check browser console for CORS errors
- **Fix**: Verify `REACT_APP_API_URL` in `.env`

### Indexing fails

**Error**: `No MDX files found`
- **Fix**: Run from project root, not `scripts/` directory

**Error**: Gemini API rate limit
- **Fix**: Wait 1 minute, script auto-retries
- **Fix**: Free tier has 1500 requests/day limit

### Chat gives empty responses

**Error**: "I couldn't find relevant information"
- **Fix**: Run `python scripts/index_content.py` first
- **Fix**: Check Qdrant collection has data via Qdrant Cloud UI

## 📖 Documentation

- **API Docs**: http://localhost:8000/docs (when running)
- **Scripts README**: `scripts/README.md`
- **Tasks Tracking**: `specs/001-physical-ai-textbook-platform/tasks.md`
- **Architecture**: `specs/001-physical-ai-textbook-platform/plan.md`

## 🤝 Contributing

See `.specify/memory/constitution.md` for development principles and coding standards.

## 📄 License

MIT License - Feel free to use for your own projects!

---

**Built with**: Docusaurus • FastAPI • Google Gemini • Qdrant • Neon Postgres • React • TypeScript • Python
