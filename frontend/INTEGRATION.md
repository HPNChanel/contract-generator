# Frontend-Backend Integration Guide

## Overview

This document explains how the React frontend integrates with the FastAPI backend for the Contract Generator application.

## Architecture

```
Frontend (React)    →    Backend (FastAPI)
http://localhost:5173    http://localhost:8000
```

## API Integration Features

### 1. CORS Configuration
The backend is configured with CORS middleware to allow requests from the frontend:

```python
# In main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Error Handling
Comprehensive error handling for different types of failures:

- **Network Errors**: CORS issues, server not running
- **Server Errors**: 4xx/5xx HTTP status codes
- **Validation Errors**: Form validation and API validation

### 3. Loading States
- Loading spinner during contract generation
- Loading toast notifications
- Disabled form submission during processing

### 4. Toast Notifications
Using `react-hot-toast` for user feedback:
- Success: "Contract generated successfully!"
- Error: Detailed error messages with troubleshooting
- Loading: "Generating contract..." with progress indication

### 5. Local Storage
Recent contract IDs are stored in localStorage:
- Automatically saves the last 10 contract IDs
- Displays recent contracts in the sidebar
- Persists across browser sessions

## API Endpoints Used

### POST /api/v1/contracts
**Purpose**: Create new contract with PDF generation

**Request**:
```json
{
  "contract_type": "Service Agreement",
  "party_a": {
    "name": "Company A",
    "email": "contact@companya.com",
    "address": "123 Business St"
  },
  "party_b": {
    "name": "Company B", 
    "email": "contact@companyb.com",
    "address": "456 Client Ave"
  },
  "terms": "Contract terms and conditions...",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "additional_clauses": ["Clause 1", "Clause 2"]
}
```

**Response**:
```json
{
  "message": "Contract created successfully with HTML preview and PDF generated",
  "contract_id": 1,
  "contract_data": {
    "id": 1,
    "contract_type": "Service Agreement",
    "party_a": {"name": "Company A", "email": "contact@companya.com"},
    "party_b": {"name": "Company B", "email": "contact@companyb.com"},
    "terms": "Contract terms...",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "additional_clauses": ["Clause 1", "Clause 2"],
    "created_at": "2024-01-27T14:30:22.123456",
    "updated_at": "2024-01-27T14:30:22.123456"
  },
  "preview_html": "<html>...complete HTML content...</html>",
  "pdf_info": {
    "pdf_path": "generated_pdfs/contract_1_20240127_143022.pdf",
    "filename": "contract_1_20240127_143022.pdf",
    "download_url": "/api/v1/contracts/download/contract_1_20240127_143022.pdf"
  }
}
```

### GET /api/v1/contracts/download/{filename}
**Purpose**: Download generated PDF files

**Response**: Binary PDF file with proper headers

### GET /api/v1/health
**Purpose**: Check backend server status

**Response**:
```json
{
  "status": "healthy"
}
```

## Connection Testing

The frontend automatically tests the backend connection on startup:

1. **On App Load**: Calls `/health` endpoint
2. **Status Indicator**: Shows connection status in header
3. **Error Handling**: Displays toast if backend is unreachable

## Error Scenarios & Handling

### 1. Backend Not Running
- **Detection**: Request timeout or connection refused
- **User Feedback**: Toast notification with setup instructions
- **Status**: Red indicator showing "API Disconnected"

### 2. CORS Issues
- **Detection**: OPTIONS request blocked
- **Resolution**: CORS middleware properly configured
- **Fallback**: Clear error message to user

### 3. Validation Errors
- **Backend Validation**: Pydantic model validation
- **Frontend Validation**: Zod schema validation
- **Double Protection**: Client and server-side validation

### 4. PDF Generation Failures
- **WeasyPrint Issues**: Automatic fallback to reportlab
- **File System Errors**: Proper error messages
- **Recovery**: User can retry with same data

## Data Flow

1. **Form Submission**:
   ```
   User fills form → Zod validation → API call → Loading state
   ```

2. **Backend Processing**:
   ```
   Receive data → Validate → Save to DB → Generate HTML → Create PDF → Return response
   ```

3. **Frontend Response**:
   ```
   Receive response → Update UI → Show preview → Enable download → Save to localStorage
   ```

## Development Setup

### Start Backend Server
```bash
cd quick_contract
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Server
```bash
cd frontend
npm run dev
```

### Verify Integration
1. Check status indicator in header (should be green)
2. Fill out contract form
3. Submit and verify:
   - Loading spinner appears
   - Success toast shows
   - Preview appears in right panel
   - PDF download works
   - Contract ID saved to localStorage

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure backend CORS middleware is configured
   - Check frontend API base URL is correct
   - Restart backend server after CORS changes

2. **Connection Refused**:
   - Verify backend server is running on port 8000
   - Check firewall settings
   - Ensure no other service is using port 8000

3. **PDF Download Issues**:
   - Check generated_pdfs directory exists
   - Verify file permissions
   - Check browser popup blocker settings

4. **Form Validation**:
   - Check browser console for validation errors
   - Verify all required fields are filled
   - Check date format (YYYY-MM-DD)

### Debug Mode

Enable additional logging by:

1. **Frontend**: Open browser dev tools, check Network tab
2. **Backend**: Check FastAPI server logs in terminal
3. **Database**: Check contracts.db file is created

## Production Considerations

1. **Environment Variables**:
   - Configure API base URL for production
   - Set proper CORS origins
   - Use secure connection (HTTPS)

2. **Error Monitoring**:
   - Implement error tracking (Sentry)
   - Log API failures
   - Monitor PDF generation success rates

3. **Performance**:
   - Implement request caching
   - Optimize PDF generation
   - Add request timeout handling

4. **Security**:
   - Validate file downloads
   - Sanitize HTML content
   - Rate limit API requests 