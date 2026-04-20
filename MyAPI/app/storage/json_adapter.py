import json
import os
from pathlib import Path
from typing import Dict, Any

# Chemin vers le dossier de stockage défini dans l'arborescence
STORAGE_DIR = Path(__file__).parent.parent.parent / "catalog" / "storage"

# Mapping des noms de domaines vers les noms de fichiers réels
FILE_MAP = {
    "customers": "customers.json",
    "inventory": "products.json",
    "hr": "employees.json",
    "sales": "orders.json",
    "logistics": "orders.json",  # Partage le même fichier source que sales
    "finance": "orders.json",    # Partage le même fichier source que sales
}

def load_data(domain: str) -> Dict[str, Any]:
    """
    Charge les données JSON pour un domaine spécifique.
    """
    file_name = FILE_MAP.get(domain)
    if not file_name:
        raise ValueError(f"Domaine '{domain}' non reconnu par l'adaptateur.")
    
    file_path = STORAGE_DIR / file_name
    
    if not file_path.exists():
        # Retourne une structure vide si le fichier n'existe pas encore
        return {domain: []}

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {domain: []}

def save_data(domain: str, data: Dict[str, Any]) -> bool:
    """
    Sauvegarde les données dans le fichier JSON correspondant au domaine.
    """
    file_name = FILE_MAP.get(domain)
    if not file_name:
        return False
    
    file_path = STORAGE_DIR / file_name
    
    # Assure que le dossier existe avant d'écrire
    os.makedirs(STORAGE_DIR, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True