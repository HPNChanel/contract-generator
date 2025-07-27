from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import json
import os

from database import get_db
from models import Contract
from utils.template_renderer import render_contract, validate_contract_data, get_sample_contract_data
from utils.pdf_generator import (
    generate_pdf_from_html, 
    generate_pdf_from_template_data, 
    get_generated_pdfs_list,
    delete_pdf_file,
    cleanup_old_pdfs
)

router = APIRouter()

# ===== PYDANTIC MODELS =====

class PartyInfo(BaseModel):
    """Model for party information (party_a or party_b)"""
    name: str = Field(..., min_length=1, description="Full name of the party")
    address: Optional[str] = Field(None, description="Address of the party")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")

class ContractCreateRequest(BaseModel):
    """Model for creating a new contract"""
    contract_type: str = Field(..., min_length=1, description="Type of contract")
    party_a: PartyInfo = Field(..., description="Information for Party A")
    party_b: PartyInfo = Field(..., description="Information for Party B")
    terms: str = Field(..., min_length=1, description="Contract terms and conditions")
    start_date: str = Field(..., description="Contract start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="Contract end date (YYYY-MM-DD)")
    additional_clauses: Optional[List[str]] = Field(None, description="Additional contract clauses")
    custom_pdf_filename: Optional[str] = Field(None, description="Custom filename for generated PDF")

class ContractResponse(BaseModel):
    """Model for contract response data"""
    id: int
    contract_type: str
    party_a: PartyInfo
    party_b: PartyInfo
    terms: str
    start_date: str
    end_date: str
    additional_clauses: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContractCreateResponse(BaseModel):
    """Model for successful contract creation response"""
    message: str
    contract_id: int
    contract_data: ContractResponse
    preview_html: str
    pdf_info: Dict[str, Any]

class ContractListItem(BaseModel):
    """Model for contract list items"""
    id: int
    contract_type: str
    party_a_name: str
    party_b_name: str
    created_at: datetime

class ContractListResponse(BaseModel):
    """Model for contracts list response"""
    message: str
    total_contracts: int
    contracts: List[ContractListItem]

class ContractDetailResponse(BaseModel):
    """Model for detailed contract response"""
    contract: ContractResponse
    pdf_file_path: Optional[str]
    pdf_exists: bool
    download_url: Optional[str]

class ContractDeleteResponse(BaseModel):
    """Model for contract deletion response"""
    message: str
    contract_id: int
    pdf_deleted: bool

# ===== HELPER FUNCTIONS =====

def _contract_data_to_template_format(contract_data: dict) -> dict:
    """Convert database contract data to template format"""
    return {
        "contract_type": contract_data.get("contract_type"),
        "party_a": contract_data.get("party_a", {}),
        "party_b": contract_data.get("party_b", {}),
        "terms": contract_data.get("terms"),
        "start_date": contract_data.get("start_date"),
        "end_date": contract_data.get("end_date"),
        "additional_clauses": contract_data.get("additional_clauses", [])
    }

def _parse_contract_data(db_contract: Contract) -> dict:
    """Parse contract data from database"""
    try:
        return json.loads(db_contract.data) if db_contract.data else {}
    except json.JSONDecodeError:
        return {}

def _create_contract_response(db_contract: Contract) -> ContractResponse:
    """Create ContractResponse from database contract"""
    contract_data = _parse_contract_data(db_contract)
    
    return ContractResponse(
        id=db_contract.id,
        contract_type=db_contract.contract_type,
        party_a=PartyInfo(**contract_data.get("party_a", {})),
        party_b=PartyInfo(**contract_data.get("party_b", {})),
        terms=contract_data.get("terms", ""),
        start_date=contract_data.get("start_date", ""),
        end_date=contract_data.get("end_date", ""),
        additional_clauses=contract_data.get("additional_clauses"),
        created_at=db_contract.created_at,
        updated_at=db_contract.updated_at
    )

# ===== MAIN ENDPOINTS =====

@router.post("/contracts", response_model=ContractCreateResponse)
def create_contract(contract_request: ContractCreateRequest, db: Session = Depends(get_db)):
    """
    Create a new contract with complete workflow:
    1. Store contract data in database
    2. Generate HTML preview using Jinja2 template
    3. Generate PDF file
    4. Return contract ID, preview HTML, and PDF download path
    """
    try:
        # Prepare contract data for storage
        contract_data = {
            "contract_type": contract_request.contract_type,
            "party_a": contract_request.party_a.dict(),
            "party_b": contract_request.party_b.dict(),
            "terms": contract_request.terms,
            "start_date": contract_request.start_date,
            "end_date": contract_request.end_date,
            "additional_clauses": contract_request.additional_clauses or []
        }
        
        # Validate contract data for template rendering
        validate_contract_data(contract_data)
        
        # Create database entry
        db_contract = Contract(
            contract_type=contract_request.contract_type,
            data=json.dumps(contract_data)
        )
        db.add(db_contract)
        db.commit()
        db.refresh(db_contract)
        
        # Generate HTML preview
        template_data = _contract_data_to_template_format(contract_data)
        preview_html = render_contract(template_data)
        
        # Generate PDF filename
        pdf_filename = contract_request.custom_pdf_filename
        if not pdf_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"contract_{db_contract.id}_{timestamp}.pdf"
        
        # Generate PDF
        pdf_path = generate_pdf_from_template_data(template_data, pdf_filename)
        
        # Prepare response
        contract_response = _create_contract_response(db_contract)
        
        pdf_info = {
            "pdf_path": pdf_path,
            "filename": os.path.basename(pdf_path),
            "download_url": f"/api/v1/contracts/download/{os.path.basename(pdf_path)}"
        }
        
        return ContractCreateResponse(
            message="Contract created successfully with HTML preview and PDF generated",
            contract_id=db_contract.id,
            contract_data=contract_response,
            preview_html=preview_html,
            pdf_info=pdf_info
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid contract data: {e}")
    except Exception as e:
        # Rollback database if PDF generation fails
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating contract: {e}")


@router.get("/contracts", response_model=ContractListResponse)
def get_contracts(
    skip: int = Query(0, ge=0, description="Number of contracts to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of contracts to return"),
    db: Session = Depends(get_db)
):
    """
    Get list of all stored contracts with ID, type, and created_at.
    Supports pagination with skip and limit parameters.
    """
    try:
        # Get total count
        total_count = db.query(Contract).count()
        
        # Get contracts with pagination
        db_contracts = db.query(Contract).offset(skip).limit(limit).all()
        
        # Convert to list items
        contract_items = []
        for db_contract in db_contracts:
            contract_data = _parse_contract_data(db_contract)
            
            contract_item = ContractListItem(
                id=db_contract.id,
                contract_type=db_contract.contract_type,
                party_a_name=contract_data.get("party_a", {}).get("name", "Unknown"),
                party_b_name=contract_data.get("party_b", {}).get("name", "Unknown"),
                created_at=db_contract.created_at
            )
            contract_items.append(contract_item)
        
        return ContractListResponse(
            message=f"Retrieved {len(contract_items)} contracts",
            total_contracts=total_count,
            contracts=contract_items
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving contracts: {e}")


@router.get("/contracts/{contract_id}", response_model=ContractDetailResponse)
def get_contract_by_id(contract_id: int, db: Session = Depends(get_db)):
    """
    Get full data for a specific contract by ID, including PDF file information.
    Returns complete contract details and PDF file status.
    """
    try:
        # Find contract in database
        db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not db_contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        # Create contract response
        contract_response = _create_contract_response(db_contract)
        
        # Check for PDF file
        pdf_files = get_generated_pdfs_list()
        pdf_file_path = None
        pdf_exists = False
        download_url = None
        
        # Look for PDF files associated with this contract
        for pdf_file in pdf_files:
            if f"contract_{contract_id}_" in pdf_file["filename"]:
                pdf_file_path = pdf_file["file_path"]
                pdf_exists = True
                download_url = f"/api/v1/contracts/download/{pdf_file['filename']}"
                break
        
        return ContractDetailResponse(
            contract=contract_response,
            pdf_file_path=pdf_file_path,
            pdf_exists=pdf_exists,
            download_url=download_url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving contract: {e}")


@router.delete("/contracts/{contract_id}", response_model=ContractDeleteResponse)
def delete_contract(
    contract_id: int, 
    delete_pdf: bool = Query(True, description="Whether to also delete associated PDF files"),
    db: Session = Depends(get_db)
):
    """
    Delete a contract entry from database and optionally delete associated PDF files.
    """
    try:
        # Find contract in database
        db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not db_contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        pdf_deleted = False
        
        # Delete associated PDF files if requested
        if delete_pdf:
            pdf_files = get_generated_pdfs_list()
            for pdf_file in pdf_files:
                if f"contract_{contract_id}_" in pdf_file["filename"]:
                    try:
                        success = delete_pdf_file(pdf_file["filename"])
                        if success:
                            pdf_deleted = True
                    except Exception as pdf_error:
                        # Log error but don't fail the contract deletion
                        print(f"Warning: Could not delete PDF file {pdf_file['filename']}: {pdf_error}")
        
        # Delete contract from database
        db.delete(db_contract)
        db.commit()
        
        return ContractDeleteResponse(
            message=f"Contract {contract_id} deleted successfully",
            contract_id=contract_id,
            pdf_deleted=pdf_deleted
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting contract: {e}")


# ===== ADDITIONAL UTILITY ENDPOINTS =====

@router.get("/contracts/{contract_id}/render", response_class=HTMLResponse)
def render_contract_html(contract_id: int, db: Session = Depends(get_db)):
    """
    Render a contract as HTML using Jinja2 template.
    """
    try:
        db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not db_contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        contract_data = _parse_contract_data(db_contract)
        template_data = _contract_data_to_template_format(contract_data)
        
        validate_contract_data(template_data)
        rendered_html = render_contract(template_data)
        
        return HTMLResponse(content=rendered_html)
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid contract data: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering contract: {e}")


@router.get("/contracts/{contract_id}/pdf")
def generate_contract_pdf(contract_id: int, custom_filename: str = None, db: Session = Depends(get_db)):
    """
    Generate PDF from existing contract in the database.
    """
    try:
        db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not db_contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        contract_data = _parse_contract_data(db_contract)
        template_data = _contract_data_to_template_format(contract_data)
        
        validate_contract_data(template_data)
        
        if custom_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            custom_filename = f"contract_{contract_id}_{timestamp}.pdf"
        
        pdf_path = generate_pdf_from_template_data(template_data, custom_filename)
        
        return {
            "message": "PDF generated successfully",
            "contract_id": contract_id,
            "pdf_path": pdf_path,
            "filename": os.path.basename(pdf_path),
            "download_url": f"/api/v1/contracts/download/{os.path.basename(pdf_path)}"
        }
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid contract data: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {e}")


@router.get("/contracts/download/{filename}")
def download_pdf(filename: str):
    """
    Download a generated PDF file by filename.
    """
    pdf_dir = "generated_pdfs"
    file_path = os.path.join(pdf_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    if not filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    return FileResponse(
        path=file_path,
        media_type='application/pdf',
        filename=filename
    )


@router.get("/contracts/sample-data")
def get_sample_data():
    """
    Returns sample contract data that can be used to test the endpoints.
    """
    return {
        "message": "Sample contract data for testing",
        "data": get_sample_contract_data()
    } 