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
└── utils/
    └── __init__.py     # Utils package
```

## Features

- **Contract Model** with the following fields:
  - `id`: Integer (primary key, auto increment)
  - `contract_type`: String
  - `data`: JSON data stored as text
  - `created_at`: DateTime (default now)
  - `updated_at`: DateTime (auto update on change)

- **RESTful API endpoints**:
  - `POST /api/v1/contracts/` - Create a new contract
  - `GET /api/v1/contracts/` - Get all contracts (with pagination)
  - `GET /api/v1/contracts/{contract_id}` - Get a specific contract
  - `PUT /api/v1/contracts/{contract_id}` - Update a contract
  - `DELETE /api/v1/contracts/{contract_id}` - Delete a contract

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

### Create a Contract
```bash
curl -X POST "http://localhost:8000/api/v1/contracts/" \
     -H "Content-Type: application/json" \
     -d '{
       "contract_type": "service_agreement",
       "data": {
         "client_name": "John Doe",
         "service": "Web Development",
         "duration": "3 months"
       }
     }'
```

### Get All Contracts
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/"
```

### Get a Specific Contract
```bash
curl -X GET "http://localhost:8000/api/v1/contracts/1"
```

### Update a Contract
```bash
curl -X PUT "http://localhost:8000/api/v1/contracts/1" \
     -H "Content-Type: application/json" \
     -d '{
       "contract_type": "updated_service_agreement",
       "data": {
         "client_name": "John Doe",
         "service": "Full Stack Development",
         "duration": "6 months"
       }
     }'
```

### Delete a Contract
```bash
curl -X DELETE "http://localhost:8000/api/v1/contracts/1"
```

## Database

The application uses SQLite as the default database. The database file (`contracts.db`) will be created automatically when you first run the application.

Tables are automatically created using `Base.metadata.create_all()` when the app starts. 