"""
F.R.I.D.A.Y. Deep Trading & Financial Intelligence Seeder.
Ingests specialized skills covering Smart Money Concepts (ICT), Wyckoff Method,
Volume Profile / VWAP, Options Greeks & Strategies, Crypto On-Chain Metrics,
Fibonacci OTE, Candlestick Recognition, and Mathematical Risk Expectancy.
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


TRADING_SKILLS_CATALOG = [
    # =========================================================================
    # 1. SMART MONEY CONCEPTS (SMC / ICT) & PRICE ACTION
    # =========================================================================
    {
        "name": "smart_money_concepts_ict_analyzer",
        "description": "Identifies Order Blocks (OB), Break of Structure (BOS), Change of Character (CHoCH), and Premium vs Discount arrays.",
        "category": "investments",
        "code": '''def analyze_smc_structure(highs: list, lows: list, closes: list) -> dict:
    if len(highs) < 5 or len(lows) < 5:
        return {"error": "Insufficient candle data for SMC analysis"}
    recent_high = max(highs[-5:])
    recent_low = min(lows[-5:])
    range_high = max(highs)
    range_low = min(lows)
    equilibrium = (range_high + range_low) / 2.0
    current_price = closes[-1]
    pricing_zone = "PREMIUM (Favorable for Shorts)" if current_price > equilibrium else "DISCOUNT (Favorable for Longs)"
    bos_bullish = closes[-1] > highs[-2] and highs[-2] > highs[-3]
    bos_bearish = closes[-1] < lows[-2] and lows[-2] < lows[-3]
    structure_shift = "BULLISH_BOS" if bos_bullish else ("BEARISH_BOS" if bos_bearish else "CONSOLIDATION")
    return {
        "range_high": range_high,
        "range_low": range_low,
        "equilibrium_50pct": round(equilibrium, 2),
        "current_price": current_price,
        "pricing_zone": pricing_zone,
        "market_structure": structure_shift,
        "optimal_trade_entry_bias": "LOOK_FOR_DISCOUNT_ORDER_BLOCKS" if current_price < equilibrium else "LOOK_FOR_PREMIUM_LIQUIDITY_SWEEPS"
    }''',
        "test_code": '''res = analyze_smc_structure([100, 105, 110, 115, 120], [95, 98, 102, 108, 112], [98, 103, 109, 114, 119])
assert res["pricing_zone"].startswith("PREMIUM")
assert res["equilibrium_50pct"] > 0''',
        "metadata": {"tags": ["trading", "smc", "ict", "order_blocks", "price_action"]}
    },
    {
        "name": "wyckoff_market_phase_detector",
        "description": "Identifies Wyckoff market cycles: Phase A (Stopping Action), Phase B (Testing), Phase C (Spring/UTAD), Phase D (SOS), Phase E (Markup/Markdown).",
        "category": "investments",
        "code": '''def detect_wyckoff_phase(closes: list, volumes: list, support_level: float, resistance_level: float) -> dict:
    if len(closes) < 5 or len(volumes) < 5:
        return {"error": "Need at least 5 periods"}
    current_close = closes[-1]
    lowest_recent = min(closes[-5:])
    highest_recent = max(closes[-5:])
    avg_vol = sum(volumes) / len(volumes)
    recent_vol = volumes[-1]
    is_spring = lowest_recent < support_level and current_close > support_level and recent_vol > avg_vol * 1.3
    is_utad = highest_recent > resistance_level and current_close < resistance_level and recent_vol > avg_vol * 1.3
    is_markup = current_close > resistance_level and recent_vol >= avg_vol
    is_markdown = current_close < support_level and recent_vol >= avg_vol
    if is_spring:
        phase = "PHASE_C_SPRING (High Probability Bullish Accumulation Test)"
    elif is_utad:
        phase = "PHASE_C_UTAD (Upthrust After Distribution - Bearish Reversal)"
    elif is_markup:
        phase = "PHASE_E_MARKUP (Active Trend Acceleration)"
    elif is_markdown:
        phase = "PHASE_E_MARKDOWN (Active Liquidation Trend)"
    else:
        phase = "PHASE_B_CONSOLIDATION (Building Cause / Liquidity Absorption)"
    return {
        "detected_wyckoff_event": phase,
        "volume_relative_to_average": round(recent_vol / avg_vol, 2) if avg_vol > 0 else 1.0,
        "is_reversal_trigger": is_spring or is_utad
    }''',
        "test_code": '''res = detect_wyckoff_phase([98, 97, 89, 92, 94], [100, 110, 250, 180, 200], 90.0, 110.0)
assert "PHASE_C_SPRING" in res["detected_wyckoff_event"]
assert res["is_reversal_trigger"] is True''',
        "metadata": {"tags": ["trading", "wyckoff", "accumulation", "distribution", "spring"]}
    },
    {
        "name": "fibonacci_retracement_golden_pocket",
        "description": "Calculates Fibonacci retracement levels, Optimal Trade Entry (OTE: 0.618 - 0.786), and extension profit targets (1.272, 1.618).",
        "category": "investments",
        "code": '''def calculate_fibonacci_levels(swing_low: float, swing_high: float, trend: str = "bullish") -> dict:
    diff = swing_high - swing_low
    if trend.lower() == "bullish":
        fibs = {
            "0.236": round(swing_high - 0.236 * diff, 2),
            "0.382": round(swing_high - 0.382 * diff, 2),
            "0.500_equilibrium": round(swing_high - 0.500 * diff, 2),
            "0.618_golden_ratio": round(swing_high - 0.618 * diff, 2),
            "0.650_golden_pocket": round(swing_high - 0.650 * diff, 2),
            "0.786_deep_retrace": round(swing_high - 0.786 * diff, 2),
            "1.272_extension_target": round(swing_high + 0.272 * diff, 2),
            "1.618_golden_extension": round(swing_high + 0.618 * diff, 2)
        }
    else:
        fibs = {
            "0.236": round(swing_low + 0.236 * diff, 2),
            "0.382": round(swing_low + 0.382 * diff, 2),
            "0.500_equilibrium": round(swing_low + 0.500 * diff, 2),
            "0.618_golden_ratio": round(swing_low + 0.618 * diff, 2),
            "0.650_golden_pocket": round(swing_low + 0.650 * diff, 2),
            "0.786_deep_retrace": round(swing_low + 0.786 * diff, 2),
            "1.272_extension_target": round(swing_low - 0.272 * diff, 2),
            "1.618_golden_extension": round(swing_low - 0.618 * diff, 2)
        }
    return {
        "trend_direction": trend.upper(),
        "golden_pocket_range": f"{fibs['0.618_golden_ratio']} - {fibs['0.650_golden_pocket']}",
        "fibonacci_levels": fibs
    }''',
        "test_code": '''res = calculate_fibonacci_levels(100.0, 200.0, "bullish")
assert res["fibonacci_levels"]["0.500_equilibrium"] == 150.0
assert res["fibonacci_levels"]["1.618_golden_extension"] == 261.8''',
        "metadata": {"tags": ["trading", "fibonacci", "golden_ratio", "ote", "technical_analysis"]}
    },

    # =========================================================================
    # 2. VOLATILITY, CHANNELS & INDICATORS
    # =========================================================================
    {
        "name": "volume_weighted_average_price_vwap",
        "description": "Calculates intraday Volume Weighted Average Price (VWAP) and +1, +2, +3 standard deviation statistical bands.",
        "category": "investments",
        "code": '''def calculate_vwap_bands(prices: list, volumes: list) -> dict:
    if len(prices) != len(volumes) or not prices:
        return {"error": "Prices and volumes must be non-empty lists of identical length"}
    cum_vol = sum(volumes)
    if cum_vol == 0:
        return {"error": "Cumulative volume is zero"}
    cum_pv = sum(p * v for p, v in zip(prices, volumes))
    vwap = cum_pv / cum_vol
    # Calculate volume-weighted variance
    variance = sum(v * ((p - vwap) ** 2) for p, v in zip(prices, volumes)) / cum_vol
    std_dev = variance ** 0.5
    current_price = prices[-1]
    return {
        "vwap": round(vwap, 2),
        "upper_band_1_sigma": round(vwap + std_dev, 2),
        "lower_band_1_sigma": round(vwap - std_dev, 2),
        "upper_band_2_sigma": round(vwap + 2 * std_dev, 2),
        "lower_band_2_sigma": round(vwap - 2 * std_dev, 2),
        "current_price": current_price,
        "mean_reversion_bias": "OVERBOUGHT_STRETCHED" if current_price > (vwap + 2 * std_dev) else ("OVERSOLD_BOUNCE" if current_price < (vwap - 2 * std_dev) else "EQUILIBRIUM")
    }''',
        "test_code": '''res = calculate_vwap_bands([100, 102, 104, 106, 108], [1000, 1500, 1200, 1800, 2000])
assert res["vwap"] > 100
assert res["upper_band_2_sigma"] > res["vwap"]''',
        "metadata": {"tags": ["trading", "vwap", "institutional", "intraday", "indicators"]}
    },
    {
        "name": "bollinger_bands_volatility_squeeze",
        "description": "Calculates 20-period Bollinger Bands, bandwidth percentage, and flags high-volatility squeeze breakout setups.",
        "category": "investments",
        "code": '''def calculate_bollinger_bands(closes: list, period: int = 20, num_std: float = 2.0) -> dict:
    if len(closes) < period:
        return {"error": f"Need at least {period} closes"}
    window = closes[-period:]
    sma = sum(window) / period
    variance = sum((x - sma) ** 2 for x in window) / period
    std_dev = variance ** 0.5
    upper = sma + (num_std * std_dev)
    lower = sma - (num_std * std_dev)
    bandwidth = ((upper - lower) / sma) * 100.0 if sma > 0 else 0.0
    current_price = closes[-1]
    # Squeeze is typically identified when bandwidth is compressed below 5%
    is_squeeze = bandwidth < 5.0
    return {
        "middle_band_sma20": round(sma, 2),
        "upper_band": round(upper, 2),
        "lower_band": round(lower, 2),
        "bandwidth_pct": round(bandwidth, 2),
        "volatility_squeeze_active": is_squeeze,
        "trading_signal": "PREPARE_BREAKOUT_PLAY" if is_squeeze else ("UPPER_BAND_RESISTANCE" if current_price >= upper else ("LOWER_BAND_SUPPORT" if current_price <= lower else "NEUTRAL"))
    }''',
        "test_code": '''res = calculate_bollinger_bands([100 + (i % 2) for i in range(25)])
assert res["bandwidth_pct"] < 5.0
assert res["volatility_squeeze_active"] is True''',
        "metadata": {"tags": ["trading", "bollinger_bands", "volatility", "squeeze", "breakout"]}
    },
    {
        "name": "candlestick_pattern_recognition_engine",
        "description": "Recognizes reversal candlestick patterns: Bullish/Bearish Engulfing, Hammer, Shooting Star, and Doji.",
        "category": "investments",
        "code": '''def detect_candlestick_pattern(open_p: float, high_p: float, low_p: float, close_p: float, prev_open: float, prev_close: float) -> dict:
    body = abs(close_p - open_p)
    total_range = high_p - low_p if (high_p - low_p) > 0 else 0.0001
    upper_wick = high_p - max(open_p, close_p)
    lower_wick = min(open_p, close_p) - low_p
    is_bullish = close_p > open_p
    prev_bullish = prev_close > prev_open
    pattern = "INDECISION / STANDARD"
    if body / total_range < 0.10:
        pattern = "DOJI (Equilibrium / Impending Volatility)"
    elif lower_wick >= 2.0 * body and upper_wick <= 0.2 * body:
        pattern = "HAMMER (Bullish Reversal Signal at support)"
    elif upper_wick >= 2.0 * body and lower_wick <= 0.2 * body:
        pattern = "SHOOTING_STAR (Bearish Reversal Signal at resistance)"
    elif is_bullish and not prev_bullish and open_p <= prev_close and close_p >= prev_open:
        pattern = "BULLISH_ENGULFING (Strong Institutional Accumulation)"
    elif not is_bullish and prev_bullish and open_p >= prev_close and close_p <= prev_open:
        pattern = "BEARISH_ENGULFING (Strong Institutional Distribution)"
    return {
        "detected_pattern": pattern,
        "is_reversal": pattern != "INDECISION / STANDARD",
        "body_to_range_ratio": round(body / total_range, 3),
        "is_bullish_candle": is_bullish
    }''',
        "test_code": '''res = detect_candlestick_pattern(95.0, 96.0, 70.0, 94.0, 96.0, 95.0)
assert "HAMMER" in res["detected_pattern"]
assert res["is_reversal"] is True''',
        "metadata": {"tags": ["trading", "candlesticks", "patterns", "technical_analysis", "charting"]}
    },

    # =========================================================================
    # 3. QUANTITATIVE RISK & POSITION SIZING
    # =========================================================================
    {
        "name": "kelly_criterion_position_sizer",
        "description": "Calculates optimal mathematical capital allocation per trade using the Kelly Criterion and Half-Kelly safety buffers.",
        "category": "investments",
        "code": '''def calculate_kelly_position(account_balance: float, win_rate_pct: float, risk_reward_ratio: float, use_half_kelly: bool = True) -> dict:
    p = win_rate_pct / 100.0
    q = 1.0 - p
    b = risk_reward_ratio # Odds received on the wager (Reward / Risk)
    if b <= 0:
        return {"error": "Risk-reward ratio must be greater than 0"}
    # Kelly % = (b*p - q) / b
    kelly_pct = ((b * p) - q) / b
    if kelly_pct <= 0:
        return {
            "recommended_allocation_pct": 0.0,
            "recommended_wager_usd": 0.0,
            "edge_status": "NEGATIVE_EXPECTANCY_DO_NOT_TRADE"
        }
    applied_pct = (kelly_pct / 2.0) if use_half_kelly else kelly_pct
    wager_amount = account_balance * applied_pct
    return {
        "full_kelly_pct": round(kelly_pct * 100.0, 2),
        "applied_allocation_pct": round(applied_pct * 100.0, 2),
        "recommended_position_risk_usd": round(wager_amount, 2),
        "edge_status": "POSITIVE_EXPECTANCY"
    }''',
        "test_code": '''res = calculate_kelly_position(100000.0, 55.0, 2.0, True)
assert res["applied_allocation_pct"] > 0.0
assert res["edge_status"] == "POSITIVE_EXPECTANCY"''',
        "metadata": {"tags": ["trading", "risk_management", "kelly_criterion", "position_sizing", "quant"]}
    },
    {
        "name": "risk_reward_expectancy_calculator",
        "description": "Calculates expected monetary value per trade, breakeven required win-rate, and portfolio survival expectancy.",
        "category": "investments",
        "code": '''def calculate_trade_expectancy(win_rate_pct: float, avg_win_usd: float, avg_loss_usd: float, num_trades_sample: int = 100) -> dict:
    w = win_rate_pct / 100.0
    l = 1.0 - w
    # Expectancy = (Win% * Avg Win) - (Loss% * Avg Loss)
    expectancy_per_trade = (w * avg_win_usd) - (l * avg_loss_usd)
    # Breakeven win rate = Loss / (Win + Loss)
    breakeven_win_rate = (avg_loss_usd / (avg_win_usd + avg_loss_usd)) * 100.0 if (avg_win_usd + avg_loss_usd) > 0 else 0.0
    projected_net_gain = expectancy_per_trade * num_trades_sample
    return {
        "expectancy_per_trade_usd": round(expectancy_per_trade, 2),
        "breakeven_win_rate_pct": round(breakeven_win_rate, 2),
        "win_rate_safety_margin_pct": round(win_rate_pct - breakeven_win_rate, 2),
        "projected_profit_over_sample": round(projected_net_gain, 2),
        "system_viable": expectancy_per_trade > 0.0
    }''',
        "test_code": '''res = calculate_trade_expectancy(50.0, 300.0, 100.0)
assert res["expectancy_per_trade_usd"] == 100.0
assert res["system_viable"] is True''',
        "metadata": {"tags": ["trading", "expectancy", "risk", "statistics", "win_rate"]}
    },

    # =========================================================================
    # 4. OPTIONS & VOLATILITY DERIVATIVES
    # =========================================================================
    {
        "name": "options_iv_rank_percentile_analyzer",
        "description": "Calculates Implied Volatility Rank (IV Rank) and IV Percentile to dictate Net Debit vs Net Credit options strategies.",
        "category": "investments",
        "code": '''def analyze_iv_environment(current_iv: float, iv_low_52wk: float, iv_high_52wk: float, days_below_current_iv: int, total_trading_days: int = 252) -> dict:
    iv_range = iv_high_52wk - iv_low_52wk
    iv_rank = ((current_iv - iv_low_52wk) / iv_range) * 100.0 if iv_range > 0 else 50.0
    iv_percentile = (days_below_current_iv / total_trading_days) * 100.0 if total_trading_days > 0 else 50.0
    strategy_recommendation = "SELL_PREMIUM (Iron Condor, Credit Spreads, Strangles)" if iv_rank >= 50.0 else "BUY_PREMIUM (Long Calls/Puts, Debit Spreads, Calendar Spreads)"
    return {
        "current_iv": current_iv,
        "iv_rank_pct": round(iv_rank, 1),
        "iv_percentile_pct": round(iv_percentile, 1),
        "volatility_regime": "HIGH_IV (Expensive Options)" if iv_rank >= 50.0 else "LOW_IV (Cheap Options)",
        "optimal_options_play": strategy_recommendation
    }''',
        "test_code": '''res = analyze_iv_environment(65.0, 20.0, 80.0, 200)
assert res["iv_rank_pct"] == 75.0
assert "SELL_PREMIUM" in res["optimal_options_play"]''',
        "metadata": {"tags": ["options", "iv_rank", "implied_volatility", "iron_condor", "derivatives"]}
    },
    {
        "name": "options_iron_condor_payoff_matrix",
        "description": "Calculates maximum profit, maximum loss, breakeven strikes, and return on risk for an Options Iron Condor.",
        "category": "investments",
        "code": '''def calculate_iron_condor(put_buy_strike: float, put_sell_strike: float, call_sell_strike: float, call_buy_strike: float, net_credit_received: float) -> dict:
    wing_width = put_sell_strike - put_buy_strike
    max_profit = net_credit_received * 100.0
    max_loss = (wing_width - net_credit_received) * 100.0
    lower_breakeven = put_sell_strike - net_credit_received
    upper_breakeven = call_sell_strike + net_credit_received
    return_on_risk = (max_profit / max_loss) * 100.0 if max_loss > 0 else 0.0
    return {
        "max_profit_usd": round(max_profit, 2),
        "max_loss_usd": round(max_loss, 2),
        "lower_breakeven": round(lower_breakeven, 2),
        "upper_breakeven": round(upper_breakeven, 2),
        "return_on_risk_pct": round(return_on_risk, 2),
        "profit_zone": f"Between ${lower_breakeven} and ${upper_breakeven}"
    }''',
        "test_code": '''res = calculate_iron_condor(90.0, 95.0, 105.0, 110.0, 1.50)
assert res["max_profit_usd"] == 150.0
assert res["max_loss_usd"] == 350.0
assert res["lower_breakeven"] == 93.50''',
        "metadata": {"tags": ["options", "iron_condor", "payoff", "delta_neutral", "hedging"]}
    },

    # =========================================================================
    # 5. CRYPTOCURRENCY ON-CHAIN & LIQUIDITY ANALYSIS
    # =========================================================================
    {
        "name": "crypto_onchain_mvrv_nvt_analyzer",
        "description": "Calculates Bitcoin/Ethereum MVRV Z-Score and NVT Ratio to determine macro cycle market tops and generational bottoms.",
        "category": "investments",
        "code": '''def analyze_onchain_valuation(market_cap_usd: float, realized_cap_usd: float, daily_transaction_volume_usd: float, mvrv_std_dev: float = 1.0) -> dict:
    mvrv_ratio = market_cap_usd / realized_cap_usd if realized_cap_usd > 0 else 1.0
    # MVRV Z-score = (Market Cap - Realized Cap) / StdDev
    mvrv_z_score = (market_cap_usd - realized_cap_usd) / mvrv_std_dev if mvrv_std_dev > 0 else 0.0
    nvt_ratio = market_cap_usd / daily_transaction_volume_usd if daily_transaction_volume_usd > 0 else 0.0
    cycle_phase = "MACRO_TOP_EUPHORIA (High Risk / Take Profits)" if mvrv_ratio >= 3.5 else ("GENERATIONAL_BOTTOM (Deep Value Accumulation)" if mvrv_ratio <= 1.0 else "FAIR_VALUE_EXPANSION")
    return {
        "mvrv_ratio": round(mvrv_ratio, 2),
        "nvt_ratio": round(nvt_ratio, 1),
        "macro_cycle_status": cycle_phase,
        "is_undervalued_historically": mvrv_ratio <= 1.0
    }''',
        "test_code": '''res = analyze_onchain_valuation(500000000.0, 600000000.0, 10000000.0)
assert res["mvrv_ratio"] < 1.0
assert res["is_undervalued_historically"] is True''',
        "metadata": {"tags": ["crypto", "bitcoin", "onchain", "mvrv", "nvt", "cycles"]}
    },
    {
        "name": "crypto_perpetual_funding_rate_arbitrage",
        "description": "Calculates annualized funding yield for cash-and-carry delta neutral arbitrage and flags liquidation squeeze risks.",
        "category": "investments",
        "code": '''def analyze_perpetual_funding(funding_rate_8h_pct: float, open_interest_change_24h_pct: float) -> dict:
    # 3 funding epochs per day (8 hours each) = 1095 epochs per year
    annualized_funding_yield = funding_rate_8h_pct * 3.0 * 365.0
    squeeze_risk = "EXTREME_LONG_SQUEEZE_RISK (Market Overleveraged Long)" if funding_rate_8h_pct > 0.05 else ("EXTREME_SHORT_SQUEEZE_RISK (Negative Funding Cascading)" if funding_rate_8h_pct < -0.02 else "HEALTHY_EQUILIBRIUM")
    return {
        "funding_rate_8h_pct": funding_rate_8h_pct,
        "annualized_delta_neutral_yield_pct": round(annualized_funding_yield, 2),
        "oi_velocity_24h_pct": open_interest_change_24h_pct,
        "liquidation_cascade_risk": squeeze_risk,
        "arbitrage_viable": abs(annualized_funding_yield) >= 12.0
    }''',
        "test_code": '''res = analyze_perpetual_funding(0.03, 15.0)
assert res["annualized_delta_neutral_yield_pct"] > 30.0
assert res["arbitrage_viable"] is True''',
        "metadata": {"tags": ["crypto", "funding_rates", "perpetuals", "arbitrage", "delta_neutral"]}
    },

    # =========================================================================
    # 6. FOREX & ELLIOTT WAVE RULES
    # =========================================================================
    {
        "name": "forex_pip_value_lot_sizer",
        "description": "Calculates pip values, stop loss risk in dollars, and exact standard/mini/micro lot sizes for FX pairs.",
        "category": "investments",
        "code": '''def calculate_forex_lot_size(account_equity: float, risk_percent: float, stop_loss_pips: float, pair: str = "EURUSD", exchange_rate: float = 1.0850) -> dict:
    risk_amount_usd = account_equity * (risk_percent / 100.0)
    # For USD quote pairs (e.g., EUR/USD), 1 standard lot (100k units) = $10 per pip
    pip_value_per_standard_lot = 10.0 if pair.endswith("USD") else (10.0 / exchange_rate)
    total_pip_risk = stop_loss_pips * pip_value_per_standard_lot
    standard_lots = risk_amount_usd / total_pip_risk if total_pip_risk > 0 else 0.0
    return {
        "risk_capital_usd": round(risk_amount_usd, 2),
        "stop_loss_pips": stop_loss_pips,
        "standard_lots_100k": round(standard_lots, 2),
        "mini_lots_10k": round(standard_lots * 10.0, 1),
        "micro_lots_1k": round(standard_lots * 100.0, 0)
    }''',
        "test_code": '''res = calculate_forex_lot_size(50000.0, 1.0, 25.0, "EURUSD")
assert res["risk_capital_usd"] == 500.0
assert res["standard_lots_100k"] == 2.0''',
        "metadata": {"tags": ["forex", "fx", "pip", "lot_sizing", "currencies"]}
    },
    {
        "name": "elliott_wave_impulse_validator",
        "description": "Validates Elliott Wave impulse rules: Wave 2 cannot retrace >100% of Wave 1, Wave 3 cannot be shortest, Wave 4 cannot overlap Wave 1.",
        "category": "investments",
        "code": '''def validate_elliott_impulse(w1_start: float, w1_end: float, w2_end: float, w3_end: float, w4_end: float, w5_end: float) -> dict:
    w1_len = abs(w1_end - w1_start)
    w2_retrace = abs(w2_end - w1_end)
    w3_len = abs(w3_end - w2_end)
    w4_retrace = abs(w4_end - w3_end)
    w5_len = abs(w5_end - w4_end)
    rules_violated = []
    # Rule 1: Wave 2 never moves beyond the start of Wave 1
    if w2_end <= w1_start:
        rules_violated.append("RULE_1_VIOLATED: Wave 2 retraced 100%+ of Wave 1.")
    # Rule 2: Wave 3 is never the shortest impulse wave
    if w3_len < w1_len and w3_len < w5_len:
        rules_violated.append("RULE_2_VIOLATED: Wave 3 is the shortest among waves 1, 3, and 5.")
    # Rule 3: Wave 4 never enters the price territory of Wave 1
    if w4_end <= w1_end:
        rules_violated.append("RULE_3_VIOLATED: Wave 4 overlaps with Wave 1 price territory.")
    is_valid = len(rules_violated) == 0
    return {
        "is_valid_elliott_impulse": is_valid,
        "wave_3_dominant": w3_len > w1_len and w3_len > w5_len,
        "violations": rules_violated,
        "guidance": "VALID_5_WAVE_IMPULSE: Prepare for ABC corrective cycle" if is_valid else "INVALID_COUNT: Recalibrate wave degrees or interpret as complex diagonal."
    }''',
        "test_code": '''res = validate_elliott_impulse(100.0, 130.0, 115.0, 180.0, 140.0, 200.0)
assert res["is_valid_elliott_impulse"] is True
assert res["wave_3_dominant"] is True''',
        "metadata": {"tags": ["trading", "elliott_wave", "cycles", "fractals", "technical_analysis"]}
    }
]


def seed_trading_skills():
    logger.info("Initializing F.R.I.D.A.Y. Engine to register Trading & Investment Skills Catalog...")
    config = FridayConfig()
    engine = FridayEngine(config)
    
    total = len(TRADING_SKILLS_CATALOG)
    logger.info(f"Seeding {total} specialized financial & trading intelligence skills...")
    
    successful = 0
    for idx, skill in enumerate(TRADING_SKILLS_CATALOG, 1):
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
                logger.info(f"[{idx}/{total}] [OK] Seeded trading skill: {skill['name']}")
            else:
                logger.warning(f"[{idx}/{total}] [WARN] Failed to seed trading skill: {skill['name']}")
        except Exception as e:
            logger.error(f"[{idx}/{total}] [ERROR] Exception while seeding {skill['name']}: {e}")
            
    print(f"\nTRADING SKILL SEEDING COMPLETE: {successful}/{total} skills stored and indexed in SQLite & SKILL.md!")

if __name__ == "__main__":
    seed_trading_skills()
