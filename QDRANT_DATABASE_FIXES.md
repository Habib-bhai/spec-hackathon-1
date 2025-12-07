# Qdrant & Database Integration Fixes

**Date**: December 7, 2025  
**Issues Fixed**: 2 critical bugs preventing RAG pipeline operation  
**Files Modified**: 2

## Executive Summary

Two critical errors were blocking the RAG chatbot from functioning:

1. **Qdrant API Incompatibility**: Using deprecated `search()` method instead of `query_points()`
2. **Database Type Mismatch**: Passing Python dict to JSONB column instead of JSON string

Both issues have been resolved using the latest Qdrant documentation from Context7 MCP server.

---

## Issue 1: AsyncQdrantClient API Method Error

### Error Message
```
AttributeError: 'AsyncQdrantClient' object has no attribute 'search'
```

### Root Cause
The code was using the **old synchronous API** method `client.search()` with `AsyncQdrantClient`. According to the latest Qdrant Python client documentation (fetched via Context7 MCP), the async client uses a different API:

- **Old API (sync)**: `client.search(collection_name, query_vector, limit, query_filter)`
- **New API (async)**: `client.query_points(collection_name, query, limit, query_filter).points`

### File: `api/services/vector_service.py`

**Before (Line 180-186):**
```python
try:
    results = await self.client.search(
        collection_name=self.collection_name,
        query_vector=query_vector,
        limit=limit,
        query_filter=query_filter,
    )
```

**After (Fixed):**
```python
try:
    # Use query_points for AsyncQdrantClient (new API)
    response = await self.client.query_points(
        collection_name=self.collection_name,
        query=query_vector,  # Note: parameter name changed from query_vector to query
        limit=limit,
        query_filter=query_filter,
    )
    results = response.points  # Extract points from response object
```

### Key Changes
1. Changed method from `search()` → `query_points()`
2. Changed parameter from `query_vector=` → `query=`
3. Added `.points` to extract results from response object
4. Split into two lines for clarity (response → results)

### Documentation Source
Context7 MCP server: `/qdrant/qdrant-client`

Example from official docs:
```python
res = await client.query_points(
    collection_name="my_collection",
    query=np.random.rand(10).tolist(),
    limit=10,
)
```

---

## Issue 2: Database JSONB Type Mismatch

### Error Message
```
asyncpg.exceptions.DataError: invalid input for query argument $4: 
{'sources': []} (expected str, got dict)
```

### Root Cause
The `chat_messages.metadata` column is defined as `JSONB` in Postgres. **asyncpg requires JSONB values to be passed as JSON strings**, not Python dictionaries.

From `scripts/seed_db.py` (line 64):
```sql
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    selected_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB  -- ← This column expects JSON STRING, not dict
);
```

### File: `api/routers/chat.py`

**Before (Line 104-115):**
```python
# Save assistant response
async with get_connection() as conn:
    await conn.execute(
        """
        INSERT INTO chat_messages (session_id, role, content, metadata)
        VALUES ($1, $2, $3, $4)
        """,
        session_id,
        "assistant",
        answer,
        {"sources": [s['chapter_slug'] for s in sources]},  # ❌ Dict passed directly
    )
```

**After (Fixed):**
```python
# Save assistant response with metadata as JSON string
metadata = json.dumps({"sources": [s['chapter_slug'] for s in sources]})  # ✅ Convert to JSON string
async with get_connection() as conn:
    await conn.execute(
        """
        INSERT INTO chat_messages (session_id, role, content, metadata)
        VALUES ($1, $2, $3, $4)
        """,
        session_id,
        "assistant",
        answer,
        metadata,  # ✅ Now a JSON string
    )
```

**Import Added (Line 8):**
```python
import json  # Added to convert dict to JSON string
```

### Key Changes
1. Added `import json` at top of file
2. Created `metadata` variable with `json.dumps()` to serialize dict → JSON string
3. Passed JSON string to database instead of dict
4. Updated comment to clarify the conversion

### asyncpg Behavior
- **JSONB columns** in asyncpg expect JSON-encoded strings
- **asyncpg automatically deserializes** JSON strings when reading from JSONB columns
- **Insert**: Pass `json.dumps(dict)` → Postgres stores as JSONB
- **Select**: asyncpg returns dict automatically (no `json.loads()` needed)

---

## Testing the Fixes

### Prerequisites
1. API server running: `cd api && uvicorn api.main:app --reload`
2. Environment variables configured (GEMINI_API_KEY, QDRANT_URL, DATABASE_URL)
3. Content indexed: `python scripts/index_content.py`
4. Database seeded: `python scripts/seed_db.py`

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

### Test 2: Basic Chat (No Session)
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is ROS 2?"
  }'
```

**Expected Response:**
```json
{
  "response": "ROS 2 (Robot Operating System 2) is...",
  "session_id": 1,
  "sources": ["module-1-ros2/week-01-intro"]
}
```

### Test 3: Chat with Context
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain this in simpler terms",
    "session_id": 1,
    "selected_text": "Nodes communicate via topics using a publisher-subscriber pattern",
    "chapter_slug": "module-1-ros2/week-02-nodes-topics"
  }'
```

**Expected Response:**
```json
{
  "response": "In simple terms, nodes are like...",
  "session_id": 1,
  "sources": ["module-1-ros2/week-02-nodes-topics"]
}
```

### Test 4: Verify Database Storage
```bash
# Connect to Neon Postgres
psql $DATABASE_URL

# Check chat messages were saved correctly
SELECT id, role, content, metadata FROM chat_messages ORDER BY created_at DESC LIMIT 5;
```

**Expected Output:**
```
 id | role      | content                  | metadata
----+-----------+--------------------------+----------------------------------
  2 | assistant | In simple terms, nodes...| {"sources": ["module-1-ros2/..."]}
  1 | user      | Explain this in...       | null
```

### Test 5: Verify Qdrant Search
Check API logs for successful search:
```
INFO - Found 5 results for search query
INFO - RAG pipeline complete: answer=150 chars, sources=2
```

---

## What Was Fixed

| Issue | File | Lines | Change | Impact |
|-------|------|-------|--------|--------|
| Qdrant API method | `api/services/vector_service.py` | 180-187 | `search()` → `query_points()` | Vector search now works with AsyncQdrantClient |
| JSONB type mismatch | `api/routers/chat.py` | 8, 104-115 | Added `json.dumps()` for metadata | Database inserts succeed without type errors |

---

## Documentation References

### Qdrant Python Client (via Context7 MCP)
- **Library ID**: `/qdrant/qdrant-client`
- **Trust Score**: 9.8/10
- **Code Snippets**: 43 examples

**Key Examples Used:**

1. **Async Search Pattern**:
```python
res = await client.search(
   collection_name="my_collection",
   query_vector=np.random.rand(10).tolist(),
   limit=10,
)
```

2. **Async Query Points Pattern** (NEW API):
```python
res = await client.query_points(
    collection_name="my_collection",
    query=np.random.rand(10).tolist(),
    limit=10,
)
print(res)
```

**Note**: The documentation shows BOTH methods exist, but for `AsyncQdrantClient` specifically, the **`query_points()` method is the correct async API**.

### asyncpg JSONB Handling
- **Official Docs**: https://magicstack.github.io/asyncpg/current/usage.html#type-conversion
- **Key Rule**: JSONB columns require JSON strings on insert, return dicts on select
- **Example**:
  ```python
  # Insert
  await conn.execute("INSERT INTO table (jsonb_col) VALUES ($1)", json.dumps({"key": "value"}))
  
  # Select (automatically deserializes)
  row = await conn.fetchrow("SELECT jsonb_col FROM table")
  print(row['jsonb_col'])  # Already a dict, no json.loads() needed
  ```

---

## Next Steps

1. **Test the chatbot** via frontend:
   - Open http://localhost:3000
   - Click chat widget (💬 icon)
   - Ask: "What is ROS 2?"
   - Verify response appears within 5 seconds

2. **Monitor logs** for errors:
   ```bash
   # Terminal with API server
   # Should see:
   # - "Found X results for search query"
   # - "RAG pipeline complete"
   # - No AttributeError or DataError
   ```

3. **Check database** for saved messages:
   ```bash
   psql $DATABASE_URL -c "SELECT COUNT(*) FROM chat_messages;"
   ```

4. **Performance testing**:
   - Send 5-10 concurrent requests
   - Verify no blocking (all should complete in <10s total)

---

## Troubleshooting

### If Qdrant search still fails:

1. **Check Qdrant client version**:
   ```bash
   pip show qdrant-client
   # Should be >= 1.7.0 for query_points support
   ```

2. **Verify collection exists**:
   ```python
   # In Python REPL
   from api.services.vector_service import VectorService
   import asyncio
   
   async def check():
       vs = VectorService()
       await vs.connect()
       exists = await vs.client.collection_exists("physical_ai_textbook")
       print(f"Collection exists: {exists}")
   
   asyncio.run(check())
   ```

3. **Re-index content** if collection is empty:
   ```bash
   python scripts/index_content.py
   ```

### If database insert still fails:

1. **Check column type**:
   ```sql
   \d chat_messages
   -- Verify metadata column is JSONB
   ```

2. **Test JSON encoding**:
   ```python
   import json
   metadata = {"sources": ["test"]}
   json_str = json.dumps(metadata)
   print(type(json_str))  # Should be <class 'str'>
   ```

3. **Check asyncpg version**:
   ```bash
   pip show asyncpg
   # Should be >= 0.29.0
   ```

---

## Summary

Both bugs were **API incompatibility issues**:

1. **Qdrant**: Using sync API with async client → Fixed by switching to `query_points()`
2. **asyncpg**: Passing dict to JSONB → Fixed by converting to JSON string with `json.dumps()`

The RAG pipeline should now work end-to-end:
- User sends message
- Vector search retrieves relevant chunks via Qdrant
- Gemini generates contextual response
- Message + metadata saved to Postgres
- Response returned to frontend

**Status**: ✅ All fixes applied and ready for testing
