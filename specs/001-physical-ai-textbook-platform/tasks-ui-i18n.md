# Tasks: UI/UX Enhancement & Multi-Language Support (i18n)

**Feature**: UI/UX Improvements + Internationalization  
**Target Languages**: English (en), French (fr), Arabic (ar), Urdu (ur)  
**Created**: 2025-12-10  
**Status**: Ready for Implementation  
**Parent Feature**: `001-physical-ai-textbook-platform`

---

## Overview

This tasks document implements the [ui-i18n-enhancement-plan.md](./ui-i18n-enhancement-plan.md) to add modern UI/UX improvements and multi-language support to the Physical AI Textbook platform.

**Core Principle**: Zero disruption to the working RAG pipeline. All changes are isolated to the frontend presentation layer.

**Implementation Strategy**:
- **Phase 1 (Week 1)**: UI/UX Foundation - Can deploy independently
- **Phase 2 (Week 2)**: i18n Infrastructure - Enables language switching
- **Phase 3 (Week 3-4)**: Content Translation - Incremental, per-language
- **Phase 4 (Week 5)**: Polish & Production - Quality assurance

---

## Phase 1: UI/UX Foundation (Week 1)

**Goal**: Enhance visual design and accessibility without adding i18n complexity.

**Deliverable**: Enhanced UI with modern design system, improved navigation, and WCAG 2.1 AA accessibility.

**Independent Test Criteria**:
- [ ] Lighthouse scores: Performance ≥90, Accessibility ≥95
- [ ] Visual regression tests pass (or manual approval)
- [ ] RAG chatbot continues to function identically
- [ ] No console errors in browser DevTools
- [ ] Mobile responsive on iPhone and Android devices

### Setup & Prerequisites

- [ ] T001 Verify Node.js and npm versions (Node 18+, npm 9+) in book/ directory
- [ ] T002 Install required development dependencies: `npm install --save-dev clsx` in book/
- [ ] T003 Create backup branch before UI changes: `git checkout -b ui-ux-backup`

### Design System Implementation

- [ ] T004 [P] Create custom color palette in `book/src/css/custom.css` (primary, semantic, dark mode colors)
- [ ] T005 [P] Update typography settings in `book/src/css/custom.css` (Inter font, line heights, spacing)
- [ ] T006 [P] Add shadow and layout variables in `book/src/css/custom.css` (container widths, shadows)
- [ ] T007 Test dark mode color scheme by toggling in browser and verifying contrast ratios

### Navigation Enhancements

- [ ] T008 [P] Enable breadcrumbs in `book/docusaurus.config.js` (set `breadcrumbs: true` in docs plugin)
- [ ] T009 [P] Configure table of contents sidebar in `book/docusaurus.config.js` (set `toc: {minHeadingLevel: 2, maxHeadingLevel: 4}`)
- [ ] T010 [P] Add docs navigation footer in `book/docusaurus.config.js` (enable previous/next buttons)
- [ ] T011 Test navigation flow: sidebar → chapter → breadcrumbs → previous/next buttons

### Code Block Enhancements

- [ ] T012 [P] Install Prism themes for enhanced syntax highlighting: `npm install --save prism-react-renderer` in book/
- [ ] T013 [P] Configure code block theme in `book/docusaurus.config.js` (prism theme, line numbers, copy button)
- [ ] T014 Add custom styles for code blocks in `book/src/css/custom.css` (filename tabs, improved contrast)
- [ ] T015 Test code block features: copy button works, line numbers display, syntax highlighting correct

### ChatWidget Visual Redesign

- [ ] T016 Create ChatWidget styles module at `book/src/components/ChatWidget/ChatWidget.module.css`
- [ ] T017 [P] Implement gradient header styling in `ChatWidget.module.css` (blue gradient, rounded corners)
- [ ] T018 [P] Add message bubble styles in `ChatWidget.module.css` (user/assistant distinction, shadows, spacing)
- [ ] T019 [P] Create smooth animations in `ChatWidget.module.css` (slide-in, fade, typing indicator)
- [ ] T020 [P] Add responsive styles in `ChatWidget.module.css` (full-screen mobile, overlay desktop)
- [ ] T021 Update `book/src/components/ChatWidget/index.tsx` to import and apply new styles
- [ ] T022 Test ChatWidget visual improvements: animations smooth, mobile responsive, no layout shift

### Accessibility Audit

- [ ] T023 Run Lighthouse accessibility audit on 3+ pages and document scores
- [ ] T024 Add ARIA labels to interactive elements in `book/src/components/ChatWidget/index.tsx` (buttons, inputs)
- [ ] T025 [P] Verify keyboard navigation: Tab through all interactive elements, test Enter/Esc keys
- [ ] T026 [P] Test color contrast ratios using browser DevTools or axe extension (minimum 4.5:1)
- [ ] T027 Add skip-to-content link in `book/src/theme/Root.tsx` (create if doesn't exist)
- [ ] T028 Test with screen reader (NVDA on Windows or VoiceOver on Mac) and document findings

### Responsive Design Testing

- [ ] T029 [P] Test on Chrome desktop (1920x1080) - verify layout, navigation, chat widget
- [ ] T030 [P] Test on Firefox desktop (1920x1080) - verify cross-browser compatibility
- [ ] T031 [P] Test on mobile Chrome (375x667 iPhone SE) - verify responsive layout
- [ ] T032 [P] Test on mobile Safari (390x844 iPhone 12) - verify iOS compatibility
- [ ] T033 Test on tablet (768x1024 iPad) - verify tablet breakpoints
- [ ] T034 Document any browser-specific issues in `specs/001-physical-ai-textbook-platform/ui-testing-notes.md`

### Phase 1 Validation

- [ ] T035 Run full build: `cd book && npm run build` - verify no errors
- [ ] T036 Serve locally: `npm run serve` - manually test all features
- [ ] T037 Verify RAG chatbot still functional: open chat, send test message, verify response
- [ ] T038 Take screenshots of before/after for documentation
- [ ] T039 Commit Phase 1 changes with message: "feat: UI/UX enhancements - modern design system and accessibility"

---

## Phase 2: i18n Infrastructure (Week 2)

**Goal**: Enable multi-language support (4 locales) with working language switcher, no content translation yet.

**Deliverable**: Infrastructure for French, Arabic, Urdu translations with placeholder content.

**Independent Test Criteria**:
- [ ] All 4 locales (en, fr, ar, ur) build successfully
- [ ] Language switcher dropdown appears and works
- [ ] RTL layout correct for Arabic and Urdu
- [ ] RAG pipeline continues to work in all locale routes
- [ ] No 404 errors when switching languages

### Docusaurus i18n Configuration

- [ ] T040 Backup current `book/docusaurus.config.js` before i18n changes
- [ ] T041 Add locales array to i18n config in `book/docusaurus.config.js` (`locales: ['en', 'fr', 'ar', 'ur']`)
- [ ] T042 [P] Configure locale metadata for English in `book/docusaurus.config.js` (label, direction: ltr, htmlLang)
- [ ] T043 [P] Configure locale metadata for French in `book/docusaurus.config.js` (label: "Français", direction: ltr, htmlLang: fr-FR)
- [ ] T044 [P] Configure locale metadata for Arabic in `book/docusaurus.config.js` (label: "العربية", direction: rtl, htmlLang: ar-SA)
- [ ] T045 [P] Configure locale metadata for Urdu in `book/docusaurus.config.js` (label: "اردو", direction: rtl, htmlLang: ur-PK)
- [ ] T046 Add locale dropdown to navbar in `book/docusaurus.config.js` (type: 'localeDropdown', position: 'right')
- [ ] T047 Test configuration: `npm run build` - verify config is valid

### Generate Translation Files

- [ ] T048 Run `npm run write-translations -- --locale fr` to generate French translation files
- [ ] T049 Run `npm run write-translations -- --locale ar` to generate Arabic translation files
- [ ] T050 Run `npm run write-translations -- --locale ur` to generate Urdu translation files
- [ ] T051 Verify directory structure created: `book/i18n/{fr,ar,ur}/docusaurus-theme-classic/`
- [ ] T052 Verify JSON files generated: `navbar.json`, `footer.json` for each locale

### RTL Stylesheet

- [ ] T053 Create RTL stylesheet at `book/src/css/rtl.css`
- [ ] T054 [P] Implement RTL navbar styles in `book/src/css/rtl.css` (flex-direction: row-reverse)
- [ ] T055 [P] Implement RTL sidebar styles in `book/src/css/rtl.css` (text-align: right, reversed icons)
- [ ] T056 [P] Implement RTL markdown styles in `book/src/css/rtl.css` (margin adjustments)
- [ ] T057 [P] Force LTR for code blocks in `book/src/css/rtl.css` (direction: ltr for pre/code elements)
- [ ] T058 Import `rtl.css` in `book/src/css/custom.css` (add `@import './rtl.css';`)
- [ ] T059 Test RTL layout by building with `npm run build -- --locale ar` and serving

### ChatWidget i18n Support

- [ ] T060 Create translations file at `book/src/components/ChatWidget/translations.ts`
- [ ] T061 [P] Define English strings in `translations.ts` (title, placeholder, send, typing, sources, error, close)
- [ ] T062 [P] Define French strings in `translations.ts` (translated UI labels)
- [ ] T063 [P] Define Arabic strings in `translations.ts` (translated UI labels in Arabic script)
- [ ] T064 [P] Define Urdu strings in `translations.ts` (translated UI labels in Urdu script)
- [ ] T065 Export translation object with locale keys in `translations.ts`
- [ ] T066 Update `book/src/components/ChatWidget/index.tsx` to accept `locale` prop
- [ ] T067 Implement locale detection in `book/src/components/ChatWidget/index.tsx` (use Docusaurus useDocusaurusContext)
- [ ] T068 Apply translations in ChatWidget based on current locale
- [ ] T069 Test ChatWidget strings change when switching languages

### Build & Test All Locales

- [ ] T070 Build all locales: `npm run build` - verify builds for en, fr, ar, ur
- [ ] T071 Verify build output structure: `book/build/{index.html, fr/, ar/, ur/}`
- [ ] T072 Serve locally: `npm run serve` and test language switcher dropdown
- [ ] T073 [P] Test English locale: navigate to `/`, verify content and layout
- [ ] T074 [P] Test French locale: navigate to `/fr/`, verify navbar/footer show French labels
- [ ] T075 [P] Test Arabic locale: navigate to `/ar/`, verify RTL layout applied
- [ ] T076 [P] Test Urdu locale: navigate to `/ur/`, verify RTL layout applied
- [ ] T077 Test RAG chatbot in each locale: open chat, send message, verify API call succeeds

### Deployment Configuration

- [ ] T078 Review `.github/workflows/deploy.yml` (if exists) for multi-locale build
- [ ] T079 Update deployment script to build all locales: ensure `npm run build` (not `npm run build -- --locale en`)
- [ ] T080 Document deployment URLs in README.md: base URL + `/fr/`, `/ar/`, `/ur/`
- [ ] T081 Test deployment preview (if using GitHub Pages, push to staging branch)

### Phase 2 Validation

- [ ] T082 Verify language switcher appears on all pages
- [ ] T083 Verify no 404 errors when navigating between locales
- [ ] T084 Verify RTL layout correct for Arabic/Urdu (sidebar on left, text right-aligned)
- [ ] T085 Verify ChatWidget UI strings translated (buttons, placeholders)
- [ ] T086 Verify RAG responses still work (API calls unchanged)
- [ ] T087 Take screenshots of all 4 locales for documentation
- [ ] T088 Commit Phase 2 changes with message: "feat: i18n infrastructure - 4 locales with RTL support"

---

## Phase 3: Content Translation (Week 3-4)

**Goal**: Translate high-priority MDX content (intro, Module 1) using hybrid approach (Gemini + human review).

**Deliverable**: Fully translated intro and Module 1 in French, Arabic, and Urdu with human review approval.

**Independent Test Criteria**:
- [ ] Intro page fully translated and displays correctly in all 3 languages
- [ ] Module 1 landing page and Week 01 translated
- [ ] Code blocks remain untranslated (English)
- [ ] MDX frontmatter preserved
- [ ] Native speaker approves at least French translations
- [ ] No broken links or rendering errors in translated pages

### Translation Script (Optional Automation)

- [ ] T089 Create translation script at `scripts/translate_content.py`
- [ ] T090 [P] Implement MDX parsing in `translate_content.py` (extract frontmatter, code blocks, text)
- [ ] T091 [P] Implement Gemini translation function in `translate_content.py` (call Gemini API with translation prompt)
- [ ] T092 [P] Implement MDX reconstruction in `translate_content.py` (preserve code blocks, reassemble file)
- [ ] T093 [P] Add CLI arguments to `translate_content.py` (source file, target language, output path)
- [ ] T094 Test translation script with sample MDX file: `python scripts/translate_content.py book/docs/intro.mdx fr book/i18n/fr/docusaurus-plugin-content-docs/current/intro.mdx`
- [ ] T095 Review Gemini-generated translation for quality (technical terms, fluency)
- [ ] T096 Document translation script usage in `scripts/README.md`

### Translate Priority 1 Content (Intro + Module Landing Pages)

- [ ] T097 Create directory structure: `mkdir -p book/i18n/fr/docusaurus-plugin-content-docs/current/`
- [ ] T098 Create directory structure: `mkdir -p book/i18n/ar/docusaurus-plugin-content-docs/current/`
- [ ] T099 Create directory structure: `mkdir -p book/i18n/ur/docusaurus-plugin-content-docs/current/`
- [ ] T100 [P] Translate `book/docs/intro.mdx` to French at `book/i18n/fr/docusaurus-plugin-content-docs/current/intro.mdx`
- [ ] T101 [P] Translate `book/docs/intro.mdx` to Arabic at `book/i18n/ar/docusaurus-plugin-content-docs/current/intro.mdx`
- [ ] T102 [P] Translate `book/docs/intro.mdx` to Urdu at `book/i18n/ur/docusaurus-plugin-content-docs/current/intro.mdx`
- [ ] T103 [P] Translate Module 1 `_category_.json` to French
- [ ] T104 [P] Translate Module 1 `_category_.json` to Arabic
- [ ] T105 [P] Translate Module 1 `_category_.json` to Urdu
- [ ] T106 Build and verify intro page renders in all locales: `npm run build && npm run serve`

### Translate Priority 2 Content (Module 1, Week 01)

- [ ] T107 [P] Translate `book/docs/module-1-ros2/week-01-intro.mdx` to French
- [ ] T108 [P] Translate `book/docs/module-1-ros2/week-01-intro.mdx` to Arabic
- [ ] T109 [P] Translate `book/docs/module-1-ros2/week-01-intro.mdx` to Urdu
- [ ] T110 Verify code blocks remain in English in all translated files
- [ ] T111 Verify frontmatter (title, sidebar_position) translated correctly
- [ ] T112 Build and test Module 1 Week 01 in all locales

### Translate UI Strings (Navbar, Footer, Custom)

- [ ] T113 [P] Translate navbar labels in `book/i18n/fr/docusaurus-theme-classic/navbar.json`
- [ ] T114 [P] Translate navbar labels in `book/i18n/ar/docusaurus-theme-classic/navbar.json`
- [ ] T115 [P] Translate navbar labels in `book/i18n/ur/docusaurus-theme-classic/navbar.json`
- [ ] T116 [P] Translate footer text in `book/i18n/fr/docusaurus-theme-classic/footer.json`
- [ ] T117 [P] Translate footer text in `book/i18n/ar/docusaurus-theme-classic/footer.json`
- [ ] T118 [P] Translate footer text in `book/i18n/ur/docusaurus-theme-classic/footer.json`
- [ ] T119 [P] Create and translate custom strings in `book/i18n/fr/code.json` (ChatWidget labels)
- [ ] T120 [P] Create and translate custom strings in `book/i18n/ar/code.json`
- [ ] T121 [P] Create and translate custom strings in `book/i18n/ur/code.json`
- [ ] T122 Rebuild and verify all UI strings translated in navbar, footer, ChatWidget

### Human Review (French)

- [ ] T123 Find French-speaking reviewer (native or fluent)
- [ ] T124 Provide review guidelines: technical terms in English, check MDX syntax, verify fluency
- [ ] T125 Reviewer: Check intro.mdx translation quality
- [ ] T126 Reviewer: Check Module 1 Week 01 translation quality
- [ ] T127 Reviewer: Check UI strings (navbar, footer, ChatWidget)
- [ ] T128 Incorporate French review feedback and update translation files
- [ ] T129 Reviewer: Final approval of French translations

### Human Review (Arabic)

- [ ] T130 Find Arabic-speaking reviewer (native or fluent)
- [ ] T131 Provide review guidelines + RTL-specific notes (punctuation, numerals)
- [ ] T132 Reviewer: Check intro.mdx translation quality and RTL rendering
- [ ] T133 Reviewer: Check Module 1 Week 01 translation quality and RTL rendering
- [ ] T134 Reviewer: Check UI strings and RTL layout
- [ ] T135 Incorporate Arabic review feedback and update translation files
- [ ] T136 Fix any RTL-specific CSS issues identified in review
- [ ] T137 Reviewer: Final approval of Arabic translations

### Human Review (Urdu)

- [ ] T138 Find Urdu-speaking reviewer (native or fluent)
- [ ] T139 Provide review guidelines + RTL-specific notes
- [ ] T140 Reviewer: Check intro.mdx translation quality and RTL rendering
- [ ] T141 Reviewer: Check Module 1 Week 01 translation quality and RTL rendering
- [ ] T142 Reviewer: Check UI strings and RTL layout
- [ ] T143 Incorporate Urdu review feedback and update translation files
- [ ] T144 Fix any Urdu font rendering issues (verify Noto Nastaliq Urdu if needed)
- [ ] T145 Reviewer: Final approval of Urdu translations

### Incremental Translation (Remaining Modules - Optional)

- [ ] T146 Translate Module 2 landing page to all 3 languages (French, Arabic, Urdu)
- [ ] T147 Translate Module 2 Week 06 to all 3 languages
- [ ] T148 Translate Module 3 landing page to all 3 languages
- [ ] T149 Translate Module 3 Week 08 to all 3 languages
- [ ] T150 Translate Module 4 landing page to all 3 languages
- [ ] T151 Translate Module 4 Week 11 to all 3 languages
- [ ] T152 Document translation progress in `book/i18n/translation-status.yml`

### Phase 3 Validation

- [ ] T153 Build all locales: `npm run build` - verify no errors
- [ ] T154 Verify intro page displays correctly in all 4 languages
- [ ] T155 Verify Module 1 Week 01 displays correctly in all 4 languages
- [ ] T156 Verify code blocks remain in English in all translated pages
- [ ] T157 Verify no broken links in translated content
- [ ] T158 Verify RTL layout correct for Arabic/Urdu content pages
- [ ] T159 Test navigation between translated pages (sidebar, breadcrumbs)
- [ ] T160 Commit Phase 3 changes with message: "feat: content translation - intro and Module 1 in French, Arabic, Urdu"

---

## Phase 4: Polish & Production (Week 5)

**Goal**: Production-ready quality with SEO, performance optimization, and comprehensive testing.

**Deliverable**: Fully polished multi-language platform ready for public deployment.

**Independent Test Criteria**:
- [ ] Lighthouse scores ≥90 (Performance), ≥95 (Accessibility) for all locales
- [ ] Native speaker approval for all 3 languages
- [ ] Cross-browser testing passed (Chrome, Firefox, Safari)
- [ ] Mobile testing passed (iOS and Android)
- [ ] RAG pipeline regression tests passed
- [ ] Load testing confirms no performance degradation

### SEO & Metadata

- [ ] T161 [P] Add SEO metadata for French locale in `book/docusaurus.config.js` (title, description, og tags)
- [ ] T162 [P] Add SEO metadata for Arabic locale in `book/docusaurus.config.js`
- [ ] T163 [P] Add SEO metadata for Urdu locale in `book/docusaurus.config.js`
- [ ] T164 Configure language-specific sitemaps in `book/docusaurus.config.js` (if plugin supports)
- [ ] T165 Add hreflang links for language alternatives (Docusaurus handles automatically, verify)
- [ ] T166 Test SEO: use Google Search Console or similar tool to verify metadata

### Search Integration (Optional - Algolia DocSearch)

- [ ] T167 Research Algolia DocSearch multi-language support and pricing
- [ ] T168 Apply for Algolia DocSearch (if free tier available for open-source)
- [ ] T169 Configure Algolia in `book/docusaurus.config.js` with locale-aware indices
- [ ] T170 Test search in each locale: verify results are language-specific
- [ ] T171 Document Algolia setup in README.md for future maintenance

### Performance Optimization

- [ ] T172 Analyze bundle size: `npm run build && du -sh build/` - document sizes per locale
- [ ] T173 [P] Implement code splitting for ChatWidget: use React.lazy() in `book/src/components/ChatWidget/index.tsx`
- [ ] T174 [P] Optimize images: compress images in `book/static/img/` using imagemin or similar
- [ ] T175 [P] Add font subsetting for Arabic/Urdu fonts (if custom fonts used)
- [ ] T176 Configure asset caching in deployment (GitHub Pages caches by default, verify)
- [ ] T177 Run Lighthouse performance audit on all locales and document scores
- [ ] T178 Fix any performance issues identified (lazy loading, compression, etc.)

### Accessibility Audit (All Languages)

- [ ] T179 [P] Run axe DevTools on English homepage and 2 chapter pages - fix issues
- [ ] T180 [P] Run axe DevTools on French homepage and 2 chapter pages - fix issues
- [ ] T181 [P] Run axe DevTools on Arabic homepage and 2 chapter pages - fix issues
- [ ] T182 [P] Run axe DevTools on Urdu homepage and 2 chapter pages - fix issues
- [ ] T183 Test keyboard navigation in RTL locales (Tab order correct, focus indicators visible)
- [ ] T184 Test screen reader with Arabic content (verify RTL pronunciation if possible)
- [ ] T185 Document accessibility test results in `specs/001-physical-ai-textbook-platform/accessibility-report.md`

### Cross-Browser Testing

- [ ] T186 [P] Test on Chrome 120+ (Windows/Mac) - all locales, verify rendering and interactions
- [ ] T187 [P] Test on Firefox 120+ (Windows/Mac) - all locales, verify rendering and interactions
- [ ] T188 [P] Test on Safari 17+ (Mac/iOS) - all locales, verify rendering and interactions
- [ ] T189 [P] Test on Edge 120+ (Windows) - all locales, verify rendering and interactions
- [ ] T190 Document any browser-specific issues and workarounds
- [ ] T191 Fix critical cross-browser issues (if any)

### Mobile Device Testing

- [ ] T192 [P] Test on iPhone SE (iOS 16+, Safari) - verify responsive layout, ChatWidget, RTL
- [ ] T193 [P] Test on iPhone 13 (iOS 17+, Safari) - verify responsive layout, ChatWidget, RTL
- [ ] T194 [P] Test on Android (Chrome, Pixel 6 or similar) - verify responsive layout, ChatWidget, RTL
- [ ] T195 [P] Test on iPad (Safari) - verify tablet breakpoints
- [ ] T196 Test ChatWidget mobile UX: full-screen modal works, keyboard doesn't obscure input
- [ ] T197 Document mobile testing results and any issues

### RAG Pipeline Regression Testing

- [ ] T198 Run existing RAG test script: `python test_rag.py` - verify passes
- [ ] T199 Test ChatWidget API call in English locale: open chat, send question, verify response
- [ ] T200 Test ChatWidget API call in French locale: verify API call still succeeds (URL routing)
- [ ] T201 Test ChatWidget API call in Arabic locale: verify API call still succeeds
- [ ] T202 Test ChatWidget API call in Urdu locale: verify API call still succeeds
- [ ] T203 Verify RAG responses are in English (as expected per ADR-002)
- [ ] T204 Add disclaimer to ChatWidget: "AI responds in English only" (if not already present)
- [ ] T205 Document RAG regression test results

### User Acceptance Testing

- [ ] T206 Recruit 3 native speakers (1 French, 1 Arabic, 1 Urdu) for UAT
- [ ] T207 Prepare UAT script: navigate site, read content, use chatbot, switch languages
- [ ] T208 French UAT: tester reviews translations, UI, navigation - document feedback
- [ ] T209 Arabic UAT: tester reviews translations, RTL layout, navigation - document feedback
- [ ] T210 Urdu UAT: tester reviews translations, RTL layout, navigation - document feedback
- [ ] T211 Incorporate UAT feedback: fix critical issues, note nice-to-have improvements
- [ ] T212 Final UAT approval from all 3 testers

### Documentation Updates

- [ ] T213 Update main README.md: add multi-language support section
- [ ] T214 Document how to add new language in `docs/CONTRIBUTING.md` or similar
- [ ] T215 Document translation workflow in `scripts/README.md`
- [ ] T216 Create translation guidelines document at `book/i18n/TRANSLATION_GUIDELINES.md`
- [ ] T217 Update deployment documentation with multi-locale build instructions
- [ ] T218 Add screenshots of all 4 locales to documentation
- [ ] T219 Document known limitations (e.g., AI responses English-only)

### Phase 4 Validation

- [ ] T220 Run full build: `npm run build` - verify all locales build successfully
- [ ] T221 Verify Lighthouse scores meet targets (Performance ≥90, Accessibility ≥95) for all locales
- [ ] T222 Verify all UAT feedback incorporated
- [ ] T223 Verify documentation complete and accurate
- [ ] T224 Smoke test all critical paths in all 4 locales
- [ ] T225 Tag release: `git tag v1.0.0-i18n`
- [ ] T226 Commit Phase 4 changes with message: "feat: production polish - SEO, performance, accessibility, UAT approved"

---

## Final Deployment & Validation

**Goal**: Deploy to production and validate live site.

**Independent Test Criteria**:
- [ ] All 4 locales accessible on production URL
- [ ] No 404 errors or broken links
- [ ] RAG chatbot functional on production
- [ ] SSL certificate valid
- [ ] Analytics configured (if applicable)

### Production Deployment

- [ ] T227 Review production deployment configuration (.github/workflows/deploy.yml or similar)
- [ ] T228 Deploy to GitHub Pages main branch: `git push origin main`
- [ ] T229 Wait for deployment to complete (check GitHub Actions status)
- [ ] T230 Verify production URLs: base URL, `/fr/`, `/ar/`, `/ur/`
- [ ] T231 Test production site in all 4 locales: navigation, content, ChatWidget
- [ ] T232 Verify SSL certificate valid (https://)
- [ ] T233 Test RAG chatbot on production: send questions, verify responses
- [ ] T234 Monitor for errors in browser console on production

### Post-Deployment Monitoring

- [ ] T235 Set up error monitoring (Sentry or similar, if not already configured)
- [ ] T236 Configure analytics for multi-language tracking (Google Analytics or similar)
- [ ] T237 Monitor first 24 hours: check error rates, response times, user feedback
- [ ] T238 Document any production issues and resolutions
- [ ] T239 Share production URLs with stakeholders for review

### Final Sign-Off

- [ ] T240 Product owner approval of all 4 locales
- [ ] T241 Stakeholder demo: present multi-language features and UI improvements
- [ ] T242 Create project retrospective document: what went well, what to improve
- [ ] T243 Archive project artifacts: PHR, ADRs, test results, screenshots
- [ ] T244 Close all related GitHub issues/tasks
- [ ] T245 Celebrate successful delivery! 🎉

---

## Dependencies & Execution Order

### Critical Path (Must Complete in Order)

1. **Phase 1 → Phase 2**: UI/UX must be solid before adding i18n complexity
2. **Phase 2 → Phase 3**: i18n infrastructure must exist before translating content
3. **Phase 3 → Phase 4**: Content must be translated before final polish and UAT

### Parallel Opportunities

Within each phase, tasks marked with `[P]` can be executed in parallel:

**Phase 1 Parallel Groups**:
- Group A: T004, T005, T006 (CSS files - different sections)
- Group B: T012, T013 (Prism installation + config)
- Group C: T017, T018, T019, T020 (ChatWidget CSS - different classes)
- Group D: T025, T026 (Accessibility - different checks)
- Group E: T029, T030, T031, T032, T033 (Browser/device testing - independent)

**Phase 2 Parallel Groups**:
- Group A: T042, T043, T044, T045 (Locale configs - independent)
- Group B: T054, T055, T056, T057 (RTL CSS - different selectors)
- Group C: T061, T062, T063, T064 (Translation strings - per language)
- Group D: T073, T074, T075, T076 (Locale testing - independent)

**Phase 3 Parallel Groups**:
- Group A: T100, T101, T102 (Intro translation - per language)
- Group B: T103, T104, T105 (Module 1 category - per language)
- Group C: T107, T108, T109 (Week 01 translation - per language)
- Group D: T113, T114, T115 (Navbar translation - per language)
- Group E: T116, T117, T118 (Footer translation - per language)
- Group F: T119, T120, T121 (Custom strings - per language)

**Phase 4 Parallel Groups**:
- Group A: T161, T162, T163 (SEO metadata - per language)
- Group B: T173, T174, T175 (Performance optimization - independent)
- Group C: T179, T180, T181, T182 (Accessibility audits - per language)
- Group D: T186, T187, T188, T189 (Cross-browser testing - independent)
- Group E: T192, T193, T194, T195 (Mobile testing - independent)

### Blocked Dependencies

- T089-T096 (Translation script) blocks T100-T109 if using automation
- T123-T129 (French review) blocks French content finalization
- T130-T137 (Arabic review) blocks Arabic content finalization
- T138-T145 (Urdu review) blocks Urdu content finalization
- T206-T212 (UAT) blocks final deployment approval

---

## MVP Scope Recommendation

**Minimum Viable Product**: Phase 1 + Phase 2 + Partial Phase 3

**MVP Deliverables**:
- ✅ Modern UI/UX with accessibility (Phase 1)
- ✅ 4-language infrastructure working (Phase 2)
- ✅ Intro + Module 1 Week 01 translated to French only (subset of Phase 3)
- ✅ Basic testing and validation

**MVP excludes**:
- Arabic and Urdu translations (add in iteration 2)
- Full content translation (incremental)
- Advanced features (Algolia search, font subsetting)
- Extensive UAT

**Rationale**: MVP proves multi-language concept, shows UI improvements, and can be deployed quickly. Arabic/Urdu RTL support adds complexity that can be iterated on after French validation.

---

## Rollback Strategy

If critical issues arise during or after deployment:

1. **Immediate Rollback**: `git revert <commit-hash>` and redeploy
2. **English-Only Fallback**: Build with `npm run build -- --locale en` and deploy single locale
3. **Phase Rollback**: Revert to previous phase tag (e.g., `git checkout v0.1.0-phase2`)
4. **Fix Forward**: Create hotfix branch, fix issue, test, merge, redeploy

**Rollback Triggers**:
- RAG pipeline broken (API errors, no responses)
- >50% increase in 404 errors or page load errors
- Critical accessibility failures (WCAG violations blocking users)
- RTL layout completely broken (content unreadable)

---

## Testing & Validation Summary

| Phase | Testing Focus | Acceptance Criteria |
|-------|--------------|---------------------|
| **Phase 1** | UI/UX, Accessibility, Responsive | Lighthouse ≥90/95, Cross-browser, Mobile |
| **Phase 2** | i18n Infrastructure, RTL | All locales build, Language switcher works, RTL correct |
| **Phase 3** | Translation Quality, Content Rendering | Native speaker approval, Code blocks untranslated |
| **Phase 4** | Production Readiness, Performance | UAT approved, Performance optimized, Documentation complete |

---

## Task Count Summary

- **Phase 1 (UI/UX)**: 39 tasks (T001-T039)
- **Phase 2 (i18n Infra)**: 49 tasks (T040-T088)
- **Phase 3 (Translation)**: 72 tasks (T089-T160)
- **Phase 4 (Polish)**: 66 tasks (T161-T226)
- **Deployment**: 19 tasks (T227-T245)
- **Total**: 245 tasks

**Parallel Opportunities**: ~80 tasks marked with `[P]` (33% can run in parallel)

**Estimated Timeline**:
- Phase 1: 1 week (40 hours)
- Phase 2: 1 week (40 hours)
- Phase 3: 2 weeks (80 hours)
- Phase 4: 1 week (40 hours)
- **Total**: 5 weeks (200 hours) for full implementation

**MVP Timeline**: 2 weeks (Phase 1 + Phase 2 + French-only translation)

---

## Implementation Strategy

### Week-by-Week Plan

**Week 1**: UI/UX Foundation
- Focus: T001-T039 (Phase 1)
- Deliverable: Enhanced UI, zero i18n
- Validation: Lighthouse scores, RAG still works

**Week 2**: i18n Infrastructure
- Focus: T040-T088 (Phase 2)
- Deliverable: 4 locales enabled, language switcher
- Validation: All locales build, RTL works

**Week 3**: High-Priority Translation
- Focus: T089-T122 (Intro + Module 1 + UI strings)
- Deliverable: Priority content translated (3 languages)
- Validation: Content renders correctly

**Week 4**: Review & Incremental Translation
- Focus: T123-T160 (Human reviews + optional modules)
- Deliverable: Reviewed translations, optional modules
- Validation: Native speaker approval

**Week 5**: Polish & Production
- Focus: T161-T245 (SEO, performance, UAT, deployment)
- Deliverable: Production-ready multi-language site
- Validation: UAT approved, deployed successfully

### Risk Mitigation During Implementation

- **Daily**: Commit after each completed task
- **End of Each Phase**: Full build + smoke test + RAG verification
- **Before Phase Transitions**: Tag release (e.g., `v0.1.0-phase1`)
- **If Blocked**: Document blocker, continue with parallel tasks, escalate if >1 day

---

## Success Metrics

### Technical Metrics

- [ ] **Build Success**: All 4 locales build without errors
- [ ] **Performance**: Lighthouse Performance ≥90 for all locales
- [ ] **Accessibility**: Lighthouse Accessibility ≥95 for all locales
- [ ] **Bundle Size**: Total bundle <500KB per locale
- [ ] **Zero Regressions**: RAG pipeline test_rag.py passes after all changes

### User Experience Metrics

- [ ] **Translation Quality**: Native speaker approval for all 3 languages
- [ ] **Navigation**: Users can switch languages and find content without confusion
- [ ] **RTL Usability**: Arabic/Urdu users report layout is natural and readable
- [ ] **ChatWidget UX**: Users can successfully ask questions in all locales
- [ ] **Mobile UX**: Mobile users report positive experience across languages

### Project Metrics

- [ ] **On-Time Delivery**: Complete within 5-week timeline (or 2 weeks for MVP)
- [ ] **Code Quality**: No critical linting errors, all tests pass
- [ ] **Documentation**: Complete setup, translation, and maintenance docs
- [ ] **Stakeholder Satisfaction**: Product owner and native speakers approve

---

## Notes

**ADR References**:
- [ADR-001](./ui-i18n-enhancement-plan.md#adr-001-use-docusaurus-built-in-i18n-instead-of-runtime-translation): Use Docusaurus built-in i18n
- [ADR-002](./ui-i18n-enhancement-plan.md#adr-002-keep-api-responses-english-only-for-now): Keep API responses English-only
- [ADR-003](./ui-i18n-enhancement-plan.md#adr-003-use-hybrid-translation-approach-gemini--human-review): Hybrid translation approach

**Related Documents**:
- [ui-i18n-enhancement-plan.md](./ui-i18n-enhancement-plan.md) - Full architectural plan
- [spec.md](./spec.md) - Feature specification
- [plan.md](./plan.md) - Original architecture plan

**Translation Guidelines**: See [Appendix 14.1](./ui-i18n-enhancement-plan.md#141-translation-guidelines-for-reviewers) in ui-i18n-enhancement-plan.md

---

**Ready to implement!** Each task is specific, has clear file paths, and can be executed by an LLM or human developer. Start with Phase 1 for quick wins, or jump to MVP scope for fastest time-to-value.
