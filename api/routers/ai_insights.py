"""
SHARED — AI Insights API

This module generates executive business insights.

Architecture:
PostgreSQL -> dbt KPIs -> Rule Engine -> Optional LLM Narrative

The rule engine always works.
The LLM only converts structured insights into a readable executive summary.
"""

import os
from datetime import datetime

from fastapi import APIRouter

from db import query

router = APIRouter(
    prefix="/insights",
    tags=["AI Insights"],
)

USE_LLM = bool(os.getenv("ANTHROPIC_API_KEY"))


# ============================================================
# SALES INSIGHTS
# ============================================================

def rule_based_sales_insights():

    at_risk = query("""
        SELECT COUNT(*) AS n
        FROM marts.fct_customer_ltv
        WHERE at_risk_flag = TRUE
    """)[0]["n"]

    top_region = query("""
        SELECT
            region,
            SUM(total_revenue) AS revenue
        FROM marts.fct_monthly_revenue
        GROUP BY region
        ORDER BY revenue DESC
        LIMIT 1
    """)

    insights = [
        f"{at_risk} customers have not placed an order in the last 90 days and are at risk of churn."
    ]

    if top_region:
        insights.append(
            f"{top_region[0]['region']} is currently the highest revenue-generating region."
        )

    return insights


# ============================================================
# INVENTORY INSIGHTS
# ============================================================

def rule_based_inventory_insights():

    reorder = query("""
        SELECT COUNT(*) AS n
        FROM marts.fct_inventory_health
        WHERE needs_reorder = TRUE
    """)[0]["n"]

    worst_return = query("""
        SELECT
            product_name,
            return_rate
        FROM marts.fct_return_analysis
        ORDER BY return_rate DESC
        LIMIT 1
    """)

    insights = [
        f"{reorder} products are currently below their reorder threshold."
    ]

    if worst_return:
        insights.append(
            f"{worst_return[0]['product_name']} has the highest return rate "
            f"({round(worst_return[0]['return_rate'] * 100, 2)}%)."
        )

    return insights


# ============================================================
# OPTIONAL LLM
# ============================================================

def narrate_with_llm(bullet_points, domain):

    if not USE_LLM:
        return " ".join(bullet_points)

    try:
        import anthropic

        client = anthropic.Anthropic()

        prompt = f"""
You are an enterprise business analyst.

Generate a concise executive summary (2-3 sentences).

Domain:
{domain}

Business Facts:
{chr(10).join("- " + b for b in bullet_points)}

Requirements:
- Professional tone
- No assumptions
- No marketing language
- Mention only supported facts
"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.content[0].text.strip()

    except Exception:
        return " ".join(bullet_points)


# ============================================================
# SALES ENDPOINT
# ============================================================

@router.get("/sales")
def sales_insights():

    bullets = rule_based_sales_insights()

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "generated_by": "LLM" if USE_LLM else "Rule Engine",
        "llm_enabled": USE_LLM,
        "domain": "Sales",
        "bullets": bullets,
        "summary": narrate_with_llm(bullets, "Sales Analytics"),
    }


# ============================================================
# INVENTORY ENDPOINT
# ============================================================

@router.get("/inventory")
def inventory_insights():

    bullets = rule_based_inventory_insights()

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "generated_by": "LLM" if USE_LLM else "Rule Engine",
        "llm_enabled": USE_LLM,
        "domain": "Inventory",
        "bullets": bullets,
        "summary": narrate_with_llm(bullets, "Inventory Analytics"),
    }