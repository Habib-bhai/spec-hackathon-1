---
id: 001
title: Initial Constitution Creation for Physical AI Textbook
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-20250514
feature: none
branch: main
user: developer
command: /sp.constitution
labels: ["constitution", "project-setup", "context7", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-initial-constitution-creation.constitution.prompt.md
tests:
  - null
---

## Prompt

Follow instructions in sp.constitution.prompt.md.

# Physical AI & Humanoid Robotics Textbook Platform

## Project Vision
Build an AI-native, interactive textbook platform for teaching Physical AI & Humanoid Robotics, featuring a RAG-powered chatbot, user authentication, content personalization, and Urdu translation—all driven by Spec-Kit Plus and Claude Code.

## Core Technologies (MUST use Context7 MCP for documentation lookup)
- **Frontend/Book:** Docusaurus 3.x
- **Deployment:** GitHub Pages
- **Backend API:** FastAPI (Python)
- **Database:** Neon Serverless Postgres
- **Vector Store:** Qdrant Cloud
- **AI/RAG:** OpenAI Agents SDK, ChatKit SDK
- **Authentication:** Better-Auth
- **Development:** TypeScript, Python

## Functional Requirements

### 1. Book Platform (Base)
- Docusaurus-powered static site with 4 modules (13 weeks of content i.e. chapters in each modules)
- Module 1: ROS 2 (Robotic Nervous System)
- Module 2: Gazebo & Unity (Digital Twin)
- Module 3: NVIDIA Isaac (AI-Robot Brain)
- Module 4: VLA & Conversational Robotics
- Deploy to GitHub Pages with CI/CD

### 2. RAG Chatbot (Base)
- Embed chatbot widget in book pages
- Answer questions about book content using RAG
- Support "selected text" context: user highlights text → asks question about it
- Backend: FastAPI + Qdrant (embeddings) + Neon (chat history, user data)
- Use OpenAI Agents SDK or ChatKit SDK

### 3. Authentication (Bonus +50)
- Signup/Signin with Better-Auth
- Onboarding survey: capture user's software/hardware background
- Store profile in Neon Postgres

### 4. Content Personalization (Bonus +50)
- "Personalize" button at start of each chapter
- Use user background to tailor explanations (beginner vs advanced)
- LLM-powered content adaptation

### 5. Urdu Translation (Bonus +50)
- "Translate to Urdu" button at chapter start
- LLM-powered translation of chapter content
- Preserve formatting and code blocks

### 6. Reusable Intelligence (Bonus +50)
- Create Claude Code subagents for:
  - Documentation lookup (using Context7 MCP)
  - Code generation for ROS 2, FastAPI, Docusaurus
  - Content writing with technical accuracy
- Define Agent Skills for recurring tasks

## Non-Functional Requirements

### Performance
- Book pages load in < 2s
- Chatbot responds in < 5s for standard queries
- Personalization/translation completes in < 10s

### Security
- No hardcoded secrets; use `.env` files
- Better-Auth handles session management
- API endpoints require authentication where appropriate

### Scalability
- Neon serverless scales automatically
- Qdrant Cloud free tier limits: plan for ~1M vectors

### Documentation
- All architectural decisions documented as ADRs
- PHRs created for every significant prompt/response

## Development Principles

### Context7 MCP Integration (MANDATORY)
Before implementing ANY feature, the agent MUST:
1. Call `mcp_context7_resolve-library-id` to find the library ID
2. Call `mcp_context7_get-library-docs` to fetch current documentation
3. Use retrieved docs as authoritative source for implementation
4. TDD (test driven development) first

Required Context7 lookups:
- Docusaurus (routing, plugins, MDX, deployment)
- FastAPI (routes, dependencies, middleware)
- Qdrant (vector operations, collections, search)
- Better-Auth (setup, providers, sessions)
- OpenAI SDK (agents, chat completions, embeddings)
- Neon Postgres (connection, queries, serverless)

### Spec-Driven Development
- Every feature starts with a spec in `specs/<feature>/spec.md`
- Architecture in `specs/<feature>/plan.md`
- Testable tasks in `specs/<feature>/tasks.md`
- Red-Green-Refactor cycle for implementation

### Code Quality
- TypeScript for frontend (strict mode)
- Python with type hints for backend
- ESLint + Prettier for JS/TS
- Ruff for Python linting
- All code must pass linting before commit

### Testing
- Unit tests for API endpoints (pytest)
- Integration tests for RAG pipeline
- E2E tests for critical user flows (optional)

## Response snapshot

Created the initial constitution for the Physical AI & Humanoid Robotics Textbook Platform at `.specify/memory/constitution.md`.

**Constitution v1.0.0** includes 8 core principles:
1. **Context7 MCP-First** - Mandatory documentation lookups before implementation
2. **Spec-Driven Development** - Feature workflow via specs, plans, tasks
3. **Test-First (TDD)** - Red-Green-Refactor cycle mandatory
4. **Documentation-First** - ADRs and PHRs required
5. **Security & Secrets Management** - No hardcoded secrets, Better-Auth
6. **Performance Standards** - Quantified budgets (<2s pages, <5s chatbot)
7. **Code Quality** - TypeScript strict, Python type hints, linting
8. **Observability & Traceability** - Structured logging, PHR history

Additional sections: Technology Stack, Development Workflow, Governance

Templates verified for consistency:
- plan-template.md ✅
- spec-template.md ✅
- tasks-template.md ✅

## Outcome

- ✅ Impact: Created foundational constitution for entire project
- 🧪 Tests: N/A (governance document)
- 📁 Files: `.specify/memory/constitution.md` created with 8 principles
- 🔁 Next prompts: `/sp.spec` for first feature (likely book-platform or rag-chatbot)
- 🧠 Reflection: Constitution establishes Context7 MCP as mandatory for all external dependencies, ensuring implementations stay current with latest APIs

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test Context7 integration with first feature spec
