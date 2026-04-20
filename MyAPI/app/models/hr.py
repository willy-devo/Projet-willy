from pydantic import BaseModel, Field
from typing import List, Optional

from pydantic import BaseModel, Field
from typing import List, Optional

class Employee(BaseModel):
    """
    Modèle représentant un employé du groupe.
    Aligné sur la structure de employees.json.
    """
    emp_id: str = Field(..., example="EMP-442")
    full_name: str = Field(..., example="Alice Martin")
    role: str = Field(..., example="Cloud Architect")
    department: str = Field(..., example="IT Infrastructure")
    skills: List[str] = Field(default_factory=list)
    clearance: int = Field(..., ge=1, le=5, example=4)
    biography: str = Field(..., description="Description détaillée de l'expérience et des responsabilités.")

    class Config:
        # Permet l'affichage des exemples dans Swagger UI (/docs)
        schema_extra = {
            "example": {
                "emp_id": "EMP-442",
                "full_name": "Alice Martin",
                "role": "Cloud Architect",
                "department": "IT Infrastructure",
                "skills": ["AWS", "Kubernetes", "API Gateway"],
                "clearance": 4,
                "biography": "Experte en conception d'architectures distribuées..."
            }
        }

class EmployeeDetail(Employee):
    skills: List[str] = Field(default=[], description="Compétences techniques")
    biography: str = Field(..., description="Parcours utilisé pour l'analyse sémantique")
    clearance: int = Field(default=1, description="Niveau d'accréditation")