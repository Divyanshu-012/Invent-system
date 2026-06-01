# InventHub — Inventory & Order Management System

A production-ready full-stack application for managing products, customers, and orders with automatic inventory tracking.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + TailwindCSS |
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
inventory-system/
├── backend/
│   ├── main.py          # FastAPI app + routes
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # Database operations + business logic
│   ├── database.py      # DB connection setup
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/       # Dashboard, Products, Customers, Orders
│   │   ├── components/  # Sidebar, Modal, EmptyState
│   │   └── utils/api.js # Axios API calls
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── .env.example
```

---

## Quick Start (Local Docker)

### 1. Clone & configure
```bash
git clone <your-repo-url>
cd inventory-system
cp .env.example .env
# Edit .env with your values
```

### 2. Run everything
```bash
docker compose up --build
```

### 3. Access
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## API Endpoints

### Products
| Method | Endpoint | Description |
|---|---|---|
| POST | /products | Create product |
| GET | /products | List all products |
| GET | /products/{id} | Get product |
| PUT | /products/{id} | Update product |
| DELETE | /products/{id} | Delete product |

### Customers
| Method | Endpoint | Description |
|---|---|---|
| POST | /customers | Create customer |
| GET | /customers | List all customers |
| GET | /customers/{id} | Get customer |
| DELETE | /customers/{id} | Delete customer |

### Orders
| Method | Endpoint | Description |
|---|---|---|
| POST | /orders | Create order |
| GET | /orders | List all orders |
| GET | /orders/{id} | Get order details |
| DELETE | /orders/{id} | Cancel order (restores stock) |

### Dashboard
| Method | Endpoint | Description |
|---|---|---|
| GET | /dashboard | Stats + low stock alerts |

---

## Business Rules Implemented

- ✅ Product SKU must be unique
- ✅ Customer email must be unique
- ✅ Product quantity cannot be negative
- ✅ Orders blocked if insufficient stock
- ✅ Order creation auto-reduces stock
- ✅ Order cancellation auto-restores stock
- ✅ Total amount auto-calculated from product prices

---

## Deployment Guide

### Backend → Render

1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repo, select `backend/` directory
3. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable:
   - `DATABASE_URL` = your Render PostgreSQL URL
5. Deploy → copy the URL (e.g. `https://inventhub-api.onrender.com`)

### Frontend → Vercel

1. Go to [vercel.com](https://vercel.com) → New Project
2. Import your GitHub repo, set **Root Directory** to `frontend/`
3. Add environment variable:
   - `VITE_API_URL` = your Render backend URL
4. Deploy → your frontend is live

### Docker Hub (Backend Image)

```bash
docker build -t yourusername/inventhub-backend ./backend
docker push yourusername/inventhub-backend
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@db:5432/inventory` |
| `POSTGRES_USER` | DB username | `postgres` |
| `POSTGRES_PASSWORD` | DB password | `postgres` |
| `POSTGRES_DB` | Database name | `inventory` |
| `VITE_API_URL` | Backend API URL for frontend | `http://localhost:8000` |
