---
name: financial_sentiment_scorer
display_name: Financial Sentiment & Materiality Scorer
category: NLP Intelligence
version: 1.0.0
description: Scores news and corporate disclosures from -1.0 (Bearish) to +1.0 (Bullish), estimating stock price materiality.
---

# Financial Sentiment & Materiality Scorer

## Overview
Scores news and corporate disclosures from -1.0 (Bearish) to +1.0 (Bullish), estimating stock price materiality.

## Category
**NLP Intelligence**

## Architecture & Logic
```python
def evaluate_sentiment_and_materiality(headline, article_body=''):
    # Combines domain-specific lexicon with LLM evaluation.
    # Filters out market noise (low-materiality fluff) from high-impact regulatory or financial shocks.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
