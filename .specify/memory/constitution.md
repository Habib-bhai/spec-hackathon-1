<!--
  ========================================
  SYNC IMPACT REPORT
  ========================================
  Version change: 0.0.0 → 1.0.0 (Initial constitution)
  
  Added Principles:
  - I. Context7 MCP-First (Authoritative Documentation)
  - II. Spec-Driven Development
  - III. Test-First (TDD - NON-NEGOTIABLE)
  - IV. Documentation-First
  - V. Security & Secrets Management
  - VI. Performance Standards
  - VII. Code Quality
  - VIII. Observability & Traceability
  
  Added Sections:
  - Technology Stack
  - Development Workflow
  - Governance
  
  Templates Status:
  ✅ plan-template.md - Constitution Check section aligned
  ✅ spec-template.md - User scenarios align with TDD principle
  ✅ tasks-template.md - Phase structure supports Red-Green-Refactor
  
  Deferred Items: None
  ========================================
-->

# Physical AI & Humanoid Robotics Textbook Platform Constitution

## Project Vision

Build an AI-native, interactive textbook platform for teaching Physical AI & Humanoid Robotics, featuring a RAG-powered chatbot, user authentication, content personalization, and Urdu translation—all driven by Spec-Kit Plus and Context7 MCP for authoritative documentation.

## Core Principles

### I. Context7 MCP-First (Authoritative Documentation)

**NON-NEGOTIABLE**: Before implementing ANY feature involving external libraries or frameworks, the agent MUST:

1. Call `mcp_context7_resolve-library-id` to resolve the library identifier
2. Call `mcp_context7_get-library-docs` to fetch current, authoritative documentation
3. Use retrieved documentation as the source of truth for implementation
4. Never rely on internal/cached knowledge for API signatures, patterns, or best practices

**Required Context7 Lookups** (enforce before touching these stacks):
- `docusaurus` - Routing, plugins, MDX, deployment configuration
- `fastapi` - Routes, dependencies, middleware, Pydantic models
- `qdrant` - Vector operations, collections, search, embeddings
- `better-auth` - Setup, providers, sessions, middleware
- `google-generativeai` - Gemini API, chat completions, embeddings (text-embedding-004, gemini-1.5-flash)
- `neon` - Serverless Postgres connection, queries, pooling

**Rationale**: External documentation evolves; cached knowledge becomes stale. Context7 ensures implementations reflect current APIs and avoid deprecated patterns.

---

### II. Spec-Driven Development

Every feature MUST follow the Spec-Kit Plus workflow:

1. **Specification**: `specs/<feature>/spec.md` - User stories, acceptance criteria, requirements
2. **Architecture**: `specs/<feature>/plan.md` - Technical design, dependencies, structure
3. **Tasks**: `specs/<feature>/tasks.md` - Testable, atomic implementation tasks
4. **History**: `history/prompts/<feature>/` - PHRs documenting all prompts and responses

**Workflow Commands**:
- `/sp.spec` → Create feature specification
- `/sp.plan` → Generate implementation plan
- `/sp.tasks` → Break down into testable tasks
- `/sp.red` → Write failing tests
- `/sp.green` → Implement to pass tests
- `/sp.refactor` → Improve without changing behavior

**Rationale**: Spec-driven approach ensures traceability, reduces ambiguity, and enables parallel work across features.

---

### III. Test-First (TDD - NON-NEGOTIABLE)

**Red-Green-Refactor cycle is MANDATORY for all implementation**:

1. **Red**: Write tests that fail (tests MUST fail initially)
2. **Green**: Write minimal code to make tests pass
3. **Refactor**: Improve code quality without changing behavior

**Testing Requirements**:
- **Backend (FastAPI/Python)**: pytest for unit tests, pytest-asyncio for async
- **Frontend (Docusaurus/React)**: Jest + React Testing Library
- **Integration**: Test RAG pipeline end-to-end, API contracts
- **E2E**: Critical user flows (optional but recommended)

**Coverage Thresholds**:
- API endpoints: 90% coverage minimum
- Business logic: 85% coverage minimum
- UI components: 70% coverage minimum

**Rationale**: Tests written after implementation tend to test what was built, not what should have been built. TDD ensures correctness by design.

---

### IV. Documentation-First

All architectural decisions MUST be documented before implementation:

1. **ADRs (Architecture Decision Records)**: Significant decisions in `history/adr/`
   - Trigger: Impact on long-term architecture, multiple alternatives considered, cross-cutting concerns
   - Suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`"
   - Never auto-create; require user consent

2. **PHRs (Prompt History Records)**: Every significant prompt in `history/prompts/`
   - Constitution prompts → `history/prompts/constitution/`
   - Feature prompts → `history/prompts/<feature-name>/`
   - General prompts → `history/prompts/general/`

3. **Inline Documentation**:
   - Python: Google-style docstrings with type hints
   - TypeScript: TSDoc comments for public APIs
   - MDX: Frontmatter metadata for all book chapters

**Rationale**: Documentation is a first-class artifact, not an afterthought. Future maintainers (and AI agents) rely on explicit decisions.

---

### V. Security & Secrets Management

**NON-NEGOTIABLE security requirements**:

1. **No Hardcoded Secrets**: All credentials, API keys, tokens MUST be in `.env` files
   - `.env.example` committed with placeholder values
   - `.env` in `.gitignore` (never committed)
   
2. **Authentication**: Better-Auth handles all session management
   - Secure cookie configuration (HttpOnly, SameSite, Secure)
   - CSRF protection enabled
   
3. **API Security**:
   - All mutation endpoints require authentication
   - Rate limiting on public endpoints (chatbot, translation)
   - Input validation via Pydantic models (FastAPI)
   
4. **Database Security**:
   - Parameterized queries only (no string concatenation)
   - Principle of least privilege for DB roles

**Rationale**: Security breaches are catastrophic and preventable. These rules eliminate common vulnerability classes.

---

### VI. Performance Standards

**Quantified performance budgets**:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Book page load | < 2 seconds | Lighthouse FCP |
| Chatbot response | < 5 seconds | API p95 latency |
| Personalization | < 10 seconds | API p95 latency |
| Translation | < 10 seconds | API p95 latency |
| Bundle size (JS) | < 500 KB | Webpack analyzer |

**Infrastructure Constraints**:
- Qdrant Cloud free tier: ~1M vectors maximum
- Neon Postgres free tier: 0.5 GB storage, auto-suspend
- GitHub Pages: Static hosting only, no server-side rendering

**Optimization Requirements**:
- Lazy-load chatbot widget
- Preload critical chapter content
- Use streaming responses for LLM operations

**Rationale**: Performance is a feature. Users abandon slow experiences. Budget-constrained infrastructure requires efficiency.

---

### VII. Code Quality

**Enforced standards by language**:

**TypeScript (Frontend/Docusaurus)**:
- Strict mode enabled (`"strict": true` in tsconfig)
- ESLint with recommended + React rules
- Prettier for formatting (2-space indent, single quotes)
- No `any` types without explicit justification

**Python (Backend/FastAPI)**:
- Type hints mandatory on all function signatures
- Ruff for linting (replaces flake8, isort, black)
- Pydantic models for all API schemas
- async/await for all I/O operations

**General**:
- All code MUST pass linting before commit
- No commented-out code in production
- Meaningful variable/function names (no single letters except loop indices)
- Maximum function length: 50 lines (extract if longer)

**Rationale**: Consistent code style reduces cognitive load and merge conflicts. Linting catches bugs before runtime.

---

### VIII. Observability & Traceability

**Logging Requirements**:

1. **Structured Logging**: JSON format for all production logs
   - Python: `structlog` or `python-json-logger`
   - Include: timestamp, level, message, request_id, user_id (if authenticated)

2. **Key Events to Log**:
   - API request/response (sanitized, no secrets)
   - RAG retrieval (query, top-k results, latency)
   - LLM calls (prompt tokens, completion tokens, model, latency)
   - Authentication events (login, logout, failures)
   - Errors with full stack traces

3. **PHR Traceability**:
   - Every user prompt generates a PHR
   - PHRs link to specs, ADRs, and PRs where applicable
   - Searchable history for debugging and learning

**Rationale**: Observability enables debugging production issues. Traceability enables understanding why decisions were made.

---

## Technology Stack

### Frontend (Book Platform)
| Technology | Purpose | Version |
|------------|---------|---------|
| Docusaurus | Static site generator | 3.x |
| React | UI components | 18.x |
| TypeScript | Type-safe JavaScript | 5.x |
| MDX | Markdown + JSX for chapters | 3.x |

### Backend (API & RAG)
| Technology | Purpose | Version |
|------------|---------|---------|
| FastAPI | API framework | 0.100+ |
| Python | Backend language | 3.11+ |
| Pydantic | Data validation | 2.x |
| Qdrant | Vector database | Cloud |
| Neon | Serverless Postgres | Cloud |
| Google Gemini API | LLM & embeddings (free tier) | Latest |

### Authentication
| Technology | Purpose | Version |
|------------|---------|---------|
| Better-Auth | Auth framework | Latest |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| GitHub Pages | Static hosting |
| GitHub Actions | CI/CD |

---

## Development Workflow

### Feature Implementation Flow

```
1. /sp.spec    → Define user stories, acceptance criteria
2. /sp.plan    → Architecture, Context7 lookups, structure
3. /sp.tasks   → Break into atomic testable tasks
4. /sp.red     → Write failing tests (TDD Red phase)
5. /sp.green   → Implement to pass tests
6. /sp.refactor→ Improve code quality
7. PHR         → Document prompt/response
```

### Constitution Check Gates

Before Phase 0 (Research) of any feature, verify:

- [ ] Context7 lookups identified for all external dependencies
- [ ] Feature aligns with project vision (Physical AI Textbook)
- [ ] Security requirements addressed (no new secrets exposed)
- [ ] Performance budget allocated
- [ ] Testing strategy defined

### Project Structure

```
/
├── book/                    # Docusaurus project
│   ├── docs/               # Book chapters (MDX)
│   │   ├── module-1-ros2/
│   │   ├── module-2-gazebo/
│   │   ├── module-3-isaac/
│   │   └── module-4-vla/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── css/
│   │   └── pages/
│   ├── static/
│   └── docusaurus.config.ts
├── api/                     # FastAPI backend
│   ├── app/
│   │   ├── routers/        # API routes
│   │   ├── services/       # Business logic
│   │   ├── models/         # Pydantic schemas
│   │   └── db/             # Database operations
│   ├── tests/
│   └── requirements.txt
├── specs/                   # Feature specifications
│   └── <feature>/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── history/                 # Project history
│   ├── prompts/            # PHRs by feature
│   │   ├── constitution/
│   │   ├── <feature-name>/
│   │   └── general/
│   └── adr/                # Architecture decisions
├── .specify/               # Spec-Kit Plus config
├── .github/
│   ├── workflows/          # CI/CD
│   └── prompts/            # Command prompts
└── .env.example            # Environment template
```

---

## Governance

### Authority

This constitution is the **authoritative source** for all development practices in this project. It supersedes:
- Prior conventions not documented here
- Individual preferences
- Cached AI knowledge (use Context7 instead)

### Amendment Process

1. **Propose**: Document the change and rationale
2. **Review**: Evaluate impact on existing code and specs
3. **Approve**: User consent required
4. **Update**: Increment version, update `LAST_AMENDED_DATE`
5. **Propagate**: Update dependent templates if affected

### Versioning Policy

- **MAJOR**: Backward-incompatible principle changes or removals
- **MINOR**: New principles, sections, or material expansions
- **PATCH**: Clarifications, typo fixes, non-semantic refinements

### Compliance

- All feature specs MUST reference this constitution
- All PRs MUST pass Constitution Check gates
- Deviations require explicit justification in ADR

---

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
