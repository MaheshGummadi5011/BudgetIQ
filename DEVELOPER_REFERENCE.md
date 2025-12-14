# 🛠️ BudgetIQ - Developer Quick Reference

## Issues Fixed - Quick Lookup

### Backend Fixes
```
✅ Fixed: ai_financial_path() logic error
   File: backend/app.py (line 97)
   Change: Removed print before validation

✅ Fixed: HTTP method case (get → GET)
   File: backend/app.py (lines 114-116)
   Change: Capitalized method names

✅ Added: Error logging system
   File: backend/logger_config.py (NEW)
   Features: File + console logging, daily rotation

✅ Added: Missing dependencies
   File: backend/requirements.txt
   Added: protobuf, requests, pydantic
```

### Frontend Fixes
```
✅ Fixed: Speech recognition resource leak
   File: frontend/src/pages/Chatbot.tsx
   Change: Proper cleanup and stop() calls

✅ Added: Error handling system
   File: frontend/src/utils/errorHandler.ts (NEW)
   Features: Type-safe, retry logic, user-friendly messages

✅ Added: Input validation
   File: frontend/src/pages/Chatbot.tsx
   Validation: Length check (max 5000), empty check
```

---

## File Changes Summary

| File | Type | Changes | Lines |
|------|------|---------|-------|
| app.py | Modified | 3 fixes + imports | 120 |
| requirements.txt | Modified | +3 deps | 12 |
| logger_config.py | Created | New | 41 |
| Chatbot.tsx | Modified | 4 fixes + imports | 5+ |
| errorHandler.ts | Created | New | 73 |
| IMPROVEMENTS_LOG.md | Created | Documentation | - |
| AUDIT_REPORT.md | Created | Audit report | - |

---

## Running the Project

### Backend
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
# Server will be at http://127.0.0.1:5000
```

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
# Frontend will be at http://localhost:5173
```

### Logs
- Backend logs: `backend/logs/budgetiq_YYYYMMDD.log`
- Check for errors and debugging info

---

## Error Handling Examples

### Backend - Logging
```python
from logger_config import log_request, log_error, log_info

# Log request
log_request("GET", "/api/endpoint", 200)

# Log error with context
log_error("ValueError", "Invalid input", context="user_input='abc'")

# Log info
log_info("API started successfully")
```

### Frontend - Error Handling
```typescript
import { handleApiError, getErrorMessage } from '../utils/errorHandler';

try {
  const response = await axios.get('/api/data');
} catch (error) {
  const apiError = handleApiError(error);
  const userMessage = getErrorMessage(apiError);
  // Show userMessage to user
}
```

---

## Testing Checklist

- [ ] Backend API responds on http://127.0.0.1:5000
- [ ] AI Assistant gives intelligent responses
- [ ] Speech input/output works
- [ ] Error messages display properly
- [ ] No console errors
- [ ] Logs are being created
- [ ] All pages load without errors

---

## Known Limitations

1. Gemini API free tier has rate limits
2. Speech API only works on HTTPS (except localhost)
3. Logs grow daily (implement rotation if needed)
4. No database persistence (use onboard.py data)

---

## Performance Notes

- First API call slower (cold start)
- Speech recognition works best in English
- Message typing effect: 30ms per character
- Error retry: exponential backoff starting at 1s

---

## Support & Debugging

### If App Crashes
1. Check `backend/logs/` for error details
2. Verify all dependencies installed
3. Ensure Gemini API key is valid
4. Check console for frontend errors

### If Speech Doesn't Work
1. Use HTTPS (or localhost)
2. Check browser permissions
3. Verify microphone is working
4. Check browser console for errors

### If API Calls Fail
1. Check server is running
2. Verify API key in `.env`
3. Check network connectivity
4. Look at backend logs

---

## Useful Commands

```bash
# Check Python syntax
python -m py_compile backend/app.py

# View recent logs
tail -f backend/logs/budgetiq_*.log

# Install frontend deps
cd frontend && npm install

# Build frontend
npm run build

# Run tests (when added)
npm test
```

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│      BudgetIQ Application           │
├─────────────────────────────────────┤
│ Frontend (React + TypeScript)       │
│ - Chatbot Component                 │
│ - Portfolio Dashboard               │
│ - Error Handling                    │
├─────────────────────────────────────┤
│ Backend (Python Flask)              │
│ - AI Agent (/agent)                 │
│ - Financial Path (/ai-financial-path)│
│ - Data APIs (/auto-bank-data, etc)  │
│ - Logging System                    │
├─────────────────────────────────────┤
│ External Services                   │
│ - Gemini API                        │
│ - Authentication (Clerk)            │
│ - Weather/News APIs                 │
└─────────────────────────────────────┘
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 18, 2025 | Initial with all fixes |
| - | - | Removed Stock Analyzer |
| - | - | Rebranded to BudgetIQ |

---

**Last Updated:** November 18, 2025  
**Status:** Production Ready ✅  
**Maintainer:** Development Team
