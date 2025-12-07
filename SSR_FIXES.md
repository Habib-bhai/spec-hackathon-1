# SSR (Server-Side Rendering) Fixes

## Issues Encountered

### 1. **ChatWidget Crash During SSR**
**Error**: `ReferenceError: window is not defined` / `document is not defined`

**Root Cause**: 
- Docusaurus performs Server-Side Rendering (SSR) during build and development
- The `ChatWidget` component uses browser-specific APIs (`window.getSelection()`, `document.addEventListener()`)
- These APIs don't exist in the Node.js server environment

### 2. **Process Environment Variable Error**
**Error**: `ReferenceError: process is not defined`

**Root Cause**:
- `process.env` is a Node.js API, not available in browser JavaScript
- Cannot use `process.env.REACT_APP_API_URL` directly in browser-rendered code

## Solutions Implemented

### Fix 1: Wrap ChatWidget with BrowserOnly Component

**File**: `book/src/theme/Root.tsx`

**Before**:
```tsx
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatWidget apiUrl={process.env.REACT_APP_API_URL || 'http://localhost:8000'} />
    </>
  );
}
```

**After**:
```tsx
import BrowserOnly from '@docusaurus/BrowserOnly';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function Root({children}) {
  const {siteConfig} = useDocusaurusContext();
  const apiUrl = (siteConfig.customFields?.apiUrl as string) || 'http://localhost:8000';
  
  return (
    <>
      {children}
      <BrowserOnly>
        {() => <ChatWidget apiUrl={apiUrl} />}
      </BrowserOnly>
    </>
  );
}
```

**Why this works**:
- `<BrowserOnly>` only renders its children in the browser, not during SSR
- This prevents server-side execution of browser-specific code

### Fix 2: Use Docusaurus Custom Fields for Configuration

**File**: `book/docusaurus.config.js`

**Added**:
```javascript
const config = {
  // ... other config
  
  customFields: {
    apiUrl: process.env.API_URL || 'http://localhost:8000',
  },
  
  // ... rest of config
};
```

**Why this works**:
- Docusaurus processes `docusaurus.config.js` at build time (Node.js environment)
- `process.env` is available in config files
- Custom fields are accessible via `useDocusaurusContext()` hook in components
- Values are safely passed to the browser context

### Fix 3: Add Browser Check in ChatWidget

**File**: `book/src/components/ChatWidget/index.tsx`

**Added safety check**:
```tsx
useEffect(() => {
  // Only run in browser environment
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return;
  }

  const handleSelection = () => {
    const selection = window.getSelection();
    // ... rest of code
  };

  document.addEventListener('mouseup', handleSelection);
  return () => document.removeEventListener('mouseup', handleSelection);
}, []);
```

**Why this works**:
- Double-checks that browser APIs are available before using them
- Gracefully handles edge cases where SSR might occur
- Defense-in-depth approach to prevent crashes

## How SSR Works in Docusaurus

```
┌─────────────────────────────────────────────────────────────┐
│                    Docusaurus Build Process                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Node.js Server (SSR)                                    │
│     ├─ Reads docusaurus.config.js                          │
│     ├─ Processes MDX/Markdown files                        │
│     ├─ Renders React components to HTML                    │
│     └─ ❌ No window/document APIs available                │
│                                                              │
│  2. Browser Hydration                                       │
│     ├─ Loads pre-rendered HTML                             │
│     ├─ Initializes React                                   │
│     ├─ <BrowserOnly> components render now                 │
│     └─ ✅ window/document APIs available                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Testing the Fixes

1. **Start the development server**:
   ```bash
   cd book
   npm start
   ```

2. **Expected behavior**:
   - ✅ No crash on page load
   - ✅ Page renders successfully
   - ✅ Chat widget (💬) appears in bottom-right corner
   - ✅ Widget only renders after page is fully loaded

3. **Verify in browser console**:
   - Open DevTools (F12)
   - Should see no errors about `window` or `process`
   - Chat widget should be interactive

## Configuration for Production

To change the API URL for production deployment:

**Option 1: Environment variable (recommended)**
```bash
API_URL=https://your-api.com npm run build
```

**Option 2: Edit docusaurus.config.js**
```javascript
customFields: {
  apiUrl: 'https://your-production-api.com',
}
```

## Common SSR Issues in React

| Issue | Symptom | Solution |
|-------|---------|----------|
| Using `window` | `ReferenceError: window is not defined` | Wrap with `<BrowserOnly>` or check `typeof window !== 'undefined'` |
| Using `document` | `ReferenceError: document is not defined` | Same as above |
| Using `localStorage` | `ReferenceError: localStorage is not defined` | Check availability before use |
| Using `process.env` in browser code | `ReferenceError: process is not defined` | Use custom fields or build-time constants |
| Event listeners | Components not interactive | Ensure proper hydration with `useEffect` |

## Related Docusaurus Documentation

- [BrowserOnly API](https://docusaurus.io/docs/docusaurus-core#browseronly)
- [Custom Fields](https://docusaurus.io/docs/api/docusaurus-config#customFields)
- [useDocusaurusContext](https://docusaurus.io/docs/docusaurus-core#usedocusauruscontext)

---

**Status**: ✅ All SSR issues resolved  
**Last Updated**: December 7, 2025
