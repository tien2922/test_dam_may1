from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product, Supplier, StockMove

# ---------- Products ----------
async def list_products(db: AsyncSession):
    res = await db.execute(select(Product).order_by(Product.id.desc()))
    return list(res.scalars())

async def create_product(db: AsyncSession, sku: str, name: str, unit_price: float):
    obj = Product(sku=sku, name=name, unit_price=unit_price, stock=0)
    db.add(obj); await db.commit(); await db.refresh(obj)
    return obj

async def update_product(db: AsyncSession, pid: int, data: dict):
    q = update(Product).where(Product.id==pid).values(**data)
    res = await db.execute(q); await db.commit()
    return res.rowcount

async def delete_product(db: AsyncSession, pid: int):
    q = delete(Product).where(Product.id==pid)
    res = await db.execute(q); await db.commit()
    return res.rowcount

# ---------- Suppliers ----------
async def list_suppliers(db: AsyncSession):
    res = await db.execute(select(Supplier).order_by(Supplier.id.desc()))
    return list(res.scalars())

async def create_supplier(db: AsyncSession, name: str, email: str | None, phone: str | None):
    obj = Supplier(name=name, email=email, phone=phone)
    db.add(obj); await db.commit(); await db.refresh(obj)
    return obj

async def update_supplier(db: AsyncSession, sid: int, data: dict):
    q = update(Supplier).where(Supplier.id==sid).values(**data)
    res = await db.execute(q); await db.commit()
    return res.rowcount

async def delete_supplier(db: AsyncSession, sid: int):
    q = delete(Supplier).where(Supplier.id==sid)
    res = await db.execute(q); await db.commit()
    return res.rowcount

# ---------- Stock Moves ----------
async def list_moves(db: AsyncSession):
    res = await db.execute(select(StockMove).order_by(StockMove.id.desc()))
    return list(res.scalars())

async def apply_move(db: AsyncSession, product_id: int, quantity: int, move_type: str, note: str | None):
    # lock product row for update
    res = await db.execute(select(Product).where(Product.id==product_id).with_for_update())
    prod = res.scalar_one_or_none()
    if not prod:
        return None, "PRODUCT_NOT_FOUND"
    if move_type not in ("IN","OUT"):
        return None, "INVALID_MOVE_TYPE"
    if quantity <= 0:
        return None, "INVALID_QUANTITY"

    if move_type == "OUT" and prod.stock < quantity:
        return None, "INSUFFICIENT_STOCK"

    # update stock
    prod.stock = prod.stock + quantity if move_type=="IN" else prod.stock - quantity
    mv = StockMove(product_id=product_id, quantity=quantity, move_type=move_type, note=note)
    db.add(mv)
    await db.commit()
    await db.refresh(mv)
    return mv, None
