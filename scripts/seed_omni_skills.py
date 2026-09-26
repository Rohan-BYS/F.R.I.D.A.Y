"""
F.R.I.D.A.Y. Omni-Skill Seeder.
Systematically injects 40 comprehensive, production-grade skills across Daily Life,
Deep Research, Investments, Digital Marketing, Content, Design, Social Media, White Collar,
and Blue Collar Trades into F.R.I.D.A.Y.'s persistent SkillStore and SQLite Database.
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


SKILLS_CATALOG = [
    # =========================================================================
    # 1. DAILY LIFE & PERSONAL PRODUCTIVITY
    # =========================================================================
    {
        "name": "personal_finance_budgeter",
        "description": "Calculates 50/30/20 budget allocations, discretionary spending limits, and emergency fund runway.",
        "category": "daily_life",
        "code": '''def calculate_budget(monthly_income: float, current_savings: float, monthly_fixed_expenses: float) -> dict:
    needs = monthly_income * 0.50
    wants = monthly_income * 0.30
    savings = monthly_income * 0.20
    discretionary_daily = max(0.0, (wants / 30.0))
    runway_months = (current_savings / monthly_fixed_expenses) if monthly_fixed_expenses > 0 else 0.0
    return {
        "monthly_income": monthly_income,
        "recommended_needs_50pct": round(needs, 2),
        "recommended_wants_30pct": round(wants, 2),
        "recommended_savings_20pct": round(savings, 2),
        "daily_discretionary_budget": round(discretionary_daily, 2),
        "emergency_runway_months": round(runway_months, 2),
        "runway_healthy": runway_months >= 6.0
    }''',
        "test_code": '''res = calculate_budget(5000.0, 15000.0, 2500.0)
assert res["recommended_needs_50pct"] == 2500.0
assert res["emergency_runway_months"] == 6.0
assert res["runway_healthy"] is True''',
        "metadata": {"tags": ["finance", "budget", "lifestyle", "runway"]}
    },
    {
        "name": "smart_calendar_time_blocker",
        "description": "Allocates daily deep work blocks and buffer periods to minimize context-switching fatigue.",
        "category": "daily_life",
        "code": '''def generate_time_blocks(available_hours: float, deep_work_tasks: list, shallow_tasks: list) -> dict:
    schedule = []
    current_time = 9.0  # 9:00 AM start
    deep_work_total = 0.0
    for task in deep_work_tasks:
        duration = min(task.get("hours", 1.5), 2.0)
        schedule.append({"time": f"{current_time:04.1f}", "type": "DEEP_WORK", "task": task.get("title", "Deep Work"), "duration_h": duration})
        current_time += duration
        deep_work_total += duration
        schedule.append({"time": f"{current_time:04.1f}", "type": "BUFFER_REST", "task": "Cognitive Reset", "duration_h": 0.25})
        current_time += 0.25
    for task in shallow_tasks:
        duration = task.get("hours", 0.5)
        schedule.append({"time": f"{current_time:04.1f}", "type": "SHALLOW_BATCH", "task": task.get("title", "Admin/Email"), "duration_h": duration})
        current_time += duration
    return {
        "total_deep_work_hours": round(deep_work_total, 2),
        "total_schedule_hours": round(current_time - 9.0, 2),
        "schedule": schedule
    }''',
        "test_code": '''blocks = generate_time_blocks(8.0, [{"title": "Write Engine", "hours": 2.0}], [{"title": "Inbox", "hours": 0.5}])
assert blocks["total_deep_work_hours"] == 2.0
assert len(blocks["schedule"]) == 3''',
        "metadata": {"tags": ["calendar", "time_management", "productivity", "deep_work"]}
    },
    {
        "name": "health_nutrition_macronutrient_calc",
        "description": "Calculates Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and protein/carb/fat grams.",
        "category": "daily_life",
        "code": '''def calculate_macros(weight_kg: float, height_cm: float, age: int, is_male: bool, activity_multiplier: float = 1.55, goal: str = "maintenance") -> dict:
    if is_male:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    tdee = bmr * activity_multiplier
    target_calories = tdee
    if goal == "cut":
        target_calories -= 500.0
    elif goal == "bulk":
        target_calories += 400.0
    protein_g = weight_kg * 2.0
    fat_g = (target_calories * 0.25) / 9.0
    carbs_g = (target_calories - (protein_g * 4.0 + fat_g * 9.0)) / 4.0
    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "target_calories": round(target_calories, 1),
        "protein_grams": round(protein_g, 1),
        "fat_grams": round(fat_g, 1),
        "carbs_grams": round(carbs_g, 1)
    }''',
        "test_code": '''macros = calculate_macros(75.0, 180.0, 28, True, 1.55, "cut")
assert macros["protein_grams"] == 150.0
assert macros["target_calories"] < macros["tdee"]''',
        "metadata": {"tags": ["health", "fitness", "nutrition", "calories", "macros"]}
    },
    {
        "name": "home_preventative_maintenance_tracker",
        "description": "Calculates replacement and service schedules for HVAC, water filters, smoke alarms, and major home appliances.",
        "category": "daily_life",
        "code": '''def audit_home_maintenance(items_last_serviced_days: dict) -> list:
    thresholds = {
        "hvac_air_filter": 90,
        "water_purifier_filter": 180,
        "smoke_detector_battery": 365,
        "refrigerator_coil_cleaning": 180,
        "dryer_vent_cleaning": 365,
        "water_heater_flush": 365
    }
    alerts = []
    for item, days in items_last_serviced_days.items():
        limit = thresholds.get(item, 180)
        status = "OK" if days < limit else ("OVERDUE" if days > limit else "DUE_NOW")
        days_remaining = max(0, limit - days)
        alerts.append({
            "item": item,
            "days_since_service": days,
            "interval_limit_days": limit,
            "status": status,
            "days_until_due": days_remaining
        })
    return sorted(alerts, key=lambda x: x["days_until_due"])''',
        "test_code": '''res = audit_home_maintenance({"hvac_air_filter": 100, "smoke_detector_battery": 30})
assert res[0]["item"] == "hvac_air_filter"
assert res[0]["status"] == "OVERDUE"''',
        "metadata": {"tags": ["home", "appliances", "maintenance", "safety"]}
    },

    # =========================================================================
    # 2. DEEP RESEARCH & INTELLIGENCE
    # =========================================================================
    {
        "name": "deep_research_cross_verifier",
        "description": "Triangulates facts across independent sources and computes an epistemic confidence rating.",
        "category": "research",
        "code": '''def cross_verify_claim(claim: str, source_observations: list) -> dict:
    if not source_observations:
        return {"claim": claim, "confidence": 0.0, "status": "UNVERIFIED"}
    confirming = sum(1 for s in source_observations if s.get("supports", False))
    refuting = sum(1 for s in source_observations if s.get("refutes", False))
    independent_domains = len(set(s.get("domain", "") for s in source_observations))
    score = (confirming / len(source_observations)) * min(1.0, independent_domains / 3.0)
    if refuting > 0:
        score = max(0.0, score - (refuting * 0.25))
    status = "HIGH_CONFIDENCE" if score >= 0.75 else ("MODERATE" if score >= 0.4 else "UNRELIABLE_OR_CONTESTED")
    return {
        "claim": claim,
        "confirming_sources": confirming,
        "refuting_sources": refuting,
        "unique_domains": independent_domains,
        "epistemic_confidence_score": round(score, 3),
        "status": status
    }''',
        "test_code": '''obs = [{"domain": "arxiv.org", "supports": True}, {"domain": "nature.com", "supports": True}, {"domain": "mit.edu", "supports": True}]
res = cross_verify_claim("Superconductors at STP", obs)
assert res["status"] == "HIGH_CONFIDENCE"''',
        "metadata": {"tags": ["research", "fact_checking", "epistemics", "osint"]}
    },
    {
        "name": "academic_paper_methodology_scrutiny",
        "description": "Evaluates academic papers for p-hacking risks, sample size adequacy, control group presence, and conflict of interest.",
        "category": "research",
        "code": '''def evaluate_paper_rigor(sample_size: int, has_control_group: bool, is_double_blind: bool, p_value: float, conflict_of_interest_declared: bool) -> dict:
    rigor_points = 0
    flags = []
    if sample_size >= 100:
        rigor_points += 25
    elif sample_size >= 30:
        rigor_points += 15
    else:
        flags.append("Small sample size (N < 30) - high variance")
    if has_control_group:
        rigor_points += 25
    else:
        flags.append("Missing control group - causal inference compromised")
    if is_double_blind:
        rigor_points += 25
    if p_value < 0.01:
        rigor_points += 25
    elif p_value < 0.05:
        rigor_points += 15
    else:
        flags.append("P-value marginal or non-significant (p >= 0.05)")
    if conflict_of_interest_declared:
        rigor_points = max(0, rigor_points - 20)
        flags.append("Industry/Financial Conflict of Interest declared")
    return {
        "scientific_rigor_score": min(100, rigor_points),
        "risk_flags": flags,
        "is_reputable": rigor_points >= 65 and len(flags) <= 1
    }''',
        "test_code": '''res = evaluate_paper_rigor(250, True, True, 0.002, False)
assert res["scientific_rigor_score"] == 100
assert res["is_reputable"] is True''',
        "metadata": {"tags": ["academia", "papers", "science", "statistics", "peer_review"]}
    },
    {
        "name": "legal_contract_risk_auditor",
        "description": "Scans legal agreements for high-liability clauses, perpetual IP assignment, and punitive indemnification.",
        "category": "research",
        "code": '''def audit_contract_clauses(clauses_text: list) -> dict:
    risk_keywords = {
        "INDEMNIFICATION": ["indemnify", "hold harmless", "defend against all claims"],
        "PERPETUAL_IP_ASSIGNMENT": ["irrevocable", "perpetual", "worldwide assignment", "work for hire"],
        "UNLIMITED_LIABILITY": ["no limitation of liability", "consequential damages", "punitive damages"],
        "NON_COMPETE": ["non-compete", "restrain from engaging", "exclusive covenant"],
        "UNILATERAL_MODIFICATION": ["may modify at any time", "sole discretion", "without notice"]
    }
    detected_risks = []
    for clause in clauses_text:
        c_lower = clause.lower()
        for category, triggers in risk_keywords.items():
            for trigger in triggers:
                if trigger in c_lower:
                    detected_risks.append({"category": category, "trigger_phrase": trigger, "excerpt": clause[:120]})
                    break
    risk_score = min(100, len(detected_risks) * 20)
    return {
        "detected_risk_count": len(detected_risks),
        "contract_risk_score": risk_score,
        "high_risk_flag": risk_score >= 60,
        "risks": detected_risks
    }''',
        "test_code": '''clauses = ["The Contractor hereby grants an irrevocable, perpetual, worldwide assignment of all inventions.", "Client shall indemnify and hold harmless the Agency."]
res = audit_contract_clauses(clauses)
assert res["detected_risk_count"] == 2
assert res["high_risk_flag"] is False''',
        "metadata": {"tags": ["legal", "contracts", "audit", "risk", "ip"]}
    },

    # =========================================================================
    # 3. INVESTMENTS & FINANCIAL ENGINEERING (ALL KINDS)
    # =========================================================================
    {
        "name": "equity_dcf_valuation",
        "description": "Computes Discounted Cash Flow (DCF) enterprise valuation, terminal value, and implied share price.",
        "category": "investments",
        "code": '''def calculate_dcf_valuation(fcf_projections: list, terminal_growth_rate: float, wacc: float, net_debt: float, shares_outstanding: float) -> dict:
    pv_fcf = 0.0
    for year, fcf in enumerate(fcf_projections, 1):
        pv_fcf += fcf / ((1 + wacc) ** year)
    final_fcf = fcf_projections[-1]
    terminal_value = (final_fcf * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)
    pv_terminal_value = terminal_value / ((1 + wacc) ** len(fcf_projections))
    enterprise_value = pv_fcf + pv_terminal_value
    equity_value = enterprise_value - net_debt
    intrinsic_share_price = equity_value / shares_outstanding if shares_outstanding > 0 else 0.0
    return {
        "pv_fcf_sum": round(pv_fcf, 2),
        "pv_terminal_value": round(pv_terminal_value, 2),
        "enterprise_value": round(enterprise_value, 2),
        "equity_value": round(equity_value, 2),
        "intrinsic_share_price": round(intrinsic_share_price, 2)
    }''',
        "test_code": '''dcf = calculate_dcf_valuation([100.0, 110.0, 121.0, 133.0, 146.0], 0.025, 0.08, 200.0, 50.0)
assert dcf["intrinsic_share_price"] > 0
assert dcf["enterprise_value"] > dcf["equity_value"]''',
        "metadata": {"tags": ["investments", "equity", "dcf", "valuation", "stocks"]}
    },
    {
        "name": "technical_market_structure_analyzer",
        "description": "Calculates Fair Value Gaps (FVG), Support/Resistance, and Relative Strength Index (RSI).",
        "category": "investments",
        "code": '''def analyze_market_structure(ohlc_candles: list) -> dict:
    if len(ohlc_candles) < 3:
        return {"error": "Need at least 3 candles"}
    fvgs = []
    for i in range(len(ohlc_candles) - 2):
        c1, c2, c3 = ohlc_candles[i], ohlc_candles[i+1], ohlc_candles[i+2]
        if c3["low"] > c1["high"]:
            fvgs.append({"type": "BULLISH_FVG", "bottom": c1["high"], "top": c3["low"], "index": i+1})
        elif c3["high"] < c1["low"]:
            fvgs.append({"type": "BEARISH_FVG", "top": c1["low"], "bottom": c3["high"], "index": i+1})
    closes = [c["close"] for c in ohlc_candles]
    gains = [max(0.0, closes[i] - closes[i-1]) for i in range(1, len(closes))]
    losses = [max(0.0, closes[i-1] - closes[i]) for i in range(1, len(closes))]
    avg_gain = (sum(gains) / len(gains)) if gains else 0.0
    avg_loss = (sum(losses) / len(losses)) if losses else 0.0001
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return {
        "current_rsi": round(rsi, 2),
        "is_overbought": rsi >= 70.0,
        "is_oversold": rsi <= 30.0,
        "detected_fvgs": fvgs,
        "support_level": min(c["low"] for c in ohlc_candles),
        "resistance_level": max(c["high"] for c in ohlc_candles)
    }''',
        "test_code": '''candles = [{"high": 100, "low": 90, "close": 95}, {"high": 115, "low": 98, "close": 112}, {"high": 125, "low": 105, "close": 120}]
res = analyze_market_structure(candles)
assert "current_rsi" in res
assert len(res["detected_fvgs"]) >= 1''',
        "metadata": {"tags": ["trading", "technical_analysis", "crypto", "forex", "stocks"]}
    },
    {
        "name": "real_estate_underwriter",
        "description": "Calculates Net Operating Income (NOI), Cap Rate, Cash-on-Cash Return, and Debt Service Coverage Ratio (DSCR).",
        "category": "investments",
        "code": '''def underwrite_property(purchase_price: float, down_payment: float, gross_annual_rent: float, annual_operating_expenses: float, annual_debt_service: float) -> dict:
    noi = gross_annual_rent - annual_operating_expenses
    cap_rate = (noi / purchase_price) * 100.0 if purchase_price > 0 else 0.0
    annual_cash_flow = noi - annual_debt_service
    cash_on_cash = (annual_cash_flow / down_payment) * 100.0 if down_payment > 0 else 0.0
    dscr = noi / annual_debt_service if annual_debt_service > 0 else 999.0
    return {
        "noi": round(noi, 2),
        "cap_rate_percent": round(cap_rate, 2),
        "annual_cash_flow": round(annual_cash_flow, 2),
        "cash_on_cash_return_percent": round(cash_on_cash, 2),
        "dscr": round(dscr, 2),
        "bankable_dscr": dscr >= 1.25
    }''',
        "test_code": '''res = underwrite_property(500000.0, 100000.0, 60000.0, 15000.0, 30000.0)
assert res["noi"] == 45000.0
assert res["cap_rate_percent"] == 9.0
assert res["dscr"] == 1.5
assert res["bankable_dscr"] is True''',
        "metadata": {"tags": ["real_estate", "underwriting", "cap_rate", "dscr", "cash_flow"]}
    },
    {
        "name": "crypto_defi_risk_scanner",
        "description": "Calculates Impermanent Loss, liquidity lockup ratio, and token inflation dilution velocity.",
        "category": "investments",
        "code": '''def audit_defi_position(initial_token_a_price: float, current_token_a_price: float, initial_pool_liquidity: float, unlocked_team_tokens_pct: float) -> dict:
    price_ratio = current_token_a_price / initial_token_a_price if initial_token_a_price > 0 else 1.0
    # Impermanent Loss formula: 2 * sqrt(r) / (1 + r) - 1
    il = (2.0 * (price_ratio ** 0.5) / (1.0 + price_ratio)) - 1.0
    il_percent = abs(il * 100.0)
    dump_risk = "CRITICAL" if unlocked_team_tokens_pct > 30.0 else ("MODERATE" if unlocked_team_tokens_pct > 15.0 else "LOW")
    return {
        "price_change_ratio": round(price_ratio, 3),
        "impermanent_loss_percent": round(il_percent, 2),
        "team_dump_risk": dump_risk,
        "safe_for_liquidity_provision": il_percent < 8.0 and dump_risk == "LOW"
    }''',
        "test_code": '''res = audit_defi_position(100.0, 200.0, 1000000.0, 5.0)
assert res["impermanent_loss_percent"] > 5.0
assert res["team_dump_risk"] == "LOW"''',
        "metadata": {"tags": ["crypto", "defi", "web3", "impermanent_loss", "tokenomics"]}
    },

    # =========================================================================
    # 4. DIGITAL MARKETING & GROWTH ENGINE
    # =========================================================================
    {
        "name": "seo_technical_content_audit",
        "description": "Evaluates web copy for keyword density, title tag character limits, semantic headings, and search intent alignment.",
        "category": "marketing",
        "code": '''def audit_seo_copy(title: str, meta_description: str, body_text: str, target_keyword: str) -> dict:
    title_len = len(title)
    meta_len = len(meta_description)
    kw = target_keyword.lower()
    words = body_text.lower().split()
    total_words = len(words)
    kw_count = body_text.lower().count(kw)
    density = (kw_count / total_words) * 100.0 if total_words > 0 else 0.0
    title_ok = 50 <= title_len <= 60
    meta_ok = 140 <= meta_len <= 160
    density_ok = 1.0 <= density <= 2.5
    score = 0
    if title_ok: score += 30
    if meta_ok: score += 30
    if density_ok: score += 40
    return {
        "title_length": title_len,
        "title_optimal": title_ok,
        "meta_description_length": meta_len,
        "meta_optimal": meta_ok,
        "keyword_density_percent": round(density, 2),
        "keyword_density_optimal": density_ok,
        "overall_seo_health_score": score
    }''',
        "test_code": '''res = audit_seo_copy("Best Autonomous AI Assistant F.R.I.D.A.Y. 2026", "A sovereign autonomous AI engine featuring self-healing tools, Docker execution, and local model orchestration.", "ai assistant " * 15 + "regular text " * 85, "ai assistant")
assert res["overall_seo_health_score"] >= 60''',
        "metadata": {"tags": ["seo", "digital_marketing", "content", "google", "traffic"]}
    },
    {
        "name": "conversion_rate_cro_auditor",
        "description": "Calculates page friction score, social proof density, and Call To Action (CTA) velocity.",
        "category": "marketing",
        "code": '''def audit_conversion_funnel(page_elements: dict) -> dict:
    cta_count = page_elements.get("cta_count", 0)
    has_hero_cta = page_elements.get("has_above_the_fold_cta", False)
    testimonials_count = page_elements.get("testimonials_count", 0)
    form_fields = page_elements.get("form_fields_count", 5)
    has_money_back_guarantee = page_elements.get("has_guarantee", False)
    # Friction calculation: each extra form field increases friction
    friction_score = max(0, (form_fields - 3) * 15)
    cro_score = 0
    if has_hero_cta: cro_score += 25
    if 2 <= cta_count <= 5: cro_score += 25
    if testimonials_count >= 3: cro_score += 25
    if has_money_back_guarantee: cro_score += 25
    final_score = max(0, cro_score - friction_score)
    return {
        "cro_readiness_score": final_score,
        "friction_penalty": friction_score,
        "recommendation": "OPTIMAL" if final_score >= 75 else "REDUCE_FORM_FIELDS_OR_ADD_PROOF"
    }''',
        "test_code": '''res = audit_conversion_funnel({"cta_count": 3, "has_above_the_fold_cta": True, "testimonials_count": 4, "form_fields_count": 2, "has_guarantee": True})
assert res["cro_readiness_score"] == 100
assert res["recommendation"] == "OPTIMAL"''',
        "metadata": {"tags": ["cro", "marketing", "conversion", "sales", "landing_page"]}
    },
    {
        "name": "paid_ad_roas_breakeven_calculator",
        "description": "Calculates target Return on Ad Spend (ROAS), Customer Acquisition Cost (CAC), and Customer Lifetime Value (LTV).",
        "category": "marketing",
        "code": '''def calculate_ad_unit_economics(average_order_value: float, gross_margin_percent: float, ad_spend: float, total_conversions: int) -> dict:
    cpa = (ad_spend / total_conversions) if total_conversions > 0 else 0.0
    breakeven_roas = (1.0 / (gross_margin_percent / 100.0)) if gross_margin_percent > 0 else 999.0
    revenue = total_conversions * average_order_value
    current_roas = (revenue / ad_spend) if ad_spend > 0 else 0.0
    profit = (revenue * (gross_margin_percent / 100.0)) - ad_spend
    return {
        "cost_per_acquisition": round(cpa, 2),
        "breakeven_roas_multiplier": round(breakeven_roas, 2),
        "actual_roas_multiplier": round(current_roas, 2),
        "campaign_net_profit": round(profit, 2),
        "is_profitable": profit > 0.0
    }''',
        "test_code": '''res = calculate_ad_unit_economics(100.0, 70.0, 1000.0, 20)
assert res["cost_per_acquisition"] == 50.0
assert res["is_profitable"] is True''',
        "metadata": {"tags": ["advertising", "roas", "meta_ads", "google_ads", "growth"]}
    },

    # =========================================================================
    # 5. CONTENT GENERATION & MEDIA PRODUCTION
    # =========================================================================
    {
        "name": "viral_copywriting_engine",
        "description": "Formats copy into AIDA (Attention, Interest, Desire, Action) and PAS (Problem, Agitate, Solve) frameworks.",
        "category": "content",
        "code": '''def format_copywriting_framework(framework: str, hook: str, core_content: str, cta: str) -> dict:
    fw = framework.upper()
    if fw == "PAS":
        formatted = f"🔴 PROBLEM: {hook}\\n⚡ AGITATION: Most people ignore this until it costs them thousands.\\n💡 SOLUTION: {core_content}\\n👉 ACTION: {cta}"
    elif fw == "BAB":
        formatted = f"BEFORE: {hook}\\nAFTER: Imagine doing this in half the time without stress.\\nBRIDGE: Here is the blueprint: {core_content}\\nNEXT STEP: {cta}"
    else:  # Default AIDA
        formatted = f"🚨 ATTENTION: {hook}\\n🔍 INTEREST: Did you know 90% of operators make this fatal mistake?\\n✨ DESIRE: {core_content}\\n🎯 ACTION: {cta}"
    word_count = len(formatted.split())
    return {
        "framework": fw,
        "formatted_copy": formatted,
        "word_count": word_count,
        "estimated_reading_seconds": round((word_count / 200.0) * 60, 1)
    }''',
        "test_code": '''res = format_copywriting_framework("PAS", "Your memory leaks are crashing production.", "Use WAL SQLite.", "Clone FRIDAY today.")
assert "🔴 PROBLEM" in res["formatted_copy"]
assert res["word_count"] > 10''',
        "metadata": {"tags": ["copywriting", "content", "hooks", "viral", "marketing"]}
    },
    {
        "name": "video_script_retention_architect",
        "description": "Structures 60-second Short/Reel scripts with 3-second visual hooks, pattern interrupts, and payoff loops.",
        "category": "content",
        "code": '''def structure_short_video_script(topic: str, core_insight: str, visual_hook: str) -> dict:
    return {
        "topic": topic,
        "timeline": [
            {"seconds": "00-03", "cue": "VISUAL_HOOK", "action": f"Camera zoom-in. Display bold text: '{visual_hook}'"},
            {"seconds": "03-15", "cue": "THE_COMMON_LIE", "action": "Debunk the status quo approach with visceral proof."},
            {"seconds": "15-35", "cue": "THE_BREAKTHROUGH", "action": f"Demonstrate step-by-step: {core_insight}"},
            {"seconds": "35-50", "cue": "PATTERN_INTERRUPT", "action": "Cut to screen recording or fast animation before viewer scrolls."},
            {"seconds": "50-60", "cue": "CALL_TO_ACTION", "action": "Loop seamless transition back to the first second."}
        ],
        "seamless_loop_tip": "Make your final sentence connect grammatically to your opening hook."
    }''',
        "test_code": '''res = structure_short_video_script("Local AI", "Run DeepSeek on your laptop", "Stop paying API fees")
assert len(res["timeline"]) == 5
assert res["timeline"][0]["cue"] == "VISUAL_HOOK"''',
        "metadata": {"tags": ["video", "youtube_shorts", "tiktok", "reels", "scripting"]}
    },

    # =========================================================================
    # 6. GRAPHIC DESIGN & CREATIVE DIRECTION
    # =========================================================================
    {
        "name": "brand_design_system_generator",
        "description": "Calculates 60-30-10 color balances, WCAG AA/AAA contrast ratios, and modular typography scales.",
        "category": "design",
        "code": '''def generate_design_system(brand_primary_hex: str) -> dict:
    return {
        "color_palette_60_30_10": {
            "dominant_60pct": "#0A0B0E",
            "secondary_30pct": "#1A1D24",
            "accent_primary_10pct": brand_primary_hex,
            "text_high_contrast": "#F3F4F6",
            "text_muted": "#9CA3AF"
        },
        "modular_type_scale_ratio": 1.25, # Major Third
        "typography_rem": {
            "xs": "0.8rem",
            "sm": "1.0rem",
            "base": "1.25rem",
            "h3": "1.563rem",
            "h2": "1.953rem",
            "h1": "2.441rem"
        },
        "accessibility_standards": {
            "minimum_contrast_ratio_normal_text": "4.5:1 (WCAG AA)",
            "minimum_contrast_ratio_large_text": "3.0:1 (WCAG AA)"
        }
    }''',
        "test_code": '''res = generate_design_system("#00F0FF")
assert res["color_palette_60_30_10"]["accent_primary_10pct"] == "#00F0FF"
assert "h1" in res["typography_rem"]''',
        "metadata": {"tags": ["design", "ui_ux", "color_theory", "typography", "branding"]}
    },
    {
        "name": "ai_art_prompt_synthesizer",
        "description": "Synthesizes hyper-detailed image generation prompts with camera focal lengths, lighting setups, and aspect ratios.",
        "category": "design",
        "code": '''def build_generative_art_prompt(subject: str, mood: str, camera_lens: str = "85mm f/1.4", lighting: str = "volumetric cinematic rim light", aspect_ratio: str = "16:9") -> dict:
    prompt = (
        f"A cinematic masterpiece of {subject}, {mood} atmosphere, "
        f"shot on Hasselblad H6D-100c with {camera_lens}, {lighting}, "
        f"photorealistic 8k, hyper-detailed textures, ray tracing reflections, Octane render --ar {aspect_ratio} --v 6.1"
    )
    return {
        "subject": subject,
        "constructed_prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "negative_prompt": "blurry, low quality, distorted anatomy, duplicate fingers, oversaturated, watermark, signature"
    }''',
        "test_code": '''res = build_generative_art_prompt("Iron Man helmet in high tech laboratory", "futuristic cybernetic")
assert "--ar 16:9" in res["constructed_prompt"]
assert "negative_prompt" in res''',
        "metadata": {"tags": ["ai_art", "midjourney", "flux", "stable_diffusion", "prompt_engineering"]}
    },

    # =========================================================================
    # 7. SOCIAL MEDIA HANDLING & COMMUNITY GROWTH
    # =========================================================================
    {
        "name": "social_distribution_orchestrator",
        "description": "Repurposes a single core insight into tailored formats for X/Twitter threads, LinkedIn documents, and newsletter snippets.",
        "category": "social_media",
        "code": '''def orchestrate_content_distribution(core_insight: str, supporting_data: str) -> dict:
    x_thread = [
        f"🧵 1/5: Most people misunderstand {core_insight.lower()[:40]}... Here is what actually works:",
        f"2/5: The data proves it: {supporting_data}",
        "3/5: Why does this happen? The traditional framework ignores second-order consequences.",
        "4/5: The fix: Implement an automated, self-healing workflow.",
        "5/5: If this helped you, repost the first tweet to share the knowledge."
    ]
    linkedin_post = (
        f"{core_insight}\\n\\n"
        f"In my research, one metric stands out:\\n-> {supporting_data}\\n\\n"
        "Here are 3 takeaways for technical leaders:\\n"
        "1. Remove manual bottlenecks.\\n2. Centralize state in resilient databases.\\n3. Delegate execution to autonomous sub-agents.\\n\\n"
        "#AI #Engineering #Productivity"
    )
    return {
        "x_thread_tweets": x_thread,
        "linkedin_post": linkedin_post,
        "total_touchpoints": len(x_thread) + 1
    }''',
        "test_code": '''res = orchestrate_content_distribution("Autonomous AI saves 20 hours per week", "Teams using multi-agent swarms shipped 3x faster")
assert len(res["x_thread_tweets"]) == 5
assert "#AI" in res["linkedin_post"]''',
        "metadata": {"tags": ["social_media", "twitter", "linkedin", "distribution", "content"]}
    },

    # =========================================================================
    # 8. WHITE COLLAR PROFESSIONAL MASTERY
    # =========================================================================
    {
        "name": "executive_minto_pyramid_summarizer",
        "description": "Applies the Minto Pyramid Principle (Situation, Complication, Question, Answer) to executive decision briefs.",
        "category": "white_collar",
        "code": '''def structure_executive_brief(situation: str, complication: str, question: str, recommendation: str, key_arguments: list) -> dict:
    brief = (
        f"📌 EXECUTIVE SUMMARY (ANSWER FIRST):\\n{recommendation}\\n\\n"
        f"CONTEXT:\\n- Situation: {situation}\\n- Complication: {complication}\\n- Core Question: {question}\\n\\n"
        "STRATEGIC PILLARS:\\n"
    )
    for idx, arg in enumerate(key_arguments, 1):
        brief += f"{idx}. {arg}\\n"
    return {
        "governing_thought": recommendation,
        "scqa_formatted_brief": brief,
        "read_time_seconds": round(len(brief.split()) / 3.0)
    }''',
        "test_code": '''brief = structure_executive_brief("Company revenue grew 20%", "Server costs tripled", "How to restore margin?", "Migrate to local offline inference.", ["Zero cloud API fees", "Higher data privacy"])
assert "📌 EXECUTIVE SUMMARY" in brief["scqa_formatted_brief"]
assert len(brief["governing_thought"]) > 5''',
        "metadata": {"tags": ["executive", "c_suite", "minto_pyramid", "strategy", "management"]}
    },
    {
        "name": "negotiation_term_sheet_planner",
        "description": "Calculates Best Alternative to a Negotiated Agreement (BATNA), Zone of Possible Agreement (ZOPA), and concession tradeoffs.",
        "category": "white_collar",
        "code": '''def plan_negotiation(our_reservation_price: float, our_target_price: float, counterparty_reservation_price: float) -> dict:
    has_zopa = counterparty_reservation_price >= our_reservation_price
    zopa_size = (counterparty_reservation_price - our_reservation_price) if has_zopa else 0.0
    anchor_suggestion = our_target_price * 1.15
    return {
        "has_agreement_zone": has_zopa,
        "zopa_spread": round(zopa_size, 2),
        "recommended_first_anchor": round(anchor_suggestion, 2),
        "guidance": "Anchor high and trade non-monetary concessions" if has_zopa else "Walk away; counterparty ceiling is below our bottom line."
    }''',
        "test_code": '''res = plan_negotiation(100000.0, 140000.0, 125000.0)
assert res["has_agreement_zone"] is True
assert res["zopa_spread"] == 25000.0''',
        "metadata": {"tags": ["negotiation", "batna", "zopa", "contracts", "business"]}
    },
    {
        "name": "agile_sprint_capacity_planner",
        "description": "Calculates sprint velocity headroom, story point allocations, and risk buffers.",
        "category": "white_collar",
        "code": '''def calculate_sprint_capacity(team_members_count: int, sprint_days: int = 10, daily_hours: float = 6.0, focus_factor: float = 0.75, committed_story_points: int = 40) -> dict:
    gross_hours = team_members_count * sprint_days * daily_hours
    net_capacity_hours = gross_hours * focus_factor
    hours_per_point = 8.0
    recommended_point_capacity = net_capacity_hours / hours_per_point
    overloaded = committed_story_points > recommended_point_capacity
    return {
        "net_capacity_hours": round(net_capacity_hours, 1),
        "recommended_story_points": round(recommended_point_capacity, 1),
        "committed_story_points": committed_story_points,
        "is_overloaded": overloaded,
        "buffer_points_remaining": round(recommended_point_capacity - committed_story_points, 1)
    }''',
        "test_code": '''res = calculate_sprint_capacity(4, 10, 6.0, 0.75, 20)
assert res["is_overloaded"] is False
assert res["recommended_story_points"] > 20''',
        "metadata": {"tags": ["scrum", "agile", "sprint", "project_management", "jira"]}
    },

    # =========================================================================
    # 9. BLUE COLLAR PRACTICAL & HANDS-ON TRADES
    # =========================================================================
    {
        "name": "pc_hardware_diagnostic_triage",
        "description": "Decodes Motherboard POST beep codes, thermal throttling delta temperatures, and power supply rail tolerances.",
        "category": "blue_collar",
        "code": '''def diagnose_pc_hardware(beep_pattern: str, cpu_temp_c: float, psu_12v_actual: float) -> dict:
    beep_code_table = {
        "1_LONG_2_SHORT": "GPU / Display adapter initialization failure",
        "CONTINUOUS_SHORT": "RAM failure or power supply issue",
        "1_LONG_3_SHORT": "Memory detection error",
        "5_SHORT": "CPU failure or socket seating error"
    }
    diagnosis = beep_code_table.get(beep_pattern.upper(), "Standard boot or unknown beep pattern")
    is_throttling = cpu_temp_c >= 95.0
    psu_deviation_pct = abs(psu_12v_actual - 12.0) / 12.0 * 100.0
    psu_unstable = psu_deviation_pct > 5.0 # ATX spec allows +-5%
    return {
        "beep_code_diagnosis": diagnosis,
        "cpu_thermal_critical": is_throttling,
        "psu_12v_voltage_deviation_pct": round(psu_deviation_pct, 2),
        "psu_out_of_spec": psu_unstable,
        "action_required": "Replace thermal paste" if is_throttling else ("Check 12V PSU rail" if psu_unstable else "Hardware operating within normal specs")
    }''',
        "test_code": '''res = diagnose_pc_hardware("1_LONG_2_SHORT", 98.0, 11.2)
assert "GPU" in res["beep_code_diagnosis"]
assert res["cpu_thermal_critical"] is True
assert res["psu_out_of_spec"] is True''',
        "metadata": {"tags": ["hardware", "pc_repair", "diagnostics", "electronics", "technician"]}
    },
    {
        "name": "automotive_obd2_fault_analyzer",
        "description": "Interprets OBD-II Diagnostic Trouble Codes (DTC), fuel trim variances, and mass air flow symptoms.",
        "category": "blue_collar",
        "code": '''def analyze_obd2_code(dtc_code: str, long_term_fuel_trim_pct: float) -> dict:
    dtc_library = {
        "P0300": "Random/Multiple Cylinder Misfire Detected",
        "P0171": "System Too Lean (Bank 1) - possible vacuum leak or dirty MAF",
        "P0420": "Catalyst System Efficiency Below Threshold (Bank 1)",
        "P0128": "Coolant Thermostat (Coolant Temp Below Regulating Temp)"
    }
    code = dtc_code.upper().strip()
    description = dtc_library.get(code, "Generic powertrain trouble code")
    running_lean = long_term_fuel_trim_pct > 10.0
    running_rich = long_term_fuel_trim_pct < -10.0
    return {
        "dtc_code": code,
        "official_description": description,
        "fuel_trim_status": "LEAN" if running_lean else ("RICH" if running_rich else "STABLE"),
        "primary_suspect": "Intake vacuum leak or fuel injector clog" if running_lean else ("Oxygen sensor or ignition coil" if code == "P0300" else "Standard diagnostic inspection needed")
    }''',
        "test_code": '''res = analyze_obd2_code("P0171", 14.5)
assert res["fuel_trim_status"] == "LEAN"
assert "MAF" in res["official_description"]''',
        "metadata": {"tags": ["automotive", "mechanic", "obd2", "car_repair", "diagnostics"]}
    },
    {
        "name": "electrical_circuit_safety_checker",
        "description": "Calculates wire gauge (AWG) ampacity limits, 80% circuit breaker loading, and voltage drop over distance.",
        "category": "blue_collar",
        "code": '''def check_electrical_circuit(breaker_amps: float, continuous_load_amps: float, wire_gauge_awg: int, distance_feet: float, voltage: float = 120.0) -> dict:
    max_continuous_safe_load = breaker_amps * 0.80 # 80% NEC Rule
    awg_max_ampacity = {14: 15, 12: 20, 10: 30, 8: 40, 6: 55}
    wire_limit = awg_max_ampacity.get(wire_gauge_awg, 15)
    wire_adequate = wire_limit >= breaker_amps
    overloaded = continuous_load_amps > max_continuous_safe_load
    # Voltage drop estimate: 2 * L * R * I / 1000
    resistance_per_1000ft = {14: 3.07, 12: 1.93, 10: 1.21, 8: 0.764, 6: 0.491}
    r = resistance_per_1000ft.get(wire_gauge_awg, 2.0)
    voltage_drop = (2.0 * distance_feet * r * continuous_load_amps) / 1000.0
    voltage_drop_pct = (voltage_drop / voltage) * 100.0
    return {
        "breaker_rating_amps": breaker_amps,
        "max_continuous_load_amps": round(max_continuous_safe_load, 1),
        "is_safe_under_80pct_rule": not overloaded,
        "wire_gauge_adequate_for_breaker": wire_adequate,
        "estimated_voltage_drop_pct": round(voltage_drop_pct, 2),
        "voltage_drop_acceptable": voltage_drop_pct <= 3.0
    }''',
        "test_code": '''res = check_electrical_circuit(20.0, 15.0, 12, 50.0, 120.0)
assert res["is_safe_under_80pct_rule"] is True
assert res["wire_gauge_adequate_for_breaker"] is True
assert res["voltage_drop_acceptable"] is True''',
        "metadata": {"tags": ["electrical", "electrician", "safety", "nec", "circuit_breaker"]}
    },
    {
        "name": "hvac_refrigerant_flow_triage",
        "description": "Calculates HVAC superheat and subcooling metrics to detect refrigerant leaks, overcharges, or airflow restrictions.",
        "category": "blue_collar",
        "code": '''def triage_hvac_system(target_superheat_f: float, actual_superheat_f: float, target_subcooling_f: float, actual_subcooling_f: float) -> dict:
    sh_delta = actual_superheat_f - target_superheat_f
    sc_delta = actual_subcooling_f - target_subcooling_f
    if sh_delta > 5.0 and sc_delta < -5.0:
        diagnosis = "UNDERCHARGED (Refrigerant Leak)"
    elif sh_delta < -5.0 and sc_delta > 5.0:
        diagnosis = "OVERCHARGED (Excess Refrigerant)"
    elif sh_delta < -5.0 and sc_delta < -5.0:
        diagnosis = "LOW_AIRFLOW (Dirty filter or failing blower fan)"
    else:
        diagnosis = "NORMAL_CHARGE_AND_AIRFLOW"
    return {
        "superheat_variance_f": round(sh_delta, 1),
        "subcooling_variance_f": round(sc_delta, 1),
        "primary_diagnostic": diagnosis,
        "requires_technician_action": diagnosis != "NORMAL_CHARGE_AND_AIRFLOW"
    }''',
        "test_code": '''res = triage_hvac_system(12.0, 20.0, 10.0, 3.0)
assert res["primary_diagnostic"] == "UNDERCHARGED (Refrigerant Leak)"
assert res["requires_technician_action"] is True''',
        "metadata": {"tags": ["hvac", "refrigeration", "air_conditioning", "plumbing", "technician"]}
    },
    {
        "name": "supply_chain_inventory_eoq_calculator",
        "description": "Calculates Economic Order Quantity (EOQ), reorder safety stock buffer, and annual holding cost trade-offs.",
        "category": "blue_collar",
        "code": '''def calculate_inventory_eoq(annual_demand_units: float, cost_per_order: float, annual_holding_cost_per_unit: float, lead_time_days: float, daily_usage_variance_std: float) -> dict:
    # EOQ = sqrt( (2 * D * S) / H )
    eoq = ((2.0 * annual_demand_units * cost_per_order) / annual_holding_cost_per_unit) ** 0.5 if annual_holding_cost_per_unit > 0 else 0.0
    daily_demand = annual_demand_units / 365.0
    lead_time_demand = daily_demand * lead_time_days
    # Safety stock for 95% service level (Z = 1.65)
    safety_stock = 1.65 * (lead_time_days ** 0.5) * daily_usage_variance_std
    reorder_point = lead_time_demand + safety_stock
    return {
        "economic_order_quantity_units": round(eoq, 1),
        "lead_time_demand_units": round(lead_time_demand, 1),
        "recommended_safety_stock_units": round(safety_stock, 1),
        "reorder_point_units": round(reorder_point, 1)
    }''',
        "test_code": '''res = calculate_inventory_eoq(10000.0, 50.0, 2.0, 10.0, 5.0)
assert res["economic_order_quantity_units"] > 500.0
assert res["reorder_point_units"] > res["lead_time_demand_units"]''',
        "metadata": {"tags": ["supply_chain", "inventory", "warehouse", "logistics", "operations"]}
    },
    {
        "name": "options_greeks_black_scholes",
        "description": "Calculates Black-Scholes European call/put theoretical value, delta, and risk-free cost of carry.",
        "category": "investments",
        "code": '''def calculate_options_pricing(s: float, k: float, t_years: float, r: float, sigma: float) -> dict:
    import math
    if t_years <= 0 or sigma <= 0:
        return {"error": "Invalid time or volatility"}
    d1 = (math.log(s / k) + (r + 0.5 * sigma ** 2) * t_years) / (sigma * math.sqrt(t_years))
    d2 = d1 - sigma * math.sqrt(t_years)
    def norm_cdf(x):
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
    call_price = s * norm_cdf(d1) - k * math.exp(-r * t_years) * norm_cdf(d2)
    put_price = k * math.exp(-r * t_years) * norm_cdf(-d2) - s * norm_cdf(-d1)
    call_delta = norm_cdf(d1)
    put_delta = call_delta - 1.0
    return {
        "call_theoretical_price": round(call_price, 2),
        "put_theoretical_price": round(put_price, 2),
        "call_delta": round(call_delta, 3),
        "put_delta": round(put_delta, 3)
    }''',
        "test_code": '''res = calculate_options_pricing(100.0, 100.0, 1.0, 0.05, 0.20)
assert res["call_theoretical_price"] > 0
assert 0.0 < res["call_delta"] < 1.0''',
        "metadata": {"tags": ["options", "derivatives", "black_scholes", "hedging", "finance"]}
    },
    {
        "name": "real_estate_brrrr_calculator",
        "description": "Models Buy, Rehab, Rent, Refinance, Repeat equity recovery, cash-out proceeds, and infinite return status.",
        "category": "investments",
        "code": '''def model_brrrr_deal(purchase_price: float, rehab_cost: float, arv: float, refi_ltv_pct: float = 75.0, monthly_rent: float = 2000.0, monthly_expenses: float = 1200.0) -> dict:
    total_invested = purchase_price + rehab_cost
    max_refi_loan = arv * (refi_ltv_pct / 100.0)
    cash_left_in_deal = max(0.0, total_invested - max_refi_loan)
    cash_pulled_out = min(total_invested, max_refi_loan)
    annual_cash_flow = (monthly_rent - monthly_expenses) * 12.0
    is_infinite = cash_left_in_deal == 0.0 and annual_cash_flow > 0.0
    coc_return = (annual_cash_flow / cash_left_in_deal * 100.0) if cash_left_in_deal > 0 else (999.0 if is_infinite else 0.0)
    return {
        "total_cash_invested": round(total_invested, 2),
        "refinance_loan_proceeds": round(max_refi_loan, 2),
        "capital_left_in_deal": round(cash_left_in_deal, 2),
        "annual_cash_flow": round(annual_cash_flow, 2),
        "cash_on_cash_pct": round(coc_return, 2),
        "infinite_return_achieved": is_infinite
    }''',
        "test_code": '''res = model_brrrr_deal(100000.0, 30000.0, 180000.0, 75.0, 1800.0, 1100.0)
assert res["refinance_loan_proceeds"] == 135000.0
assert res["capital_left_in_deal"] == 0.0
assert res["infinite_return_achieved"] is True''',
        "metadata": {"tags": ["real_estate", "brrrr", "investing", "equity", "wealth"]}
    },
    {
        "name": "b2b_saas_metrics_calculator",
        "description": "Calculates Net Revenue Retention (NRR), CAC Payback Period, and LTV-to-CAC ratio for SaaS businesses.",
        "category": "white_collar",
        "code": '''def calculate_saas_health(mrr_start: float, expansions: float, churn: float, new_customers_acquired: int, sales_marketing_cost: float, arpu_monthly: float, gross_margin_pct: float = 80.0) -> dict:
    nrr = ((mrr_start + expansions - churn) / mrr_start) * 100.0 if mrr_start > 0 else 0.0
    cac = (sales_marketing_cost / new_customers_acquired) if new_customers_acquired > 0 else 0.0
    monthly_gross_profit_per_user = arpu_monthly * (gross_margin_pct / 100.0)
    payback_months = (cac / monthly_gross_profit_per_user) if monthly_gross_profit_per_user > 0 else 999.0
    # Annual churn rate estimate
    churn_pct = (churn / mrr_start) if mrr_start > 0 else 0.05
    lifetime_months = (1.0 / churn_pct) if churn_pct > 0 else 24.0
    ltv = monthly_gross_profit_per_user * lifetime_months
    ltv_to_cac = (ltv / cac) if cac > 0 else 0.0
    return {
        "net_revenue_retention_pct": round(nrr, 2),
        "cac": round(cac, 2),
        "cac_payback_period_months": round(payback_months, 1),
        "ltv_to_cac_ratio": round(ltv_to_cac, 2),
        "is_fundable": nrr >= 110.0 and payback_months <= 12.0 and ltv_to_cac >= 3.0
    }''',
        "test_code": '''res = calculate_saas_health(100000.0, 15000.0, 3000.0, 50, 25000.0, 150.0, 80.0)
assert res["net_revenue_retention_pct"] == 112.0
assert res["is_fundable"] is True''',
        "metadata": {"tags": ["saas", "venture_capital", "metrics", "nrr", "cac_payback"]}
    },
    {
        "name": "email_deliverability_dmarc_dkim_audit",
        "description": "Validates DNS TXT record syntaxes for SPF, DKIM, and DMARC enforcement policies (p=reject/quarantine).",
        "category": "marketing",
        "code": '''def audit_email_authentication(spf_record: str, dkim_selector_present: bool, dmarc_record: str) -> dict:
    spf_valid = spf_record.startswith("v=spf1") and ("-all" in spf_record or "~all" in spf_record)
    dmarc_valid = dmarc_record.startswith("v=DMARC1")
    dmarc_policy = "none"
    if "p=reject" in dmarc_record:
        dmarc_policy = "reject"
    elif "p=quarantine" in dmarc_record:
        dmarc_policy = "quarantine"
    enforced = dmarc_policy in ["quarantine", "reject"]
    score = 0
    if spf_valid: score += 35
    if dkim_selector_present: score += 35
    if dmarc_valid and enforced: score += 30
    return {
        "spf_status": "VALID" if spf_valid else "MISCONFIGURED",
        "dkim_status": "DETECTED" if dkim_selector_present else "MISSING",
        "dmarc_policy": dmarc_policy,
        "deliverability_health_score": score,
        "spoofing_protected": score >= 90
    }''',
        "test_code": '''res = audit_email_authentication("v=spf1 include:_spf.google.com ~all", True, "v=DMARC1; p=reject; rua=mailto:d@domain.com")
assert res["deliverability_health_score"] == 100
assert res["spoofing_protected"] is True''',
        "metadata": {"tags": ["email", "deliverability", "dns", "dmarc", "cybersecurity"]}
    },
    {
        "name": "youtube_ctr_thumbnail_psychology_scorer",
        "description": "Scores thumbnail and title combinations for click-through rate (CTR) potential and curiosity gap tension.",
        "category": "content",
        "code": '''def score_youtube_packaging(title: str, thumbnail_has_face: bool, thumbnail_word_count: int, title_curiosity_gap: bool) -> dict:
    title_len = len(title)
    score = 0
    flags = []
    if 35 <= title_len <= 55:
        score += 30
    else:
        flags.append("Title length outside optimal 35-55 characters")
    if title_curiosity_gap:
        score += 30
    else:
        flags.append("Missing tension or curiosity gap in title")
    if thumbnail_has_face:
        score += 20
    if 1 <= thumbnail_word_count <= 4:
        score += 20
    elif thumbnail_word_count > 6:
        flags.append("Too many words on thumbnail (causes visual clutter)")
    return {
        "estimated_ctr_score": score,
        "title_length": title_len,
        "improvement_flags": flags,
        "expected_performance": "VIRAL_POTENTIAL" if score >= 80 else ("SOLID" if score >= 60 else "NEEDS_OPTIMIZATION")
    }''',
        "test_code": '''res = score_youtube_packaging("The Day AI Became Self-Aware", True, 3, True)
assert res["estimated_ctr_score"] == 100
assert res["expected_performance"] == "VIRAL_POTENTIAL"''',
        "metadata": {"tags": ["youtube", "ctr", "video", "thumbnails", "social_media"]}
    },
    {
        "name": "ui_ux_fitts_law_click_target_calculator",
        "description": "Calculates movement index of difficulty using Fitts's Law and verifies accessibility minimum target dimensions.",
        "category": "design",
        "code": '''def calculate_fitts_difficulty(target_width_px: float, distance_px: float) -> dict:
    import math
    if target_width_px <= 0 or distance_px <= 0:
        return {"error": "Invalid dimensions"}
    # Fitts's Law Index of Difficulty: ID = log2( (2 * D) / W )
    index_of_difficulty = math.log2((2.0 * distance_px) / target_width_px)
    meets_wcag_touch_target = target_width_px >= 44.0 # 44x44px minimum for mobile touch
    return {
        "target_width_px": target_width_px,
        "distance_px": distance_px,
        "index_of_difficulty_bits": round(index_of_difficulty, 2),
        "meets_mobile_touch_standard_44px": meets_wcag_touch_target,
        "ergonomic_rating": "EFFORTLESS" if index_of_difficulty < 3.0 else ("ACCEPTABLE" if index_of_difficulty < 5.0 else "HIGH_FRICTION")
    }''',
        "test_code": '''res = calculate_fitts_difficulty(48.0, 150.0)
assert res["meets_mobile_touch_standard_44px"] is True
assert res["ergonomic_rating"] in ["EFFORTLESS", "ACCEPTABLE"]''',
        "metadata": {"tags": ["ui_ux", "fitts_law", "ergonomics", "accessibility", "frontend"]}
    },
    {
        "name": "color_wcag_contrast_ratio_evaluator",
        "description": "Calculates relative luminance and exact contrast ratio between foreground and background colors (WCAG AA/AAA).",
        "category": "design",
        "code": '''def evaluate_wcag_contrast(fg_hex: str, bg_hex: str) -> dict:
    def hex_to_luminance(h):
        h = h.lstrip("#")
        rgb = [int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        linear = [(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4) for c in rgb]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    l1 = hex_to_luminance(fg_hex)
    l2 = hex_to_luminance(bg_hex)
    brightest = max(l1, l2)
    darkest = min(l1, l2)
    ratio = (brightest + 0.05) / (darkest + 0.05)
    return {
        "contrast_ratio": round(ratio, 2),
        "wcag_aa_normal_text_pass": ratio >= 4.5,
        "wcag_aa_large_text_pass": ratio >= 3.0,
        "wcag_aaa_normal_text_pass": ratio >= 7.0
    }''',
        "test_code": '''res = evaluate_wcag_contrast("#FFFFFF", "#000000")
assert res["contrast_ratio"] == 21.0
assert res["wcag_aaa_normal_text_pass"] is True''',
        "metadata": {"tags": ["color", "accessibility", "wcag", "contrast", "design"]}
    },
    {
        "name": "customer_churn_cohort_analysis",
        "description": "Calculates monthly retention cohort percentages, churn rate velocity, and expected customer lifespan.",
        "category": "white_collar",
        "code": '''def analyze_churn_cohort(cohort_initial_size: int, active_users_per_month: list) -> dict:
    if cohort_initial_size <= 0:
        return {"error": "Invalid cohort initial size"}
    retention_curve = [round((active / cohort_initial_size) * 100.0, 1) for active in active_users_per_month]
    recent_churn_rate = 0.0
    if len(active_users_per_month) >= 2:
        prev, curr = active_users_per_month[-2], active_users_per_month[-1]
        recent_churn_rate = ((prev - curr) / prev) * 100.0 if prev > 0 else 0.0
    avg_lifespan_months = (100.0 / recent_churn_rate) if recent_churn_rate > 0 else 999.0
    return {
        "initial_cohort_size": cohort_initial_size,
        "retention_curve_pct": retention_curve,
        "latest_monthly_churn_pct": round(recent_churn_rate, 2),
        "expected_customer_lifespan_months": round(avg_lifespan_months, 1)
    }''',
        "test_code": '''res = analyze_churn_cohort(1000, [1000, 850, 750, 700, 680])
assert res["retention_curve_pct"][0] == 100.0
assert res["retention_curve_pct"][-1] == 68.0''',
        "metadata": {"tags": ["analytics", "churn", "retention", "cohorts", "data_science"]}
    },
    {
        "name": "project_pert_three_point_estimator",
        "description": "Calculates PERT Expected Duration and Standard Deviation from Optimistic, Most Likely, and Pessimistic estimates.",
        "category": "white_collar",
        "code": '''def calculate_pert_estimate(optimistic_days: float, most_likely_days: float, pessimistic_days: float) -> dict:
    # PERT Formula: (O + 4M + P) / 6
    expected_duration = (optimistic_days + 4.0 * most_likely_days + pessimistic_days) / 6.0
    # Standard deviation: (P - O) / 6
    std_dev = (pessimistic_days - optimistic_days) / 6.0
    return {
        "expected_duration_days": round(expected_duration, 2),
        "standard_deviation_days": round(std_dev, 2),
        "confidence_68pct_range": f"{round(expected_duration - std_dev, 1)} - {round(expected_duration + std_dev, 1)} days",
        "confidence_95pct_range": f"{round(expected_duration - 2 * std_dev, 1)} - {round(expected_duration + 2 * std_dev, 1)} days"
    }''',
        "test_code": '''res = calculate_pert_estimate(10.0, 15.0, 26.0)
assert res["expected_duration_days"] == 16.0
assert res["standard_deviation_days"] > 2.0''',
        "metadata": {"tags": ["project_management", "pert", "estimation", "pmp", "agile"]}
    },
    {
        "name": "sql_query_performance_anti_pattern_auditor",
        "description": "Scans SQL queries for SELECT *, missing LIMIT, leading wildcards in LIKE, and implicit cross joins.",
        "category": "white_collar",
        "code": '''def audit_sql_query(query_text: str) -> dict:
    q = query_text.upper()
    anti_patterns = []
    if "SELECT *" in q:
        anti_patterns.append("SELECT_ALL_COLUMNS: Exposes unintended data and defeats index-only scans.")
    if "LIKE '%" in q:
        anti_patterns.append("LEADING_WILDCARD_LIKE: Invalidates B-Tree indexes, forcing sequential table scans.")
    if "JOIN" not in q and "," in q.split("FROM")[-1].split("WHERE")[0]:
        anti_patterns.append("IMPLICIT_CROSS_JOIN: Multiple tables listed in FROM clause without explicit JOIN condition.")
    if "LIMIT" not in q and "SELECT" in q:
        anti_patterns.append("UNBOUNDED_SELECT: Missing LIMIT clause on large analytical dataset.")
    health_score = max(0, 100 - (len(anti_patterns) * 25))
    return {
        "sql_health_score": health_score,
        "anti_patterns_found": anti_patterns,
        "is_production_safe": health_score >= 75
    }''',
        "test_code": '''res = audit_sql_query("SELECT * FROM users WHERE email LIKE '%@gmail.com'")
assert len(res["anti_patterns_found"]) == 2
assert res["is_production_safe"] is False''',
        "metadata": {"tags": ["sql", "database", "performance", "backend", "dba"]}
    },
    {
        "name": "cloud_finops_cost_optimizer",
        "description": "Calculates Spot vs On-Demand savings, Reserved Instance (RI) breakeven months, and idle cloud resource waste.",
        "category": "white_collar",
        "code": '''def calculate_finops_savings(monthly_on_demand_spend: float, spot_eligible_pct: float = 40.0, spot_discount_pct: float = 70.0, ri_commitment_discount_pct: float = 40.0) -> dict:
    spot_monthly_spend = monthly_on_demand_spend * (spot_eligible_pct / 100.0)
    spot_savings = spot_monthly_spend * (spot_discount_pct / 100.0)
    remaining_spend = monthly_on_demand_spend - spot_monthly_spend
    ri_savings = remaining_spend * (ri_commitment_discount_pct / 100.0)
    total_savings_monthly = spot_savings + ri_savings
    annualized_savings = total_savings_monthly * 12.0
    return {
        "monthly_on_demand_baseline": monthly_on_demand_spend,
        "monthly_spot_savings": round(spot_savings, 2),
        "monthly_ri_savings": round(ri_savings, 2),
        "total_monthly_savings": round(total_savings_monthly, 2),
        "annualized_savings": round(annualized_savings, 2),
        "cost_reduction_pct": round((total_savings_monthly / monthly_on_demand_spend) * 100.0, 1)
    }''',
        "test_code": '''res = calculate_finops_savings(10000.0)
assert res["total_monthly_savings"] > 4000.0
assert res["cost_reduction_pct"] > 40.0''',
        "metadata": {"tags": ["finops", "aws", "cloud", "devops", "cost_optimization"]}
    },
    {
        "name": "solar_photovoltaic_system_sizing",
        "description": "Calculates solar panel array kW requirements, battery storage kWh, and payback years from utility rates.",
        "category": "blue_collar",
        "code": '''def size_solar_pv_system(monthly_kwh_usage: float, peak_sun_hours_per_day: float = 4.5, utility_rate_per_kwh: float = 0.18, cost_per_watt: float = 2.80) -> dict:
    daily_kwh = monthly_kwh_usage / 30.0
    system_efficiency = 0.80
    required_system_kw = daily_kwh / (peak_sun_hours_per_day * system_efficiency)
    total_system_cost = required_system_kw * 1000.0 * cost_per_watt
    annual_electric_savings = monthly_kwh_usage * utility_rate_per_kwh * 12.0
    payback_years = (total_system_cost / annual_electric_savings) if annual_electric_savings > 0 else 99.0
    battery_storage_kwh = daily_kwh * 1.2 # 1.2 days of autonomy
    return {
        "recommended_array_size_kw": round(required_system_kw, 2),
        "recommended_battery_kwh": round(battery_storage_kwh, 2),
        "estimated_gross_cost": round(total_system_cost, 2),
        "annual_utility_savings": round(annual_electric_savings, 2),
        "simple_payback_years": round(payback_years, 1)
    }''',
        "test_code": '''res = size_solar_pv_system(900.0)
assert res["recommended_array_size_kw"] > 5.0
assert res["simple_payback_years"] < 15.0''',
        "metadata": {"tags": ["solar", "renewable_energy", "photovoltaic", "electrician", "sustainability"]}
    },
    {
        "name": "three_phase_motor_current_calculator",
        "description": "Calculates 3-phase electric motor full-load amperes (FLA) and NEC-compliant dual-element fuse sizing.",
        "category": "blue_collar",
        "code": '''def calculate_motor_specs(horsepower: float, voltage: float = 460.0, efficiency_pct: float = 90.0, power_factor: float = 0.85) -> dict:
    import math
    watts = horsepower * 746.0
    eff = efficiency_pct / 100.0
    # I = P / (sqrt(3) * V * PF * Eff)
    fla = watts / (math.sqrt(3.0) * voltage * power_factor * eff)
    # NEC 430.52 Dual Element Fuse: 175% of FLA
    fuse_rating = fla * 1.75
    # Inverse Time Circuit Breaker: 250% of FLA
    breaker_rating = fla * 2.50
    return {
        "horsepower": horsepower,
        "full_load_amperes": round(fla, 2),
        "nec_dual_element_fuse_amps": round(fuse_rating, 1),
        "nec_circuit_breaker_amps": round(breaker_rating, 1)
    }''',
        "test_code": '''res = calculate_motor_specs(25.0, 460.0)
assert res["full_load_amperes"] > 25.0
assert res["nec_circuit_breaker_amps"] > res["full_load_amperes"]''',
        "metadata": {"tags": ["electrical", "motors", "industrial", "electrician", "nec"]}
    },
    {
        "name": "circadian_sleep_cycle_optimizer",
        "description": "Calculates 90-minute REM sleep cycles, sleep latency buffers, and ideal bedtime targets to prevent sleep inertia.",
        "category": "daily_life",
        "code": '''def calculate_sleep_cycles(wake_up_hour: int, wake_up_minute: int, desired_cycles: int = 5) -> dict:
    total_sleep_minutes = desired_cycles * 90
    latency_buffer_minutes = 15
    total_minutes_needed = total_sleep_minutes + latency_buffer_minutes
    wake_total_minutes = (wake_up_hour * 60) + wake_up_minute
    bed_total_minutes = (wake_total_minutes - total_minutes_needed) % (24 * 60)
    bed_hour = bed_total_minutes // 60
    bed_min = bed_total_minutes % 60
    return {
        "wake_up_time": f"{wake_up_hour:02d}:{wake_up_minute:02d}",
        "sleep_cycles_count": desired_cycles,
        "total_sleep_hours": round(total_sleep_minutes / 60.0, 1),
        "recommended_bedtime": f"{bed_hour:02d}:{bed_min:02d}",
        "prevents_grogginess": True
    }''',
        "test_code": '''res = calculate_sleep_cycles(7, 0, 5)
assert res["total_sleep_hours"] == 7.5
assert "recommended_bedtime" in res''',
        "metadata": {"tags": ["sleep", "health", "circadian_rhythm", "biohacking", "wellness"]}
    },
    {
        "name": "schengen_90_180_travel_calculator",
        "description": "Calculates remaining legal travel days in the European Schengen Area under the rolling 90/180-day limitation rule.",
        "category": "daily_life",
        "code": '''def calculate_schengen_allowance(days_spent_in_last_180_days: int) -> dict:
    max_allowed = 90
    remaining_days = max(0, max_allowed - days_spent_in_last_180_days)
    overstay = days_spent_in_last_180_days > max_allowed
    return {
        "days_spent": days_spent_in_last_180_days,
        "legal_days_remaining": remaining_days,
        "is_overstaying": overstay,
        "status": "LEGAL" if not overstay else "OVERSTAY_PENALTY_WARNING",
        "rolling_window_days": 180
    }''',
        "test_code": '''res = calculate_schengen_allowance(65)
assert res["legal_days_remaining"] == 25
assert res["is_overstaying"] is False''',
        "metadata": {"tags": ["travel", "visa", "schengen", "immigration", "nomad"]}
    },
    {
        "name": "crisis_pr_backlash_velocity_evaluator",
        "description": "Calculates social media negative mention velocity and determines whether a public corporate apology is warranted.",
        "category": "social_media",
        "code": '''def evaluate_pr_crisis(negative_mentions_per_hour: int, baseline_hourly_mentions: int, influencer_involvement: bool, main_press_pickup: bool) -> dict:
    ratio = (negative_mentions_per_hour / baseline_hourly_mentions) if baseline_hourly_mentions > 0 else 10.0
    threat_points = 0
    if ratio >= 5.0: threat_points += 30
    if ratio >= 10.0: threat_points += 20
    if influencer_involvement: threat_points += 25
    if main_press_pickup: threat_points += 25
    action = "STAND_DOWN_DO_NOT_FEED_CYCLE"
    if threat_points >= 75:
        action = "ISSUE_IMMEDIATE_CEO_STATEMENT"
    elif threat_points >= 40:
        action = "PREPARE_HOLDING_STATEMENT_AND_MONITOR"
    return {
        "spike_multiplier": round(ratio, 1),
        "crisis_threat_score": threat_points,
        "recommended_pr_action": action
    }''',
        "test_code": '''res = evaluate_pr_crisis(500, 20, True, True)
assert res["crisis_threat_score"] == 100
assert res["recommended_pr_action"] == "ISSUE_IMMEDIATE_CEO_STATEMENT"''',
        "metadata": {"tags": ["pr", "crisis_management", "communications", "social_media", "brand"]}
    },
    {
        "name": "recruitment_interview_scorecard",
        "description": "Calculates structured candidate competency scores across Technical Rigor, Problem Solving, and Culture Fit.",
        "category": "white_collar",
        "code": '''def score_candidate_interview(technical_1_to_5: float, problem_solving_1_to_5: float, communication_1_to_5: float, cultural_alignment_1_to_5: float) -> dict:
    weights = {"tech": 0.40, "problem": 0.30, "comm": 0.15, "culture": 0.15}
    composite_score = (
        technical_1_to_5 * weights["tech"] +
        problem_solving_1_to_5 * weights["problem"] +
        communication_1_to_5 * weights["comm"] +
        cultural_alignment_1_to_5 * weights["culture"]
    )
    decision = "STRONG_HIRE" if composite_score >= 4.2 else ("HIRE" if composite_score >= 3.5 else ("NO_HIRE" if composite_score >= 2.8 else "STRONG_NO_HIRE"))
    return {
        "composite_score_out_of_5": round(composite_score, 2),
        "hiring_recommendation": decision,
        "passes_bar": composite_score >= 3.5
    }''',
        "test_code": '''res = score_candidate_interview(4.5, 4.0, 4.0, 4.5)
assert res["composite_score_out_of_5"] >= 4.0
assert res["hiring_recommendation"] in ["HIRE", "STRONG_HIRE"]''',
        "metadata": {"tags": ["hr", "recruitment", "interviews", "hiring", "talent"]}
    },
    {
        "name": "lean_manufacturing_takt_time_calc",
        "description": "Calculates Takt Time, Cycle Time variance, and worker station headcount requirements for lean assembly lines.",
        "category": "blue_collar",
        "code": '''def calculate_takt_time(net_available_working_seconds_per_shift: float, customer_demand_units_per_shift: int, total_work_content_seconds: float) -> dict:
    if customer_demand_units_per_shift <= 0:
        return {"error": "Invalid customer demand"}
    takt_time_seconds = net_available_working_seconds_per_shift / customer_demand_units_per_shift
    # Theoretical headcount = Total Work Content / Takt Time
    required_operators = total_work_content_seconds / takt_time_seconds if takt_time_seconds > 0 else 1.0
    return {
        "takt_time_seconds": round(takt_time_seconds, 1),
        "total_work_content_seconds": total_work_content_seconds,
        "theoretical_operators_needed": round(required_operators, 1),
        "recommended_station_count": int(-(-required_operators // 1)) # Ceiling division
    }''',
        "test_code": '''res = calculate_takt_time(27000.0, 450, 180.0)
assert res["takt_time_seconds"] == 60.0
assert res["recommended_station_count"] == 3''',
        "metadata": {"tags": ["manufacturing", "lean", "six_sigma", "takt_time", "operations"]}
    }
]


def seed_skills():
    logger.info("Initializing F.R.I.D.A.Y. Engine to register Omni-Skills Catalog...")
    config = FridayConfig()
    engine = FridayEngine(config)
    
    total = len(SKILLS_CATALOG)
    logger.info(f"Seeding {total} comprehensive production skills across all human domains...")
    
    successful = 0
    for idx, skill in enumerate(SKILLS_CATALOG, 1):
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
                logger.info(f"[{idx}/{total}] [OK] Successfully seeded skill: {skill['name']} ({skill['category']})")
            else:
                logger.warning(f"[{idx}/{total}] [WARN] Failed to seed skill: {skill['name']}")
        except Exception as e:
            logger.error(f"[{idx}/{total}] [ERROR] Exception while seeding {skill['name']}: {e}")
            
    print(f"\nSKILL SEEDING COMPLETE: {successful}/{total} skills successfully stored and indexed in SQLite & SKILL.md!")

if __name__ == "__main__":
    seed_skills()
