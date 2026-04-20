from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.hr import Employee, EmployeeDetail
from app.services import hr_service

router = APIRouter()

@router.get("/", response_model=dict)
async def list_employees(department: Optional[str] = None):
    """Liste le personnel de l'entreprise."""
    employees = hr_service.get_all_employees(department)
    return {"employees": employees}

@router.get("/expertise", response_model=dict)
async def get_experts(skill: str = Query(..., description="La compétence recherchée")):
    """Recherche d'un expert par domaine technique (ex: Kubernetes)."""
    experts = hr_service.search_experts_by_skill(skill)
    return {"experts": experts}

@router.get("/{id}", response_model=EmployeeDetail)
async def read_employee(id: str):
    """Récupère le profil détaillé d'un collaborateur."""
    employee = hr_service.get_employee_by_id(id)
    if not employee:
        raise HTTPException(status_code=404, detail="L'employé spécifié n'existe pas")
    return employee