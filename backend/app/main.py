import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, AsyncSessionLocal
from .models import Base
from . import crud, schemas

APP_PORT = int(os.getenv("APP_PORT", "8080"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

app = FastAPI(title="BDU Inventory Management API")

allow_origins = [o.strip() for o in CORS_ORIGINS.split(",")] if CORS_ORIGINS and CORS_ORIGINS != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def on_startup():
    # If DB user has permissions, uncomment to auto-create:
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    pass

@app.get("/health")
async def health():
    return {"status": "ok"}

# ----- Products -----
@app.get("/api/products", response_model=list[schemas.ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await crud.list_products(db)

@app.post("/api/products", response_model=schemas.ProductOut, status_code=201)
async def create_product(payload: schemas.ProductIn, db: AsyncSession = Depends(get_db)):
    return await crud.create_product(db, payload.sku, payload.name, payload.unit_price)

@app.put("/api/products/{pid}")
async def update_product(pid: int, payload: schemas.ProductIn, db: AsyncSession = Depends(get_db)):
    updated = await crud.update_product(db, pid, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"updated": updated}

@app.delete("/api/products/{pid}")
async def delete_product(pid: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_product(db, pid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"deleted": deleted}

# ----- Suppliers -----
@app.get("/api/suppliers", response_model=list[schemas.SupplierOut])
async def list_suppliers(db: AsyncSession = Depends(get_db)):
    return await crud.list_suppliers(db)

@app.post("/api/suppliers", response_model=schemas.SupplierOut, status_code=201)
async def create_supplier(payload: schemas.SupplierIn, db: AsyncSession = Depends(get_db)):
    return await crud.create_supplier(db, payload.name, payload.email, payload.phone)

@app.put("/api/suppliers/{sid}")
async def update_supplier(sid: int, payload: schemas.SupplierIn, db: AsyncSession = Depends(get_db)):
    updated = await crud.update_supplier(db, sid, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"updated": updated}

@app.delete("/api/suppliers/{sid}")
async def delete_supplier(sid: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_supplier(db, sid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"deleted": deleted}

# ----- Stock Moves -----
@app.get("/api/stock_moves", response_model=list[schemas.MoveOut])
async def list_moves(db: AsyncSession = Depends(get_db)):
    return await crud.list_moves(db)

@app.post("/api/stock_moves", response_model=schemas.MoveOut, status_code=201)
async def create_move(payload: schemas.MoveIn, db: AsyncSession = Depends(get_db)):
    mv, err = await crud.apply_move(db, payload.product_id, payload.quantity, payload.move_type, payload.note)
    if err == "PRODUCT_NOT_FOUND":
        raise HTTPException(404, "Product not found")
    if err == "INVALID_MOVE_TYPE":
        raise HTTPException(400, "Invalid move_type (must be IN or OUT)")
    if err == "INVALID_QUANTITY":
        raise HTTPException(400, "Quantity must be > 0")
    if err == "INSUFFICIENT_STOCK":
        raise HTTPException(400, "Insufficient stock for OUT move")
    return mv
