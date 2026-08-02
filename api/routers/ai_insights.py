"""
SHARED — AI Insights layer.
Both members plug their domain's KPI data into this. Design choice
worth explaining: it's rule-based by default (deterministic,
free, testable) with an OPTIONAL LLM call layered on top to turn
the numbers into a written narrative. Don't lead an interview with
"we used AI" — lead with the rule engine, then mention the LLM
narrative as a nice-to-have on top of real analysis.
"""
import os
from fastapi import APIRouter
from db import query

router = APIRouter(prefix="/insights", tags=["ai_insights"])

USE_LLM = bool(os.environ.get("ANTHROPIC_API_KEY"))


def rule_based_sales_insights():
    at_risk = query("""
        select count(*) as n from marts.fct_customer_ltv where at_risk_flag = true
    """)[0]["n"]
    top_region = query("""
        select region, sum(total_revenue) as rev
        from marts.fct_monthly_revenue
        group by region order by rev desc limit 1
    """)
    insights = [f"{at_risk} customers have not ordered in 90+ days and are at risk of churn."]
    if top_region:
        insights.append(f"{top_region[0]['region']} is the top-performing region by revenue.")
    return insights


def rule_based_inventory_insights():
    reorder = query("""
        select count(*) as n from marts.fct_inventory_health where needs_reorder = true
    """)[0]["n"]
    worst_return = query("""
        select product_name, return_rate from marts.fct_return_analysis
        order by return_rate desc limit 1
    """)
    insights = [f"{reorder} products are below their reorder threshold and need restocking."]
    if worst_return:
        insights.append(
            f"'{worst_return[0]['product_name']}' has the highest return rate "
            f"at {round(worst_return[0]['return_rate'] * 100, 1)}%."
        )
    return insights


def narrate_with_llm(bullet_points: list[str], domain: str) -> str:
    """Optional: turn structured bullets into a short executive narrative.
    Falls back to a plain join if no API key is configured — the
    dashboard should never break just because the LLM key is missing.
    """
    if not USE_LLM:
        return " ".join(bullet_points)
    try:
        import anthropic
        client = anthropic.Anthropic()
        prompt = (
            f"Write a 2-sentence executive summary for a {domain} dashboard "
            f"based on these facts: {'; '.join(bullet_points)}. "
            f"Be concise and factual, no fluff."
        )
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text
    except Exception as e:
        return " ".join(bullet_points) + f" (LLM narration unavailable: {e})"


@router.get("/sales")
def sales_insights():
    bullets = rule_based_sales_insights()
    return {"bullets": bullets, "summary": narrate_with_llm(bullets, "sales")}


@router.get("/inventory")
def inventory_insights():
    bullets = rule_based_inventory_insights()
    return {"bullets": bullets, "summary": narrate_with_llm(bullets, "inventory")}
