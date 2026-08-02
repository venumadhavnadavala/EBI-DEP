# 📊 Enterprise Business Intelligence & Data Engineering Platform

An enterprise-scale Business Intelligence (BI) and Data Engineering platform built to simulate a real-world analytics pipeline. The project follows a modern layered data warehouse architecture and demonstrates how raw business data is transformed into analytics-ready datasets using ETL pipelines, PostgreSQL, dbt, and Docker.

This project is being developed by a **2-member team**, where each member owns a separate business domain while collaborating on the shared data warehouse and infrastructure.

---

# 🚀 Project Overview

The platform processes business data through multiple layers:

```
CSV Data Sources
        │
        ▼
Python ETL Pipelines
        │
        ▼
Raw Schema
(Original Source Data)
        │
        ▼
Staging Schema
(Cleaned & Validated Data)
        │
        ▼
dbt Transformations
        │
        ▼
Marts Schema
(Business KPIs)
        │
        ▼
FastAPI (Upcoming)
        │
        ▼
Dashboard (Upcoming)
```

The architecture follows a traditional enterprise data warehouse approach used in modern analytics systems.

---

# ✨ Features

## ✅ Enterprise Data Warehouse

- Layered warehouse architecture
  - Raw
  - Staging
  - Marts
- PostgreSQL data warehouse
- Schema-driven database design
- Dockerized PostgreSQL environment

---

## ✅ Data Generation

Synthetic datasets for:

- Customers
- Employees
- Orders
- Order Lines
- Products
- Suppliers
- Inventory
- Returns

---

## ✅ Python ETL Pipelines

### Sales & Customer Analytics

- Extract source data
- Validate records
- Remove duplicates
- Handle missing values
- Type conversion
- Revenue calculation
- Load into warehouse

---

### Product & Inventory Analytics

- Inventory validation
- Product cleaning
- Supplier processing
- Return data processing
- Inventory standardization
- Load into warehouse

---

## ✅ Data Quality

The ETL pipeline performs:

- Duplicate removal
- Null handling
- Invalid record filtering
- Data type conversion
- Business rule validation

---

## ✅ dbt Data Models

Business-ready analytical models include:

- Monthly Revenue
- Customer Lifetime Value (CLV)
- Salesperson Performance
- Product Profitability
- Inventory Health
- Return Analysis

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Programming | Python |
| Database | PostgreSQL |
| ETL | Pandas |
| Data Transformation | dbt |
| SQL | PostgreSQL SQL |
| Containerization | Docker |
| Orchestration | Apache Airflow *(Upcoming)* |
| API | FastAPI *(Upcoming)* |
| Dashboard | React + Chart.js *(Upcoming)* |

---

# 📂 Project Structure

```
biplatform
│
├── api/                # FastAPI backend (Upcoming)
├── dags/               # Airflow DAGs
├── dashboard/          # Dashboard UI
├── data/
│   ├── raw/            # Generated CSV files
│   ├── etl_sales.py
│   ├── etl_inventory.py
│   ├── generate_data.py
│   └── db.py
│
├── dbt_project/
│   ├── models/
│   ├── macros/
│   └── profiles/
│
├── sql/
│   └── schema.sql
│
├── docker/
└── docker-compose.yml
```

---

# 🏗 Data Warehouse Architecture

## Raw Layer

Stores the original extracted data without modifications.

Purpose:

- Data backup
- Audit trail
- Reprocessing

---

## Staging Layer

Stores validated and cleaned data.

Operations include:

- Duplicate removal
- Missing value handling
- Type conversion
- Data validation

---

## Marts Layer

Built using dbt.

Provides analytics-ready tables for:

- Revenue analysis
- Customer analytics
- Inventory analytics
- Product performance

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/enterprise-bi-platform.git

cd enterprise-bi-platform/biplatform
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

### Data Pipeline

```bash
pip install -r data/requirements.txt
```

### dbt

```bash
pip install -r dbt_project/requirements.txt
```

### FastAPI (Upcoming)

```bash
pip install -r api/requirements.txt
```

---

## 4. Start Docker

```bash
docker compose up -d
```

---

## 5. Generate Data

```bash
cd data

python generate_data.py
```

---

## 6. Run ETL Pipelines

```bash
python etl_sales.py

python etl_inventory.py
```

---

## 7. Run dbt Models

```bash
cd ..

cd dbt_project

dbt run --profiles-dir profiles
```

---

# 📈 Current Progress

- ✅ PostgreSQL Warehouse
- ✅ Warehouse Schema
- ✅ Python ETL
- ✅ Raw Layer
- ✅ Staging Layer
- ✅ dbt Models
- ✅ Docker
- 🚧 FastAPI
- 🚧 React Dashboard
- 🚧 Apache Airflow
- 🚧 AI Business Insights

---

# 👨‍💻 Team Responsibilities

## Venu Madhav

### Sales & Customer Analytics

- Sales ETL
- Customer ETL
- Revenue KPIs
- Customer KPIs
- Sales dbt Models
- Sales APIs *(Upcoming)*
- Sales Dashboard *(Upcoming)*

---

## Karthik

### Product & Inventory Analytics

- Inventory ETL
- Product ETL
- Inventory KPIs
- Product KPIs
- Inventory dbt Models
- Inventory APIs *(Upcoming)*
- Inventory Dashboard *(Upcoming)*

---

## Shared

- PostgreSQL
- Database Design
- Docker
- Authentication *(Upcoming)*
- Deployment *(Upcoming)*
- AI Insights *(Upcoming)*

---

# 🚀 Future Enhancements

- FastAPI REST APIs
- Interactive React Dashboard
- Apache Airflow Scheduling
- AI-powered Business Insights
- JWT Authentication
- Automated Deployment

---

# 👨‍💻 Developed By

## Venu Madhav Nadavala
## Karthik Dommaraju

B.Tech, IIT Tirupati
