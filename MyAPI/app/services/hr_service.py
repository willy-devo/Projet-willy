from app.storage.json_adapter import load_data
from app.models.hr import Employee, EmployeeDetail
from typing import List, Optional

def get_all_employees(department: Optional[str] = None) -> List[Employee]:
    """Liste les employés, avec filtrage optionnel par département."""
    data = load_data("hr") # Charge employees.json
    employees = data.get("employees", [])
    
    if department:
        employees = [e for e in employees if e["department"].lower() == department.lower()]
    
    return [Employee(**e) for e in employees]

def get_employee_by_id(emp_id: str) -> Optional[EmployeeDetail]:
    """Récupère le profil complet d'un collaborateur."""
    data = load_data("hr")
    employees = data.get("employees", [])
    emp_data = next((e for e in employees if e["emp_id"] == emp_id), None)
    
    return EmployeeDetail(**emp_data) if emp_data else None

def search_experts_by_skill(skill: str) -> List[Employee]:
    """Recherche des collaborateurs possédant une compétence spécifique."""
    data = load_data("hr")
    employees = data.get("employees", [])
    
    # Recherche insensible à la casse dans la liste des skills
    experts = [
        e for e in employees 
        if any(skill.lower() in s.lower() for s in e.get("skills", []))
    ]
    
    return [Employee(**e) for e in experts]