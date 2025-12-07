# Feature Specification: Physical AI & Humanoid Robotics Textbook Platform

**Feature Branch**: `001-physical-ai-textbook-platform`  
**Created**: 2025-12-07  
**Status**: Draft  
**Input**: User description: "Physical AI & Humanoid Robotics Textbook Platform with Docusaurus book, RAG chatbot, Better-Auth, personalization, and Urdu translation"

---

## Problem Statement

Panaversity needs an AI-native textbook platform to teach the Physical AI & Humanoid Robotics course in a way that:

- Matches the technical depth of the course (ROS 2, Gazebo, NVIDIA Isaac, VLA).
- Lets students interact with the content via an integrated RAG chatbot.
- Adapts explanations to each student's software/hardware background.
- Supports Urdu translation to increase accessibility.
- Demonstrates best practices in Spec-Driven Development, TDD, and AI-native tooling.

The hackathon requires a unified project that delivers:

- A Docusaurus-based book deployed to GitHub Pages.
- An integrated RAG chatbot powered by OpenAI/ChatKit, FastAPI, Neon, and Qdrant.
- Optional but high-value enhancements: reusable subagents, auth/profile, personalization, and Urdu translation.

### Target Users

| Persona | Description |
|---------|-------------|
| **Student** | Learns Physical AI concepts and code, with varying technical backgrounds |
| **Instructor/Author** | Writes and maintains textbook content, labs, and examples |
| **Anonymous Visitor** | Browses and samples content and basic chatbot functionality without logging in |

---

## Goals & Non-Goals

### Goals

| ID | Goal |
|----|------|
| G-001 | Deliver a Docusaurus 3 book site with 4 modules and ~13 weeks of content structure aligned to the course outline |
| G-002 | Embed a RAG chatbot that answers questions about the textbook content, including questions scoped to user-selected text |
| G-003 | Implement signup/signin using Better-Auth, including an onboarding survey to capture each user's software/hardware background and store it in Neon Postgres |
| G-004 | Enable per-user content personalization at the chapter level based on the stored background profile |
| G-005 | Enable chapter-level Urdu translation while preserving MDX formatting and code blocks |
| G-006 | Create Claude Code subagents and Agent Skills to reuse intelligence for documentation lookup, scaffolding, and content generation |
| G-007 | Enforce the project constitution: Context7 MCP-First, Spec-Driven, TDD, code quality, security, and observability |

### Non-Goals

| ID | Non-Goal |
|----|----------|
| NG-001 | No real-world robot control or deployment (simulation/teaching focus only) |
| NG-002 | No native mobile apps; the scope is web-only |
| NG-003 | No advanced multi-tenant SaaS features (teams, organizations, billing) |
| NG-004 | No requirement to support offline-first reading or PWA behavior |
| NG-005 | No custom LLM training beyond prompt engineering and standard embeddings/RAG |

---

## Sub-Features (Decomposition)

This top-level spec covers the full platform. Each sub-feature below will receive its own `/sp.spec` for detailed implementation:

| Sub-Feature | Scope | Priority |
|-------------|-------|----------|
| `book-platform` | Docusaurus 3 setup, 4 modules, 13+ chapters (MDX), GitHub Pages CI/CD | P1 (Base) |
| `rag-chatbot` | FastAPI backend, Qdrant vectors, Neon chat history, OpenAI RAG, embedded widget, selected-text Q&A | P1 (Base) |
| `auth-and-profile` | Better-Auth signup/signin, onboarding survey, user profiles in Neon | P2 (Bonus) |
| `content-personalization` | "Personalize" button per chapter, LLM-driven adaptation by user profile | P2 (Bonus) |
| `urdu-translation` | "Translate to Urdu" button per chapter, preserve MDX/code, caching | P2 (Bonus) |
| `reusable-intelligence` | Claude Code subagents, Agent Skills for Context7 lookup, code gen, content drafting | P2 (Bonus) |
| `devx-and-governance` | Context7 MCP-First enforcement, TDD workflows, PHR/ADR practices, CI/linting | P1 (Foundation) |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read and Navigate Chapters (Priority: P1)

As a **Student**, I want to browse modules and chapters in the Physical AI textbook so that I can follow the course sequence and find relevant content quickly.

**Why this priority**: Reading and navigation are the absolute core of the textbook; everything else builds on this.

**Independent Test**: A student can open the site, navigate from the home page to a module, select a chapter (week), and read the content without any errors or broken links.

**Acceptance Scenarios**:

1. **Given** I open the book homepage, **When** I click on "Module 1: ROS 2", **Then** I see a list of chapters for that module and can open "Week 1" content.
2. **Given** I am reading a chapter, **When** I use the sidebar navigation, **Then** I can move between weeks and modules without encountering 404s or broken links.
3. **Given** the book is deployed to GitHub Pages, **When** I access the public URL, **Then** the site loads in under 2 seconds on a standard connection.

---

### User Story 2 - Ask Questions About Content (Priority: P1)

As a **Student**, I want to ask questions about what I am reading so that I can clarify misunderstandings quickly.

**Why this priority**: RAG chatbot is a core hackathon requirement and central to the AI-native experience.

**Independent Test**: From any chapter page, the user can open the chatbot, ask a question about the content, and receive a relevant answer based only on the textbook.

**Acceptance Scenarios**:

1. **Given** I am on a chapter page, **When** I open the chatbot and ask "What is ROS 2?", **Then** I receive an answer grounded in the textbook's ROS 2 description within 5 seconds.
2. **Given** I ask a question about content not present in the book, **When** the RAG system cannot find relevant context, **Then** it responds with a graceful fallback message indicating the limitation (no hallucinated external facts).
3. **Given** the chatbot is opened, **When** I type and submit a question, **Then** I see a loading indicator until the response arrives.

---

### User Story 3 - Ask Questions About Selected Text (Priority: P1)

As a **Student**, I want to highlight specific text and ask a question about it so that I can get explanations tailored to that passage.

**Why this priority**: This is called out explicitly in the hackathon requirements and showcases deep integration.

**Independent Test**: Highlighting text in a chapter and invoking the chatbot uses only the selected passage as primary context in the answer.

**Acceptance Scenarios**:

1. **Given** I highlight a paragraph about "URDF for humanoid robots", **When** I click "Ask about selection" and ask "Explain this in simpler terms", **Then** the answer clearly references and simplifies that paragraph.
2. **Given** I highlight code in MDX, **When** I ask "What does this function do?", **Then** the answer explains the code without including unrelated content.
3. **Given** I highlight text but do not ask a question, **When** I simply open the chatbot, **Then** the selected text is shown as context that I can optionally use.

---

### User Story 4 - Sign Up and Complete Background Survey (Priority: P1)

As a **Student**, I want to sign up and answer a short background survey so that the platform can personalize explanations to my experience level and hardware.

**Why this priority**: Required for personalization bonuses and aligns with the constitution's personalization and security principles.

**Independent Test**: A new user can sign up with Better-Auth, complete onboarding questions, and see their profile stored in Neon.

**Acceptance Scenarios**:

1. **Given** I am a new user, **When** I click "Sign up" and complete the form using Better-Auth, **Then** my account is created and I am redirected to the onboarding survey.
2. **Given** I complete questions about my programming experience and available hardware, **When** I submit the survey, **Then** my profile (experience level, hardware capabilities) is stored in Neon and associated with my account.
3. **Given** I already have an account, **When** I sign in, **Then** I am taken to the book homepage with my profile loaded.

---

### User Story 5 - See Personalized Explanations (Priority: P2)

As a **Student**, I want to click a "Personalize this chapter" button so that the content better matches my background and hardware constraints.

**Why this priority**: High-impact differentiation feature that leverages the background survey.

**Independent Test**: Two users with different backgrounds see different inline adaptive callouts for the same chapter after clicking "Personalize".

**Personalization Delivery**: Inline adaptive callouts/snippets are layered within the canonical chapter (highlighted boxes, expandable notes, or footnotes) rather than replacing the entire chapter view.

**Acceptance Scenarios**:

1. **Given** I am marked as a beginner with no prior ROS 2 experience, **When** I click "Personalize" on a ROS 2 chapter, **Then** I see inline callout boxes with step-by-step, beginner-friendly explanations inserted at key sections within 10 seconds.
2. **Given** I am marked as advanced with a strong software background and RTX workstation access, **When** I click "Personalize" on the same chapter, **Then** I see inline callouts with concise, advanced-focused tips and optimization notes instead of beginner content.
3. **Given** I am not logged in, **When** I click "Personalize", **Then** I am prompted to sign in or sign up first.
4. **Given** I have personalized a chapter, **When** I toggle personalization off, **Then** the inline callouts are hidden and the canonical chapter content remains unchanged.

---

### User Story 6 - Translate Chapter to Urdu (Priority: P2)

As a **Student**, I want to translate a chapter to Urdu so that I can understand complex topics more comfortably in my native language.

**Why this priority**: Directly maps to a bonus requirement and improves accessibility.

**Independent Test**: Clicking "Translate to Urdu" generates an Urdu version of the chapter while preserving structure and code formatting.

**Acceptance Scenarios**:

1. **Given** I am reading an English chapter, **When** I click "Translate to Urdu", **Then** the main text is translated into Urdu while code blocks and inline code remain in the original language, within 10 seconds.
2. **Given** I navigate away and return to the chapter, **When** I revisit the translation option, **Then** the behavior is consistent (either reusing a cached result or regenerating predictably).
3. **Given** the translation service fails, **When** the error occurs, **Then** I see a user-friendly error message and can retry.

---

### User Story 7 - Author Updates Content (Priority: P2)

As an **Instructor/Author**, I want to edit MDX content and have the chatbot index updated so that Q&A stays aligned with the textbook.

**Why this priority**: Keeps the RAG system in sync with evolving content.

**Independent Test**: After a content update, re-indexing occurs (manually or automatically), and new Q&A responses follow the updated content.

**Acceptance Scenarios**:

1. **Given** I modify a chapter's MDX file and run the indexing process, **When** I ask a question about the updated section, **Then** the chatbot answer reflects the new text, not the old version.
2. **Given** the indexing process fails, **When** I check logs or an admin view, **Then** I see a clear error and guidance for remediation.

---

### User Story 8 - Anonymous Visitor Browses Content (Priority: P2)

As an **Anonymous Visitor**, I want to browse public chapters and try the chatbot so that I can evaluate the platform before signing up.

**Why this priority**: Encourages sign-ups by demonstrating value upfront.

**Independent Test**: An unauthenticated user can read chapters and ask basic questions.

**Acceptance Scenarios**:

1. **Given** I am not logged in, **When** I navigate to a public chapter, **Then** I can read the full content.
2. **Given** I am not logged in, **When** I open the chatbot and ask a question, **Then** I receive an answer (personalization and translation buttons are disabled or prompt login).

---

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Qdrant or Neon temporarily unavailable | Chatbot degrades gracefully with an explanatory message; no stack traces to the user |
| User with extremely low bandwidth | Core reading experience still works; advanced features fail gracefully with messaging |
| Incomplete or inconsistent background survey | Personalization falls back to a default track; surfaces a prompt to complete/update the profile |
| Translation or personalization LLM call fails/times out | Show a clear error and provide a way to retry; the original English chapter remains available |
| User highlights no text but clicks "Ask about selection" | Chatbot opens with empty context; user can still type a general question |
| Very long chapter translation (>10,000 tokens) | Chunk the translation or show progress; do not time out silently |

---

## Requirements *(mandatory)*

### Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-001 | System MUST render a Docusaurus-based book with modules and chapters that map to the 13-week Physical AI course outline |
| FR-002 | System MUST embed a chatbot widget on chapter pages that answers questions using RAG grounded only in textbook content |
| FR-003 | System MUST allow users to highlight text in a chapter and send it as primary context to the chatbot for Q&A |
| FR-004 | System MUST implement signup and signin using Better-Auth, including secure session handling |
| FR-005 | System MUST present an onboarding survey at first login to capture software and hardware background, and persist responses in Neon Postgres |
| FR-006 | System MUST provide a "Personalize" button per chapter that layers inline adaptive callouts/snippets (highlighted boxes, footnotes) based on the stored user profile, without replacing the canonical chapter content |
| FR-007 | System MUST provide a "Translate to Urdu" button per chapter that returns an Urdu rendering with MDX structure and code blocks preserved |
| FR-008 | System MUST create and use Claude Code subagents and Agent Skills for documentation lookup, code generation, and content drafting |
| FR-009 | System MUST log significant events (auth, RAG queries, translation, personalization) in a structured format |
| FR-010 | System MUST align with the Context7 MCP-First principle for all external dependency usage (Docusaurus, FastAPI, Qdrant, Better-Auth, OpenAI, Neon) |

### Key Entities

| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| **User** | Authenticated user account | id, email, auth_provider_data, created_at, updated_at |
| **UserProfile** | User's background and preferences | user_id, programming_experience_level, robotics_experience_level, available_hardware, preferred_language, last_updated_at |
| **Chapter** | A single chapter/week in the book | id, module_id, slug, title, mdx_path, last_indexed_at |
| **ChatSession** | A conversation session | id, user_id (nullable for anonymous), created_at |
| **ChatMessage** | A single message in a session | id, session_id, role (user/assistant/system), content, created_at, metadata (selected_text_range, embeddings_id) |

---

## Constraints & Assumptions

### Constraints

| ID | Constraint |
|----|------------|
| C-001 | GitHub Pages is static hosting only; no server-side rendering |
| C-002 | Neon Postgres free tier: 0.5 GB storage, auto-suspend after inactivity |
| C-003 | Qdrant Cloud free tier: ~1M vectors maximum |
| C-004 | No hardcoded secrets; all credentials via `.env` files |
| C-005 | Context7 MCP MUST be used for Docusaurus, FastAPI, Qdrant, Better-Auth, OpenAI, Neon documentation lookups before implementation |
| C-006 | Demo video must be under 90 seconds |

### Assumptions

| ID | Assumption |
|----|------------|
| A-001 | Students have basic web browser access and internet connectivity |
| A-002 | Google Gemini API keys will be provided for embeddings and chat completions (free tier preferred) |
| A-003 | The 13-week course outline in hackathon-requirements.md is the authoritative content structure |
| A-004 | Better-Auth supports email/password authentication out of the box |
| A-005 | Translation to Urdu uses LLM-based translation (not a dedicated translation API) |

---

## High-Level Dependencies

| Dependency | Purpose | Context7 MCP Required |
|------------|---------|----------------------|
| Docusaurus 3.x | Static site generator for the book | ✅ MUST call `mcp_context7_resolve-library-id` before implementation |
| FastAPI | Python backend API for RAG, auth, personalization | ✅ MUST call `mcp_context7_resolve-library-id` before implementation |
| Qdrant Cloud | Vector database for embeddings/RAG | ✅ MUST call `mcp_context7_resolve-library-id` before implementation |
| Neon Serverless Postgres | Relational database for users, profiles, chat history | ✅ MUST call `mcp_context7_resolve-library-id` before implementation |
| Google Gemini API | Embeddings (text-embedding-004 free tier) and chat completions | ✅ MUST call `mcp_context7_resolve-library-id` before implementation |
| Better-Auth | Authentication framework | ✅ MUST call `mcp_context7_resolve-library-id` before implementation |
| GitHub Pages | Static hosting for the book | Standard deployment; no Context7 needed |
| GitHub Actions | CI/CD for build and deploy | Standard usage; no Context7 needed |

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

| ID | Criterion | Target |
|----|-----------|--------|
| SC-001 | Students can navigate from the book homepage to any chapter | ≤ 3 clicks, page load < 2 seconds |
| SC-002 | Chatbot responses for standard questions | < 5 seconds (p95) |
| SC-003 | Questions directly about textbook content receive grounded answers | ≥ 80% (manual sampling) |
| SC-004 | Personalization and translation complete | < 10 seconds (p95) |
| SC-005 | Hardcoded secrets in repository | 0 incidents (verified via scans) |
| SC-006 | Backend endpoints and core frontend flows have automated tests | Coverage per constitution thresholds |
| SC-007 | All external dependencies have documented Context7 MCP lookup IDs | 100% of dependencies listed |

---

## NFRs (from Constitution)

### Performance

| Metric | Target |
|--------|--------|
| Book page load | < 2 seconds |
| Chatbot response | < 5 seconds |
| Personalization/Translation | < 10 seconds |
| Bundle size (JS) | < 500 KB |

### Security

- No hardcoded secrets; `.env` pattern enforced
- Better-Auth handles session management with secure cookies
- All mutation endpoints require authentication
- Input validation via Pydantic models

### Code Quality

- TypeScript strict mode for frontend
- Python type hints mandatory for backend
- ESLint + Prettier for JS/TS
- Ruff for Python linting
- All code must pass linting before commit

### Testing

- Unit tests for API endpoints (pytest)
- Integration tests for RAG pipeline
- E2E tests for critical user flows (optional but recommended)
- Coverage: 90% API, 85% business logic, 70% UI

---

## Appendix: Course Content Structure

Based on `hackathon-requirements.md`, the book modules and chapters are:

| Module | Title | Weeks/Chapters |
|--------|-------|----------------|
| 1 | The Robotic Nervous System (ROS 2) | Weeks 1-5 |
| 2 | The Digital Twin (Gazebo & Unity) | Weeks 6-7 |
| 3 | The AI-Robot Brain (NVIDIA Isaac) | Weeks 8-10 |
| 4 | Vision-Language-Action (VLA) & Conversational Robotics | Weeks 11-13 |

**Total**: 4 modules, 13 weeks of content.

---

## Clarifications

### Session 2025-12-07

- Q: How should personalized content be presented to the user? → A: Option B – Layer inline adaptive callouts/snippets within the canonical chapter (highlighted boxes, footnotes) rather than replacing the entire chapter.
