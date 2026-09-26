"""
F.R.I.D.A.Y. Digital Marketing & Web Agency Skills Seeder.
Equips F.R.I.D.A.Y. with specialized skills for marketing agencies, web developers,
and hosting administrators (Cloudflare, SEO decay, Meta Ads fatigue, WordPress, Shopify, HubSpot).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from friday_engine.config import FridayConfig
from friday_engine.core.engine import FridayEngine
from friday_engine.logger import logger


AGENCY_SKILLS_CATALOG = [
    {
        "name": "cloudflare_dns_waf_caching_optimizer",
        "description": "Calculates optimal Cloudflare Edge Cache TTL, Browser Cache TTL, SSL Full (Strict) requirements, and DDoS WAF rate limits.",
        "category": "marketing",
        "code": '''def calculate_cloudflare_rules(traffic_daily_requests: int, static_assets_pct: float = 70.0, is_ecommerce: bool = False) -> dict:
    edge_ttl_seconds = 7200 if is_ecommerce else 86400  # 2 hours for dynamic store, 24 hours for content
    browser_ttl_seconds = 14400 # 4 hours
    bandwidth_saved_pct = static_assets_pct * 0.90
    rate_limit_per_minute = max(100, int((traffic_daily_requests / (24 * 60)) * 5.0))
    return {
        "recommended_edge_cache_ttl_seconds": edge_ttl_seconds,
        "recommended_browser_cache_ttl_seconds": browser_ttl_seconds,
        "estimated_bandwidth_saved_pct": round(bandwidth_saved_pct, 1),
        "recommended_waf_rate_limit_per_ip_min": rate_limit_per_minute,
        "security_recommendations": [
            "Enable SSL/TLS Full (Strict) Mode with Cloudflare Origin CA Certificate",
            "Enable 'Always Use HTTPS' and HTTP/3 with QUIC",
            "Brotli Compression: Enabled",
            "Bot Fight Mode: Enabled for WordPress/Shopify endpoints"
        ]
    }''',
        "test_code": '''res = calculate_cloudflare_rules(100000, 75.0, False)
assert res["recommended_edge_cache_ttl_seconds"] == 86400
assert res["estimated_bandwidth_saved_pct"] > 60.0''',
        "metadata": {"tags": ["cloudflare", "dns", "cdn", "hosting", "web_development", "security"]}
    },
    {
        "name": "google_search_console_ctr_decay_audit",
        "description": "Audits Google Search Console data to identify keyword cannibalization, decaying rankings, and low-CTR high-impression opportunities.",
        "category": "marketing",
        "code": '''def audit_gsc_performance(queries_data: list) -> dict:
    opportunities = []
    cannibalization_warnings = []
    for q in queries_data:
        impressions = q.get("impressions", 0)
        clicks = q.get("clicks", 0)
        position = q.get("position", 50.0)
        ctr = (clicks / impressions * 100.0) if impressions > 0 else 0.0
        # High impression, low CTR in top 10 = Title/Meta copy fix opportunity
        if position <= 10.0 and impressions >= 1000 and ctr < 3.0:
            opportunities.append({
                "query": q.get("query"),
                "impressions": impressions,
                "clicks": clicks,
                "position": round(position, 1),
                "actual_ctr_pct": round(ctr, 2),
                "action": "REWRITE_TITLE_AND_META_DESCRIPTION (High impressions, underperforming CTR)"
            })
        if q.get("distinct_urls_ranking", 1) >= 2 and position <= 20.0:
            cannibalization_warnings.append({
                "query": q.get("query"),
                "ranking_urls_count": q.get("distinct_urls_ranking"),
                "action": "CONSOLIDATE_OR_CANONICALIZE (Multiple pages competing for same search term)"
            })
    return {
        "high_value_ctr_optimization_count": len(opportunities),
        "cannibalization_risks_count": len(cannibalization_warnings),
        "ctr_opportunities": opportunities[:5],
        "cannibalization_risks": cannibalization_warnings[:5]
    }''',
        "test_code": '''data = [{"query": "digital marketing agency", "impressions": 5000, "clicks": 50, "position": 4.2, "distinct_urls_ranking": 1}]
res = audit_gsc_performance(data)
assert res["high_value_ctr_optimization_count"] == 1
assert "REWRITE_TITLE" in res["ctr_opportunities"][0]["action"]''',
        "metadata": {"tags": ["seo", "google_search_console", "ctr", "ranking", "digital_marketing"]}
    },
    {
        "name": "meta_ads_creative_fatigue_detector",
        "description": "Calculates Ad Frequency vs. CPA degradation curves to flag ad fatigue and determine creative refresh schedules.",
        "category": "marketing",
        "code": '''def detect_ad_fatigue(ad_frequency: float, baseline_cpa: float, current_cpa: float, days_running: int) -> dict:
    cpa_increase_pct = ((current_cpa - baseline_cpa) / baseline_cpa) * 100.0 if baseline_cpa > 0 else 0.0
    is_fatigued = ad_frequency >= 2.5 and cpa_increase_pct >= 25.0
    action = "HEALTHY_CREATIVE"
    if ad_frequency >= 3.5:
        action = "CRITICAL_FATIGUE: Rotate creative immediately or expand audience targeting."
    elif is_fatigued:
        action = "EARLY_FATIGUE: Launch A/B test variations with new hook/thumbnail."
    elif days_running >= 30:
        action = "PROACTIVE_REFRESH: Ad running >30 days, prepare fresh creatives."
    return {
        "ad_frequency": ad_frequency,
        "cpa_increase_pct": round(cpa_increase_pct, 1),
        "creative_fatigued": is_fatigued,
        "recommended_action": action
    }''',
        "test_code": '''res = detect_ad_fatigue(2.8, 20.0, 28.0, 14)
assert res["creative_fatigued"] is True
assert "EARLY_FATIGUE" in res["recommended_action"]''',
        "metadata": {"tags": ["meta_ads", "facebook_ads", "cpa", "ad_fatigue", "advertising"]}
    },
    {
        "name": "website_core_web_vitals_auditor",
        "description": "Evaluates Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS) against Google SEO thresholds.",
        "category": "marketing",
        "code": '''def audit_core_web_vitals(lcp_seconds: float, inp_milliseconds: float, cls_score: float) -> dict:
    lcp_status = "GOOD" if lcp_seconds <= 2.5 else ("NEEDS_IMPROVEMENT" if lcp_seconds <= 4.0 else "POOR")
    inp_status = "GOOD" if inp_milliseconds <= 200.0 else ("NEEDS_IMPROVEMENT" if inp_milliseconds <= 500.0 else "POOR")
    cls_status = "GOOD" if cls_score <= 0.1 else ("NEEDS_IMPROVEMENT" if cls_score <= 0.25 else "POOR")
    all_good = lcp_status == "GOOD" and inp_status == "GOOD" and cls_status == "GOOD"
    return {
        "lcp_seconds": lcp_seconds,
        "lcp_rating": lcp_status,
        "inp_milliseconds": inp_milliseconds,
        "inp_rating": inp_status,
        "cls_score": cls_score,
        "cls_rating": cls_status,
        "passes_google_page_experience": all_good,
        "google_search_ranking_advantage": "ENABLED" if all_good else "PENALIZED_BY_PERFORMANCE"
    }''',
        "test_code": '''res = audit_core_web_vitals(1.8, 120.0, 0.04)
assert res["passes_google_page_experience"] is True
assert res["google_search_ranking_advantage"] == "ENABLED"''',
        "metadata": {"tags": ["core_web_vitals", "seo", "performance", "lcp", "inp", "cls", "web_development"]}
    },
    {
        "name": "hubspot_lead_scoring_mql_pipeline",
        "description": "Calculates behavioral lead scores based on pricing page visits, form submissions, and email engagement to qualify MQL/SQL status.",
        "category": "marketing",
        "code": '''def calculate_lead_score(pricing_page_visits: int, content_downloads: int, email_clicks: int, company_size_headcount: int) -> dict:
    score = 0
    score += min(40, pricing_page_visits * 15)
    score += min(30, content_downloads * 10)
    score += min(20, email_clicks * 5)
    if company_size_headcount >= 50:
        score += 25
    elif company_size_headcount >= 10:
        score += 15
    stage = "SUBSCRIBER"
    if score >= 80:
        stage = "SQL (Sales Qualified Lead - Route to Account Executive)"
    elif score >= 50:
        stage = "MQL (Marketing Qualified Lead - Trigger Automated Nurture Call)"
    elif score >= 25:
        stage = "LEAD (Enrolled in Educational Drip Sequence)"
    return {
        "composite_lead_score": score,
        "lifecycle_stage": stage,
        "ready_for_sales_outreach": score >= 80
    }''',
        "test_code": '''res = calculate_lead_score(3, 2, 4, 100)
assert res["composite_lead_score"] >= 80
assert res["ready_for_sales_outreach"] is True''',
        "metadata": {"tags": ["hubspot", "crm", "lead_scoring", "mql", "sql", "sales_pipeline"]}
    },
    {
        "name": "shopify_aov_cart_recovery_model",
        "description": "Models abandoned cart recovery sequence timing, dynamic discount elasticity, and Average Order Value (AOV) cross-sell uplift.",
        "category": "marketing",
        "code": '''def model_cart_recovery_sequence(cart_value_usd: float, customer_purchase_count: int) -> dict:
    discount_pct = 0.0 if customer_purchase_count >= 3 else (10.0 if cart_value_usd >= 100.0 else 5.0)
    return {
        "cart_value_usd": cart_value_usd,
        "recovery_cadence": [
            {"hour": 1, "channel": "EMAIL_SMS", "discount": "0%", "hook": "Did you leave something behind?"},
            {"hour": 24, "channel": "EMAIL", "discount": f"{discount_pct}%", "hook": "Exclusive limited-time offer for your cart."},
            {"hour": 48, "channel": "SMS_RETARGETING", "discount": f"{discount_pct}%", "hook": "Final 4 hours before your cart expires."}
        ],
        "recommended_post_purchase_upsell_usd": round(cart_value_usd * 0.25, 2),
        "target_cart_recovery_rate_pct": 18.5
    }''',
        "test_code": '''res = model_cart_recovery_sequence(150.0, 1)
assert len(res["recovery_cadence"]) == 3
assert res["recommended_post_purchase_upsell_usd"] == 37.5''',
        "metadata": {"tags": ["shopify", "e_commerce", "abandoned_cart", "aov", "email_marketing"]}
    },
    {
        "name": "agency_blended_roas_and_cpl_evaluator",
        "description": "Calculates Marketing Efficiency Ratio (MER / Blended ROAS), Cost Per Lead (CPL), and multi-channel marketing attribution.",
        "category": "marketing",
        "code": '''def calculate_agency_blended_metrics(total_ad_spend_all_channels: float, total_revenue_all_channels: float, total_leads_generated: int) -> dict:
    blended_roas = (total_revenue_all_channels / total_ad_spend_all_channels) if total_ad_spend_all_channels > 0 else 0.0
    cpl = (total_ad_spend_all_channels / total_leads_generated) if total_leads_generated > 0 else 0.0
    mer = blended_roas
    health = "EXCELLENT (Scaling Budget Permitted)" if mer >= 3.5 else ("STABLE (Maintain Spend)" if mer >= 2.0 else "UNPROFITABLE (Audit Attribution & CVR)")
    return {
        "blended_roas_mer": round(blended_roas, 2),
        "cost_per_lead_usd": round(cpl, 2),
        "agency_performance_tier": health,
        "is_scaling_recommended": mer >= 3.5
    }''',
        "test_code": '''res = calculate_agency_blended_metrics(10000.0, 42000.0, 250)
assert res["blended_roas_mer"] == 4.2
assert res["cost_per_lead_usd"] == 40.0
assert res["is_scaling_recommended"] is True''',
        "metadata": {"tags": ["marketing_agency", "roas", "mer", "cpl", "analytics", "attribution"]}
    }
]


def seed_agency_skills():
    logger.info("Initializing F.R.I.D.A.Y. Engine to register Digital Marketing & Agency Skills...")
    config = FridayConfig()
    engine = FridayEngine(config)
    
    total = len(AGENCY_SKILLS_CATALOG)
    logger.info(f"Seeding {total} digital marketing agency & hosting skills...")
    
    successful = 0
    for idx, skill in enumerate(AGENCY_SKILLS_CATALOG, 1):
        try:
            ok = engine.skill_store.save_skill(
                name=skill["name"],
                description=skill["description"],
                code=skill["code"],
                test_code=skill["test_code"],
                category=skill["category"],
                metadata=skill.get("metadata")
            )
            if ok:
                successful += 1
                logger.info(f"[{idx}/{total}] [OK] Seeded agency skill: {skill['name']}")
            else:
                logger.warning(f"[{idx}/{total}] [WARN] Failed to seed skill: {skill['name']}")
        except Exception as e:
            logger.error(f"[{idx}/{total}] [ERROR] Exception while seeding {skill['name']}: {e}")
            
    print(f"\nAGENCY SKILL SEEDING COMPLETE: {successful}/{total} skills stored and indexed in SQLite & SKILL.md!")

if __name__ == "__main__":
    seed_agency_skills()
