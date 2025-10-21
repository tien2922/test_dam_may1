# BDU Inventory Management (React + FastAPI + MySQL/RDS)

A practical **inventory management** starter built for VS Code first, then containerized for AWS.
- **Frontend**: React (Vite). Local dev on `http://localhost:5173`, build static to serve by Nginx
- **Backend**: FastAPI (async SQLAlchemy + aiomysql). Local dev on `http://localhost:8080`
- **Database**: MySQL (Docker for dev, **RDS** in prod)

## Core features
- Products: CRUD (`sku`, `name`, `unit_price`, `stock`)
- Suppliers: CRUD (`name`, `email`, `phone`)
- Stock Movements: record **IN/OUT** moves and auto-update product stock atomically
- Simple seed data

## Architecture
```
Browser ⇄ Frontend (React) ⇄ Backend (FastAPI) ⇄ MySQL (local or Amazon RDS)
```

---

## 1) Local Dev (VS Code first)

### 1.1 Start MySQL (Docker)
```bash
cd backend
docker compose up -d
# mysql:8.0  → 3306 (root/secret)
mysql -h127.0.0.1 -P3306 -uroot -psecret <<'SQL'
CREATE DATABASE IF NOT EXISTS bdu_inventory;
USE bdu_inventory;
SOURCE ../sql/schema.sql;
SQL
```

### 1.2 Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# DB_URL=mysql+aiomysql://root:secret@127.0.0.1:3306/bdu_inventory
uvicorn app.main:app --reload --port 8080
# http://localhost:8080/docs
```

### 1.3 Frontend
```bash
cd frontend
npm install
cp .env.example .env   # VITE_API_BASE_URL=http://localhost:8080
npm run dev            # http://localhost:5173
```

---

## 2) Docker flows

### Dev (hot reload all services)
```bash
docker compose -f docker-compose.dev.yml up --build
# FE: http://localhost:5173 | BE: http://localhost:8080
```

### Prod-style images (for EC2 + RDS)
```bash
export DB_URL="mysql+aiomysql://<user>:<pass>@<rds-endpoint>:3306/bdu_inventory"
export CORS_ORIGINS="https://your-frontend-domain"
docker compose build
docker compose up -d
# FE: 80 (Nginx) | BE: 8080 (gunicorn/uvicorn)
```

---

## 3) API Summary
- **Products**
  - `GET /api/products`
  - `POST /api/products`
  - `PUT /api/products/{id}`
  - `DELETE /api/products/{id}`
- **Suppliers**
  - `GET /api/suppliers`
  - `POST /api/suppliers`
  - `PUT /api/suppliers/{id}`
  - `DELETE /api/suppliers/{id}`
- **Stock Moves**
  - `GET /api/stock_moves`
  - `POST /api/stock_moves` with JSON `{"product_id":1,"quantity":10,"move_type":"IN","note":"initial"}`
    - `move_type` = `IN` or `OUT`
    - Enforces non-negative stock (prevents OUT beyond current)

---

## 4) Files
- `frontend/` React Vite app
- `backend/` FastAPI with async SQLAlchemy
- `sql/schema.sql` DB schema + seed data
- `docker-compose.dev.yml` (dev with hot reload)
- `docker-compose.yml` (prod FE+BE; use RDS for DB)
- `.vscode/` launch & tasks for VS Code first workflow

Generated: 2025-10-10
