from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import json

from database import get_db
from models import Contract

router = APIRouter()

# Pydantic models for request/response
class ContractCreate(BaseModel):
    contract_type: str
    data: dict

class ContractUpdate(BaseModel):
    contract_type: str = None
    data: dict = None

class ContractResponse(BaseModel):
    id: int
    contract_type: str
    data: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Create a new contract
@router.post("/contracts/", response_model=ContractResponse)
def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    db_contract = Contract(
        contract_type=contract.contract_type,
        data=json.dumps(contract.data)
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    
    # Convert data back to dict for response
    db_contract.data = json.loads(db_contract.data) if db_contract.data else {}
    return db_contract

# Get all contracts
@router.get("/contracts/", response_model=List[ContractResponse])
def read_contracts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contracts = db.query(Contract).offset(skip).limit(limit).all()
    
    # Convert data back to dict for response
    for contract in contracts:
        contract.data = json.loads(contract.data) if contract.data else {}
    
    return contracts

# Get a specific contract by ID
@router.get("/contracts/{contract_id}", response_model=ContractResponse)
def read_contract(contract_id: int, db: Session = Depends(get_db)):
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Convert data back to dict for response
    db_contract.data = json.loads(db_contract.data) if db_contract.data else {}
    return db_contract

# Update a contract
@router.put("/contracts/{contract_id}", response_model=ContractResponse)
def update_contract(contract_id: int, contract: ContractUpdate, db: Session = Depends(get_db)):
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    if contract.contract_type is not None:
        db_contract.contract_type = contract.contract_type
    if contract.data is not None:
        db_contract.data = json.dumps(contract.data)
    
    db.commit()
    db.refresh(db_contract)
    
    # Convert data back to dict for response
    db_contract.data = json.loads(db_contract.data) if db_contract.data else {}
    return db_contract

# Delete a contract
@router.delete("/contracts/{contract_id}")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    db.delete(db_contract)
    db.commit()
    return {"message": "Contract deleted successfully"} 