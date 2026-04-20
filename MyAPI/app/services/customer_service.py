from app.storage.json_adapter import load_data, save_data
from app.models.customer import Customer
from typing import List, Optional

def get_filtered_customers(
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    segment: Optional[str] = None,
    city: Optional[str] = None,
    interest: Optional[str] = None
) -> List[Customer]:
    data = load_data("customers")
    customers_list = data.get("customers", [])
    
    filtered = []
    for c in customers_list:
        # Logique de filtrage cumulative
        if full_name and full_name.lower() not in c.get("full_name", "").lower():
            continue
        if email and email.lower() != c.get("email", "").lower():
            continue
        if segment and segment != c.get("segment"):
            continue
        if city and city.lower() != c.get("city", "").lower(): # Champ city dans le JSON
            continue
        if interest and interest not in c.get("interests", []):
            continue
            
        filtered.append(Customer(**c))
    
    return filtered

def get_customer_by_id(cust_id: str) -> Optional[Customer]:
    data = load_data("customers")
    cust = next((c for c in data.get("customers", []) if c["customer_id"] == cust_id), None)
    return Customer(**cust) if cust else None

def upsert_customer(customer: Customer) -> Customer:
    data = load_data("customers")
    customers = data.get("customers", [])
    
    # Trouver l'index existant ou ajouter
    index = next((i for i, c in enumerate(customers) if c["customer_id"] == customer.customer_id), None)
    
    if index is not None:
        customers[index] = customer.dict()
    else:
        customers.append(customer.dict())
        
    data["customers"] = customers
    save_data("customers", data)
    return customer