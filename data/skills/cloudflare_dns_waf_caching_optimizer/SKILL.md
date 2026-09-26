---
name: cloudflare_dns_waf_caching_optimizer
description: Calculates optimal Cloudflare Edge Cache TTL, Browser Cache TTL, SSL Full (Strict) requirements, and DDoS WAF rate limits.
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:47:21
---

# 🧠 Learned Skill: cloudflare_dns_waf_caching_optimizer

> Calculates optimal Cloudflare Edge Cache TTL, Browser Cache TTL, SSL Full (Strict) requirements, and DDoS WAF rate limits.

## Implementation Code
```python
def calculate_cloudflare_rules(traffic_daily_requests: int, static_assets_pct: float = 70.0, is_ecommerce: bool = False) -> dict:
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
    }
```

## Validation Tests
```python
res = calculate_cloudflare_rules(100000, 75.0, False)
assert res["recommended_edge_cache_ttl_seconds"] == 86400
assert res["estimated_bandwidth_saved_pct"] > 60.0
```
