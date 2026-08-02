# 📊 Enterprise Business Intelligence & Data Engineering Platform

An enterprise-scale **Business Intelligence (BI)** and **Data Engineering** platform that simulates a real-world analytics pipeline. The project follows a modern layered data warehouse architecture and demonstrates how raw business data is transformed into analytics-ready datasets using **Python ETL, PostgreSQL, dbt, and Docker**.

The project is being developed by a **2-member team**, where each member owns a separate business domain while collaborating on the shared data warehouse, infrastructure, and deployment.

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
FastAPI (In Progress)
        │
        ▼
Dashboard (In Progress)
```

The architecture follows a traditional enterprise data warehouse approach used in modern analytics platforms.

---

# ✨ Features

## ✅ Enterprise Data Warehouse

- Layered warehouse architecture
  - Raw Layer
  - Staging Layer
  - Marts Layer
- PostgreSQL Data Warehouse
- Schema-driven database design
- Dockerized PostgreSQL environment

---

## ✅ Synthetic Data Generation

Automatically generates realistic business datasets for:

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
- Data type conversion
- Revenue calculation
- Load into PostgreSQL

### Product & Inventory Analytics

- Product validation
- Inventory processing
- Supplier data cleaning
- Returns processing
- Inventory standardization
- Load into PostgreSQL

---

## ✅ Data Quality

The ETL pipeline performs:

- Duplicate removal
- Missing value handling
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
| SQL | PostgreSQL |
| Containerization | Docker |
| Orchestration | Apache Airflow *(In Progress)* |
| REST API | FastAPI *(In Progress)* |
| Dashboard | React + Chart.js *(In Progress)* |

---

# 📂 Project Structure

```
EBI-DEP
│
├── api/                    # FastAPI Backend
├── dags/                   # Apache Airflow DAGs
├── dashboard/              # Dashboard UI
│
├── data/
│   ├── raw/
│   ├── db.py
│   ├── generate_data.py
│   ├── etl_sales.py
│   ├── etl_inventory.py
│   └── requirements.txt
│
├── dbt_project/
│   ├── macros/
│   ├── models/
│   ├── profiles/
│   ├── dbt_project.yml
│   └── requirements.txt
│
├── docker/
│
├── sql/
│   └── schema.sql
│
├── docker-compose.yml
└── README.md
```

---

# 🏗 Data Warehouse Architecture

## Raw Layer

Stores the original extracted data exactly as received from the source.

Purpose:

- Preserve original data
- Data auditing
- Reprocessing
- Backup layer

---

## Staging Layer

Stores validated and cleaned business data.

Operations performed:

- Duplicate removal
- Missing value handling
- Data validation
- Data type conversion
- Business rule enforcement

---

## Marts Layer

Built using **dbt**.

Provides analytics-ready tables for:

- Revenue Analysis
- Customer Analytics
- Inventory Analytics
- Product Performance

---

# ⚙️ Prerequisites

Before running the project, install:

- Python 3.11+
- Docker Desktop
- Git

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/venumadhavnadavala/EBI-DEP.git

cd EBI-DEP
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

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

### API

```bash
pip install -r api/requirements.txt
```

---

## 4. Start Docker Services

```bash
docker compose up -d
```

---

## 5. Generate Sample Data

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

## 7. Build dbt Models

```bash
cd ..

cd dbt_project

dbt run --profiles-dir profiles
```

---

## 8. Verify the Warehouse

```bash
docker exec -it bi_postgres psql -U biuser -d bi_platform
```

Example:

```sql
SELECT COUNT(*) FROM staging.stg_customers;

SELECT COUNT(*) FROM marts.fct_monthly_revenue;
```

---

# ✅ Current Progress

- ✅ PostgreSQL Warehouse
- ✅ Layered Warehouse Architecture
- ✅ Database Schema Design
- ✅ Synthetic Data Generator
- ✅ Python ETL Pipelines
- ✅ Raw Layer
- ✅ Staging Layer
- ✅ dbt Transformations
- ✅ Dockerized Deployment
- 🚧 FastAPI Backend
- 🚧 React Dashboard
- 🚧 Apache Airflow
- 🚧 AI Business Insights

---

# 👨‍💻 Team Responsibilities

## Venu Madhav Nadavala

### Sales & Customer Analytics

- Sales ETL Pipeline
- Customer ETL Pipeline
- Revenue KPIs
- Customer KPIs
- Sales dbt Models
- Sales APIs *(In Progress)*
- Sales Dashboard *(In Progress)*

---

## Karthik Dommaraju

### Product & Inventory Analytics

- Inventory ETL Pipeline
- Product ETL Pipeline
- Inventory KPIs
- Product KPIs
- Inventory dbt Models
- Inventory APIs *(In Progress)*
- Inventory Dashboard *(In Progress)*

---

## Shared Responsibilities

- PostgreSQL Warehouse
- Database Design
- Docker
- Authentication *(Planned)*
- Deployment *(Planned)*
- AI Insights *(Planned)*

---

# 🚀 Future Enhancements

- REST APIs using FastAPI
- Interactive React Dashboard
- Apache Airflow Scheduling
- AI-powered Business Insights
- JWT Authentication
- Automated Deployment
- CI/CD Pipeline
- Cloud Deployment (AWS)

---

# 👨‍💻 Developed By

### Venu Madhav Nadavala

### Karthik Dommaraju

**B.Tech, IIT Tirupati**
