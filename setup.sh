#!/bin/bash
# Quick Setup Script for Physical AI Textbook Platform
# This script helps you set up the environment step by step

echo "🚀 Physical AI Textbook Platform - Quick Setup"
echo "=============================================="
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "✅ Found .env file"
else
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: You need to fill in your API credentials in .env"
    echo ""
    echo "Required credentials:"
    echo "  1. DATABASE_URL - Get from https://neon.tech (use POOLED connection)"
    echo "  2. QDRANT_URL and QDRANT_API_KEY - Get from https://cloud.qdrant.io"
    echo "  3. GEMINI_API_KEY - Get from https://makersuite.google.com/app/apikey"
    echo ""
    echo "After adding credentials, run this script again."
    exit 1
fi

# Check if environment variables are set
source .env 2>/dev/null || true

if [ -z "$DATABASE_URL" ] || [ "$DATABASE_URL" = "postgresql://user:password@host.neon.tech/dbname?sslmode=require" ]; then
    echo "❌ DATABASE_URL not configured in .env"
    echo "Please edit .env and add your Neon Postgres connection string"
    exit 1
fi

if [ -z "$QDRANT_API_KEY" ] || [ "$QDRANT_API_KEY" = "your-qdrant-api-key-here" ]; then
    echo "❌ QDRANT credentials not configured in .env"
    echo "Please edit .env and add your Qdrant Cloud credentials"
    exit 1
fi

if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your-gemini-api-key-here" ]; then
    echo "❌ GEMINI_API_KEY not configured in .env"
    echo "Please edit .env and add your Google Gemini API key"
    exit 1
fi

echo "✅ Environment variables configured"
echo ""

# Check Python dependencies
echo "📦 Checking Python dependencies..."
if python -c "import fastapi, asyncpg, qdrant_client, google.generativeai" 2>/dev/null; then
    echo "✅ Python dependencies installed"
else
    echo "📥 Installing Python dependencies..."
    pip install -r api/requirements.txt
fi
echo ""

# Check Node dependencies
echo "📦 Checking Node.js dependencies..."
if [ -d "book/node_modules" ]; then
    echo "✅ Node.js dependencies installed"
else
    echo "📥 Installing Node.js dependencies (this may take 5-10 minutes)..."
    cd book && npm install && cd ..
fi
echo ""

# Initialize database
echo "🗄️  Initializing database..."
python scripts/seed_db.py
if [ $? -eq 0 ]; then
    echo "✅ Database initialized"
else
    echo "❌ Database initialization failed"
    echo "Check your DATABASE_URL and try again"
    exit 1
fi
echo ""

# Index content
echo "📚 Indexing textbook content..."
python scripts/index_content.py
if [ $? -eq 0 ]; then
    echo "✅ Content indexed"
else
    echo "❌ Content indexing failed"
    echo "Check your QDRANT and GEMINI credentials and try again"
    exit 1
fi
echo ""

echo "=============================================="
echo "✅ Setup complete! Ready to start the servers"
echo "=============================================="
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (API):"
echo "  python -m uvicorn api.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd book && npm start"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
