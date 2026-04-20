from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Importation des routeurs de chaque domaine
from app.api.endpoints import (
    customers,
    inventory,
    hr,
    sales,
    logistics,
    finance,
    marketing
)

app = FastAPI(
    title="Magasin-Elec-Global API",
    description="Backend centralisé pour la gouvernance agentique et la recherche sémantique.",
    version="1.0.0"
)


app.mount("/docs", StaticFiles(directory="catalog/openapi"), name="docs")

# # Configuration CORS (essentiel pour Kong et les appels front/agents)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Montage des routes par domaine
# On utilise le préfixe /v1 pour matcher la configuration de la Gateway Kong
app.include_router(customers.router, prefix="/v1/customers", tags=["Customers"])
app.include_router(inventory.router, prefix="/v1/products", tags=["Inventory"])
app.include_router(hr.router, prefix="/v1/employees", tags=["HR"])
app.include_router(sales.router, prefix="/v1/orders", tags=["Sales"])
app.include_router(logistics.router, prefix="/v1/logistics", tags=["Logistics"])
app.include_router(finance.router, prefix="/v1/finance", tags=["Finance"])
app.include_router(marketing.router, prefix="/v1/marketing", tags=["Marketing"])

@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API Magasin-Elec-Global",
        "status": "online",
        "docs": "/docs"
    }