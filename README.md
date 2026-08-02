# Enterprise Sales & Inventory BI Platform

A 2-person data engineering + analytics project. Both members build the
same technical pattern (ETL → warehouse → dbt models → API → dashboard →
AI insights); only the business domain differs.

- **Member 1** owns: Sales & Customer Analytics
- **Member 2** owns: Product & Inventory Analytics
- **Shared**: warehouse schema, Docker setup, dashboard shell, AI insights layer

---

## What was actually verified (read this before you claim anything in an interview)

Everything below was run for real against a live Postgres instance during
development — not just written and assumed correct. Five real bugs were
found and fixed in the process; they're listed because you should be able
to explain at least a couple of them if asked "what went wrong when you
built this?" (that question is common, and "everything worked first try"
is not a believable answer):

1. **ETL path bug** — scripts read `data/raw/*.csv` with a relative path,
   which only resolves correctly if you run them from the project root,
   not from inside `data/`. Fixed by documenting the required working
   directory (see below) rather than hardcoding absolute paths.
2. **Postgres `round()` type error** — `round(double precision, integer)`
   doesn't exist in Postgres; `round()` with a precision argument requires
   a `numeric` type. Every `round(x / y, n)` in the dbt models needed an
   explicit `::numeric` cast.
3. **Interval vs integer comparison** — `current_date - timestamp_column`
   returns an `interval`, not an integer, so `> 90` failed. Fixed by
   casting the timestamp to `::date` first so subtraction yields a plain
   integer day count.
4. **dbt schema naming** — by default, dbt does NOT put a model tagged
   `+schema: marts` into a schema literally called `marts`. It
   concatenates `<profile_target_schema>_<custom_schema>`, so everything
   landed in `staging_marts` instead. Fixed with a custom
   `generate_schema_name` macro. This is a well-known dbt gotcha — if an
   interviewer asks "why does your macros folder have that file," this is
   why.
5. **Dashboard default filter too aggressive** — the returns-analysis
   widget defaulted to `min_rate=0.05` (5%), but the synthetic dataset's
   real return rates topped out around 4%, so the widget silently showed
   nothing. Not a code bug — a bad default given the data's actual
   distribution. Lowered to 1%.

**Verified working end-to-end:** data generation → Postgres schema →
both ETL pipelines → all 6 dbt models → all FastAPI endpoints (sales,
inventory, AI insights) → dashboard successfully served and pointed at
the live API.

**NOT verified in this environment** (network/sandbox restrictions,
not code problems):
- Full Airflow scheduler execution — the two DAG files are syntactically
  valid Python (AST-parsed clean) and structurally correct, but were never
  run inside an actual Airflow scheduler/webserver. You should do this
  yourself with `docker-compose` + the official Airflow image before
  claiming "orchestrated with Airflow" in an interview.
- `docker-compose.yml` as a whole — built to standard patterns but not
  spun up as containers in this sandbox (no Docker daemon available here).
  Test it yourself: `docker compose up --build`.
- The LLM narrative layer in `/insights` — code path is written and has a
  tested fallback (confirmed working), but the actual Anthropic API call
  branch only runs if you set `ANTHROPIC_API_KEY`, which wasn't configured
  here.

Don't let this list scare you — this is what a real, honestly-tested
project's caveats look like. A project with zero caveats listed is one
nobody actually ran.

---

## Architecture

```
Raw CSVs (simulated source system)
   |
   v
ETL (Python/pandas)  --------->  Postgres: raw -> staging
   |  Member 1: sales.py                (validate, dedupe, clean)
   |  Member 2: inventory.py
   v
dbt models  ---------------->  Postgres: marts (fct_* tables)
   |  Member 1: models/sales/
   |  Member 2: models/inventory/
   v
FastAPI  -------------------->  REST endpoints per domain
   |  Member 1: routers/sales.py
   |  Member 2: routers/inventory.py
   |  Shared:   routers/ai_insights.py
   v
Dashboard (HTML + Chart.js) -->  Tabs: Sales | Inventory
```

Orchestration: Airflow DAGs (`dags/sales_dag.py`, `dags/inventory_dag.py`)
schedule the ETL + dbt run daily, staggered an hour apart.

---

## How to run it yourself

### 1. Local (no Docker) — what was used to verify this project
```bash
# Postgres
sudo apt-get install postgresql
sudo service postgresql start
sudo -u postgres psql -c "CREATE USER biuser WITH PASSWORD 'bipass' SUPERUSER;"
sudo -u postgres psql -c "CREATE DATABASE bi_platform OWNER biuser;"

# From the project root (NOT from inside data/ — see bug #1 above)
pip install -r data/requirements.txt
psql -h localhost -U biuser -d bi_platform -f sql/schema.sql
export DATABASE_URL="postgresql+psycopg2://biuser:bipass@localhost:5432/bi_platform"
python3 data/generate_data.py
python3 data/etl_sales.py
python3 data/etl_inventory.py

# dbt
pip install dbt-postgres
cd dbt_project
export DBT_PROFILES_DIR=$(pwd)/profiles
export DB_HOST=localhost DB_USER=biuser DB_PASSWORD=bipass DB_NAME=bi_platform
dbt run

# API
cd ../api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# docs at http://localhost:8000/docs

# Dashboard
cd ../dashboard
python3 -m http.server 3000
# open http://localhost:3000, point apiBase at http://localhost:8000
```

### 2. Docker (untested in this sandbox — verify yourself)
```bash
docker compose up --build
# Postgres: localhost:5432, API: localhost:8000, Dashboard: localhost:3000
```

---

## Resume bullets

### Member 1
**Enterprise Sales & Customer Analytics Platform** *(Team of 2)*
Python, SQL, PostgreSQL, dbt, Apache Airflow, FastAPI, Chart.js, Docker

- Built an ETL pipeline in Python that cleans and loads sales/customer
  data into Postgres, handling deduplication, null-imputation, and
  invalid-data rejection (e.g. negative quantities).
- Wrote dbt models to compute revenue, customer lifetime value, churn-risk
  flags, and salesperson performance from raw transactional data.
- Built FastAPI endpoints serving these metrics, and a dashboard tab
  visualizing revenue trends and at-risk customers.
- Debugged real Postgres type-casting and dbt schema-configuration issues
  while integrating the pipeline end-to-end.

### Member 2
**Enterprise Product & Inventory Analytics Platform** *(Team of 2)*
Python, SQL, PostgreSQL, dbt, Apache Airflow, FastAPI, Chart.js, Docker

- Built an ETL pipeline in Python that cleans and loads product,
  inventory, and returns data into Postgres, enforcing data-quality rules
  (e.g. clipping negative stock values).
- Wrote dbt models joining inventory and sales data to compute stock
  turnover, reorder alerts, product profitability, and return-rate
  analysis by reason.
- Built FastAPI endpoints and a dashboard tab surfacing reorder alerts
  and product profitability rankings.
- Debugged real Postgres type-casting and dbt schema-configuration issues
  while integrating the pipeline end-to-end.

**Do not use these verbatim if you haven't personally run the code and
hit at least some of these issues yourself.** Interviewers who ask "walk
me through a bug you hit" are testing whether the bullet is true.

---

## What to actually do before putting this on a resume

1. Run every command in the "How to run it" section yourself.
2. Break something on purpose (change a column name, feed it bad data)
   and fix it — that's what gives you something real to say when asked
   "what was hard about this."
3. Get Airflow and Docker Compose actually running — those two weren't
   verified here and are the two most likely to have real issues.
4. Change at least one KPI definition or add one new endpoint yourselves,
   so there's a piece of this that isn't just "Claude wrote it and I ran
   it."
