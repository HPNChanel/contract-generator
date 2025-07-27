# Quick Contract API

A FastAPI application for managing contracts with SQLite database and SQLAlchemy ORM.

## Project Structure

```
quick_contract/
├── main.py              # FastAPI app initialization
├── database.py          # SQLAlchemy database configuration
├── models.py           # Database models
├── requirements.txt    # Project dependencies
├── routes/
│   └── contract.py     # Contract CRUD endpoints
├── templates/
│   └── contract_template.html  # Jinja2 HTML template
├── generated_pdfs/     # Auto-created directory for PDF files
└── utils/
    ├── __init__.py     # Utils package
    ├── template_renderer.py   # Jinja2 template rendering functions
    └── pdf_generator.py       # WeasyPrint PDF generation functions
```

## Features

- **Contract Model** with the following fields:
  - `id`: Integer (primary key, auto increment)
  - `contract_type`: String
  - `data`: JSON data stored as text
  - `created_at`: DateTime (default now)
  - `updated_at`: DateTime (auto update on change)

- **RESTful API endpoints**:
  - `POST /api/v1/contracts` - Create contract with DB storage, HTML preview, and PDF generation
  - `GET /api/v1/contracts` - List all contracts with pagination
  - `GET /api/v1/contracts/{id}` - Get specific contract with full data and PDF status
  - `DELETE /api/v1/contracts/{id}` - Delete contract and optionally associated PDF files
  - `GET /api/v1/contracts/{id}/render` - Render contract as HTML using Jinja2 template
  - `GET /api/v1/contracts/{id}/pdf` - Generate PDF from existing contract
  - `GET /api/v1/contracts/download/{filename}` - Download generated PDF file
  - `GET /api/v1/contracts/sample-data` - Get sample contract data for testing

- **Jinja2 Template Engine** for generating HTML contracts:
  - Professional HTML contract templates with styling
  - Template variables: `{{ contract_type }}`, `{{ party_a.name }}`, `{{ party_b.name }}`, `{{ terms }}`, `{{ start_date }}`, `{{ end_date }}`
  - Support for optional fields and additional clauses
  - Auto-escaping for security

- **PDF Generation** with automatic fallback:
  - Primary: WeasyPrint for high-quality HTML-to-PDF conversion
  - Fallback: reportlab for Windows compatibility (automatic)
  - Automatic file management in `generated_pdfs/` directory
  - Custom filenames with timestamp-based naming
  - A4 page formatting with proper margins and styling
  - File download, listing, and cleanup capabilities

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note for Windows users**: If you encounter WeasyPrint installation issues (GTK dependencies), don't worry! The application automatically falls back to using reportlab for PDF generation, which works perfectly on Windows without additional dependencies.

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## Usage Examples

### Create a Contract (with HTML + PDF generation)
```bash
curl -X POST "http://localhost:8000/api/v1/contracts" \
     -H "Content-Type: application/json" \
     -d '{
       "contract_type": "Service Agreement",
       "party_a": {
         "name": "ABC Company Inc.",
         "address": "123 Business St, City, State 12345",
         "email": "contact@abccompany.com",
         "phone": "+1 (555) 123-4567"
       },
       "party_b": {
         "name": "John Doe",
         "address": "456 Client Ave, Town, State 67890",
         "email": "john.doe@email.com",
         "phone": "+1 (555) 987-6543"
       },
       "terms": "This agreement establishes the terms for providing consulting services.",
       "start_date": "2024-01-01",
       "end_date": "2024-12-31",
       "additional_clauses": [
         "Payment terms are Net 30 days",
         "Either party may terminate with 30 days notice"
       ],
       "custom_pdf_filename": "my_contract.pdf"
     }'
```

### Get All Contracts
```bash
curl -X GET "http://localhost:8000/api/v1/contracts?skip=0&limit=10"
```

### Get a Specific Contract
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/1"
```

### Delete a Contract (with PDF cleanup)
```bash
curl -X DELETE "http://localhost:8000/api/v1/contracts/1?delete_pdf=true"
```

## Template Engine Usage

### Get Sample Template Data
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/sample-data"
```

### Preview Contract HTML (without saving)
```bash
curl -X POST "http://localhost:8000/api/v1/contracts/render" \
     -H "Content-Type: application/json" \
     -d '{
       "contract_type": "Service Agreement",
       "party_a": {
         "name": "ABC Company Inc.",
         "address": "123 Business St, City, State 12345",
         "email": "contact@abccompany.com"
       },
       "party_b": {
         "name": "John Doe",
         "address": "456 Client Ave, Town, State 67890",
         "email": "john.doe@email.com"
       },
       "terms": "This agreement establishes the terms for providing consulting services.",
       "start_date": "2024-01-01",
       "end_date": "2024-12-31"
     }'
```

### Render Existing Contract as HTML
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/1/render"
```

## PDF Generation Usage

### Generate PDF from Existing Contract
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/1/pdf?custom_filename=my_contract.pdf"
```

### Generate PDF from Contract Data (without saving)
```bash
curl -X POST "http://localhost:8000/api/v1/contracts/generate-pdf" \
     -H "Content-Type: application/json" \
     -d '{
       "contract_type": "Service Agreement",
       "party_a": {
         "name": "ABC Company Inc.",
         "address": "123 Business St, City, State 12345",
         "email": "contact@abccompany.com"
       },
       "party_b": {
         "name": "John Doe",
         "address": "456 Client Ave, Town, State 67890",
         "email": "john.doe@email.com"
       },
       "terms": "This agreement establishes the terms for providing consulting services.",
       "start_date": "2024-01-01",
       "end_date": "2024-12-31"
     }'
```

### Download PDF File
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/download/contract_20241127_143022.pdf" \
     --output "downloaded_contract.pdf"
```

### List Generated PDF Files
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/pdfs"
```

### Delete Specific PDF File
```bash
curl -X DELETE "http://localhost:8000/api/v1/contracts/pdfs/contract_20241127_143022.pdf"
```

### Cleanup Old PDF Files (older than 30 days)
```bash
curl -X POST "http://localhost:8000/api/v1/contracts/pdfs/cleanup?days_old=30"
```

## Database

The application uses SQLite as the default database. The database file (`contracts.db`) will be created automatically when you first run the application.

Tables are automatically created using `Base.metadata.create_all()` when the app starts. 