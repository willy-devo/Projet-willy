from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Invoice(BaseModel):
    """
    Modèle représentant une facture générée à partir d'une commande.
    Correspond à la définition dans finance.yaml.
    """
    invoice_id: str = Field(..., description="ID unique de la facture (ex: INV-2026-001)")
    order_id: str = Field(..., description="Référence de la commande liée (ex: CMD-2026-001)")
    billing_date: datetime = Field(default_factory=datetime.now)
    amount_ht: float = Field(..., description="Montant hors taxes calculé")
    vat_rate: float = Field(default=20.0, description="Taux de TVA en pourcentage")
    amount_ttc: float = Field(..., description="Montant total TTC (issu de orders.json)")
    currency: str = Field(default="EUR")

class RevenueStats(BaseModel):
    """
    Modèle pour les rapports de performance financière.
    """
    total_revenue: float = Field(..., description="Somme de tous les montants TTC")
    currency: str = "EUR"
    order_count: int = Field(..., description="Nombre total de transactions traitées")

class FinanceReport(BaseModel):
    """
    Modèle global regroupant les statistiques et la liste des factures récentes.
    """
    stats: RevenueStats
    recent_invoices: List[Invoice] # Utilisation de List avec majuscule (nécessite l'import typing)