# UI/UX & i18n Implementation - Quick Reference

**Status**: ✅ Tasks Generated  
**File**: [tasks-ui-i18n.md](./tasks-ui-i18n.md)  
**Total Tasks**: 245 tasks across 5 weeks  
**Created**: 2025-12-10

---

## 🎯 Quick Start

### MVP Scope (2 weeks)
Start here for fastest time-to-value:
- ✅ Phase 1: UI/UX Foundation (39 tasks)
- ✅ Phase 2: i18n Infrastructure (49 tasks)
- ✅ French translation only (subset of Phase 3)

### Full Implementation (5 weeks)
- Week 1: UI/UX Foundation → Enhanced design, accessibility
- Week 2: i18n Infrastructure → 4 languages enabled
- Week 3-4: Content Translation → French, Arabic, Urdu
- Week 5: Polish & Production → SEO, performance, UAT

---

## 📋 Phase Overview

| Phase | Tasks | Timeline | Key Deliverable |
|-------|-------|----------|-----------------|
| **Phase 1: UI/UX** | T001-T039 | Week 1 | Modern design system, WCAG 2.1 AA |
| **Phase 2: i18n Infra** | T040-T088 | Week 2 | 4 locales working, language switcher |
| **Phase 3: Translation** | T089-T160 | Week 3-4 | Content translated (fr, ar, ur) |
| **Phase 4: Polish** | T161-T226 | Week 5 | Production-ready, UAT approved |
| **Deployment** | T227-T245 | End Week 5 | Live multi-language site |

---

## 🚀 Getting Started

### 1. Start Phase 1 (UI/UX)
```bash
cd book/
git checkout -b ui-i18n-enhancement
```

**First Tasks**:
- T001: Verify Node.js 18+ and npm 9+
- T002: Install dependencies: `npm install --save-dev clsx`
- T004: Create color palette in `src/css/custom.css`

### 2. Validation Checkpoints
After each phase:
```bash
# Build all locales
npm run build

# Serve locally
npm run serve

# Test RAG pipeline
cd ..
python test_rag.py
```

---

## 🎨 Phase 1: UI/UX Foundation (Week 1)

**Goal**: Modern design without i18n complexity

### Key Files to Edit
- `book/src/css/custom.css` - Design system (T004-T006)
- `book/docusaurus.config.js` - Navigation config (T008-T010, T013)
- `book/src/components/ChatWidget/ChatWidget.module.css` - Widget styles (T016-T020)
- `book/src/components/ChatWidget/index.tsx` - Apply new styles (T021)

### Parallel Tasks
Run simultaneously:
- CSS updates (T004, T005, T006)
- Prism setup (T012, T013)
- ChatWidget styles (T017-T020)
- Browser testing (T029-T033)

### Validation
- [ ] Lighthouse: Performance ≥90, Accessibility ≥95
- [ ] RAG chatbot still works
- [ ] Mobile responsive (iPhone, Android)

---

## 🌍 Phase 2: i18n Infrastructure (Week 2)

**Goal**: Enable 4 languages, no content translation yet

### Key Files to Edit
- `book/docusaurus.config.js` - Add locales config (T041-T046)
- `book/src/css/rtl.css` - RTL styles (T053-T057)
- `book/src/components/ChatWidget/translations.ts` - UI strings (T060-T065)
- `book/src/components/ChatWidget/index.tsx` - Locale detection (T066-T068)

### Commands
```bash
# Generate translation files
npm run write-translations -- --locale fr
npm run write-translations -- --locale ar
npm run write-translations -- --locale ur

# Build all locales
npm run build

# Test specific locale
npm run build -- --locale ar
```

### Validation
- [ ] All 4 locales build without errors
- [ ] Language switcher appears in navbar
- [ ] RTL layout correct for Arabic/Urdu
- [ ] RAG works in all locale routes

---

## 📝 Phase 3: Content Translation (Week 3-4)

**Goal**: Translate high-priority content with human review

### Translation Priority
1. **Priority 1** (T100-T106): intro.mdx, module landing pages
2. **Priority 2** (T107-T112): Module 1 Week 01
3. **UI Strings** (T113-T122): navbar, footer, ChatWidget

### Optional: Translation Script
Create `scripts/translate_content.py` (T089-T096):
```python
# Usage:
python scripts/translate_content.py \
  book/docs/intro.mdx \
  fr \
  book/i18n/fr/docusaurus-plugin-content-docs/current/intro.mdx
```

### Human Review Process
- **French** (T123-T129): Find reviewer, provide guidelines, incorporate feedback
- **Arabic** (T130-T137): Review + RTL rendering checks
- **Urdu** (T138-T145): Review + font rendering checks

### Validation
- [ ] Native speaker approval for each language
- [ ] Code blocks remain in English
- [ ] No broken links in translated content
- [ ] RTL layout correct for ar/ur

---

## 🎨 Phase 4: Polish & Production (Week 5)

**Goal**: Production-ready quality

### Key Activities
- **SEO** (T161-T166): Metadata for all locales
- **Performance** (T172-T178): Bundle optimization, code splitting
- **Accessibility** (T179-T185): axe DevTools audits for all languages
- **Testing** (T186-T205): Cross-browser, mobile, RAG regression
- **UAT** (T206-T212): Native speaker testing
- **Documentation** (T213-T219): README, CONTRIBUTING, guidelines

### Testing Matrix
| Browser | Desktop | Mobile |
|---------|---------|--------|
| Chrome | T186 | T194 |
| Firefox | T187 | - |
| Safari | T188 | T192, T193 |
| Edge | T189 | - |

### Validation
- [ ] Lighthouse scores meet targets (all locales)
- [ ] UAT approved by native speakers
- [ ] Documentation complete
- [ ] RAG regression tests pass

---

## 🚢 Deployment (End of Week 5)

### Production Checklist
```bash
# Final build
npm run build

# Verify output
ls -la book/build/
# Should see: index.html, fr/, ar/, ur/

# Deploy to GitHub Pages
git push origin main
```

### Post-Deployment
- T230: Verify production URLs (base, /fr/, /ar/, /ur/)
- T233: Test RAG on production
- T235-T239: Monitor errors, analytics, user feedback

---

## 🔄 Parallel Execution Opportunities

**80 tasks (33%) can run in parallel** - marked with `[P]`

### Phase 1 Parallel Groups
- **CSS Group**: T004, T005, T006 (different sections)
- **ChatWidget**: T017, T018, T019, T020 (different classes)
- **Testing**: T029-T033 (independent browsers/devices)

### Phase 2 Parallel Groups
- **Locale Configs**: T042-T045 (each language independent)
- **RTL Styles**: T054-T057 (different selectors)
- **Translations**: T061-T064 (per language)

### Phase 3 Parallel Groups
- **Content**: T100-T102 (intro per language)
- **UI Strings**: T113-T121 (navbar/footer/code per language)

### Phase 4 Parallel Groups
- **SEO**: T161-T163 (per locale)
- **Browsers**: T186-T189 (independent testing)
- **Mobile**: T192-T195 (independent devices)

---

## ⚠️ Critical Principles

### Zero RAG Disruption
- ✅ **DO**: Edit frontend files (CSS, React, MDX, config)
- ❌ **DON'T**: Touch `api/` backend code
- ❌ **DON'T**: Modify database schema
- ❌ **DON'T**: Change vector database setup

### After Every Phase
1. Run full build: `npm run build`
2. Test RAG: `python test_rag.py`
3. Verify chatbot in browser
4. Commit with descriptive message

### Rollback Strategy
If issues arise:
```bash
# Immediate rollback
git revert <commit-hash>

# Or revert to phase tag
git checkout v0.1.0-phase2

# Or English-only fallback
npm run build -- --locale en
```

---

## 📊 Success Metrics

### Technical
- [ ] All 4 locales build successfully
- [ ] Lighthouse: Performance ≥90, Accessibility ≥95
- [ ] Bundle size <500KB per locale
- [ ] RAG test script passes

### User Experience
- [ ] Native speaker approval (all 3 languages)
- [ ] Language switcher intuitive
- [ ] RTL layout natural for Arabic/Urdu
- [ ] ChatWidget functional in all locales

### Project
- [ ] Complete within 5 weeks (or 2 for MVP)
- [ ] Documentation complete
- [ ] Stakeholder approval

---

## 🔗 Key Documents

- **Tasks File**: [tasks-ui-i18n.md](./tasks-ui-i18n.md) - Full task breakdown
- **Architecture Plan**: [ui-i18n-enhancement-plan.md](./ui-i18n-enhancement-plan.md) - Design decisions
- **PHR**: [0008-generate-ui-i18n-tasks.tasks.prompt.md](../../history/prompts/001-physical-ai-textbook-platform/0008-generate-ui-i18n-tasks.tasks.prompt.md) - Task generation record

### ADRs (Architecture Decisions)
- **ADR-001**: Use Docusaurus built-in i18n (not runtime translation)
- **ADR-002**: Keep API responses English-only (for now)
- **ADR-003**: Hybrid translation approach (Gemini + human review)

---

## 🎯 Next Actions

### Option 1: Start Phase 1 (Recommended)
```bash
cd book/
npm install --save-dev clsx
# Begin with T004: Edit src/css/custom.css
```

### Option 2: MVP Fast-Track
Focus on:
- Phase 1 complete (UI/UX)
- Phase 2 complete (i18n infra)
- French translation only (skip Arabic/Urdu for iteration 2)

### Option 3: Create GitHub Issues
Convert tasks to issues for project management:
- Use task IDs as issue titles
- Group by phase
- Assign to team members

---

**Ready to implement!** Each task has specific file paths and clear acceptance criteria. Start with Phase 1 for immediate UI improvements, or jump straight to MVP scope for fastest deployment.
