#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Virtual Paper Trading & Backtesting Simulator
===========================================================
Simulates automated order execution, trailing stop losses, take profits,
and portfolio accounting with zero real capital risk.
Stores portfolio state and trade history in SQLite WAL database.

Usage:
  python scripts/paper_trading_simulator.py --summary
  python scripts/paper_trading_simulator.py --buy NVDA --price 140.50 --qty 10 --sl 135.0 --tp 155.0
  python scripts/paper_trading_simulator.py --buy TATAMOTORS.NS --price 980 --qty 100 --sl 960 --tp 1020
  python scripts/paper_trading_simulator.py --sell NVDA --price 148.0
"""

import os
import sys
import json
import sqlite3
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data" / "market_chronos"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "paper_trading.db"

DEFAULT_STARTING_CASH_INR = 1000000.0  # ₹10 Lakh
DEFAULT_STARTING_CASH_USD = 10000.0    # $10,000


class PaperTradingSimulator:
    """Manages virtual portfolios, trade executions, and P&L tracking."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")

        # Portfolio Balance Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_balance (
                currency TEXT PRIMARY KEY,
                cash_balance REAL NOT NULL,
                initial_capital REAL NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)

        # Open Positions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS open_positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT UNIQUE NOT NULL,
                side TEXT NOT NULL,
                qty REAL NOT NULL,
                avg_entry_price REAL NOT NULL,
                current_price REAL NOT NULL,
                stop_loss REAL,
                take_profit REAL,
                opened_at TEXT NOT NULL,
                reason TEXT
            );
        """)

        # Trade History Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                qty REAL NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL NOT NULL,
                pnl_amount REAL NOT NULL,
                pnl_pct REAL NOT NULL,
                opened_at TEXT NOT NULL,
                closed_at TEXT NOT NULL,
                reason TEXT
            );
        """)

        # Initialize default capital if empty
        cursor.execute("SELECT COUNT(*) FROM portfolio_balance;")
        if cursor.fetchone()[0] == 0:
            now = datetime.datetime.now().isoformat()
            cursor.execute("INSERT INTO portfolio_balance VALUES ('INR', ?, ?, ?);", (DEFAULT_STARTING_CASH_INR, DEFAULT_STARTING_CASH_INR, now))
            cursor.execute("INSERT INTO portfolio_balance VALUES ('USD', ?, ?, ?);", (DEFAULT_STARTING_CASH_USD, DEFAULT_STARTING_CASH_USD, now))

        conn.commit()
        conn.close()

    def _get_currency(self, symbol: str) -> str:
        return "INR" if ".NS" in symbol or ".BO" in symbol else "USD"

    def buy(self, symbol: str, price: float, qty: float, sl: Optional[float] = None, tp: Optional[float] = None, reason: str = "Signal Execution") -> Dict[str, Any]:
        """Opens or adds to a long paper position."""
        curr = self._get_currency(symbol)
        total_cost = price * qty

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check cash balance
        cursor.execute("SELECT cash_balance FROM portfolio_balance WHERE currency = ?;", (curr,))
        row = cursor.fetchone()
        cash = row[0] if row else 0.0

        if cash < total_cost:
            conn.close()
            return {"status": "REJECTED", "reason": f"Insufficient {curr} cash balance ({cash:.2f} available, {total_cost:.2f} required)."}

        # Deduct cash
        new_cash = cash - total_cost
        now = datetime.datetime.now().isoformat()
        cursor.execute("UPDATE portfolio_balance SET cash_balance = ?, updated_at = ? WHERE currency = ?;", (new_cash, now, curr))

        # Check existing position
        cursor.execute("SELECT qty, avg_entry_price FROM open_positions WHERE symbol = ?;", (symbol,))
        pos = cursor.fetchone()

        if pos:
            old_qty, old_price = pos
            total_qty = old_qty + qty
            new_avg = ((old_qty * old_price) + total_cost) / total_qty
            cursor.execute("""
                UPDATE open_positions SET qty = ?, avg_entry_price = ?, current_price = ?, stop_loss = ?, take_profit = ?, opened_at = ?, reason = ?
                WHERE symbol = ?;
            """, (total_qty, new_avg, price, sl, tp, now, reason, symbol))
        else:
            cursor.execute("""
                INSERT INTO open_positions (symbol, side, qty, avg_entry_price, current_price, stop_loss, take_profit, opened_at, reason)
                VALUES (?, 'BUY', ?, ?, ?, ?, ?, ?, ?);
            """, (symbol, qty, price, price, sl, tp, now, reason))

        conn.commit()
        conn.close()

        return {
            "status": "FILLED",
            "action": "BUY",
            "symbol": symbol,
            "qty": qty,
            "fill_price": price,
            "total_cost": total_cost,
            "stop_loss": sl,
            "take_profit": tp,
            "remaining_cash": new_cash,
            "currency": curr,
        }

    def sell(self, symbol: str, price: float, reason: str = "Target / Exit Trigger") -> Dict[str, Any]:
        """Closes an open paper position and logs P&L."""
        curr = self._get_currency(symbol)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT qty, avg_entry_price, opened_at FROM open_positions WHERE symbol = ?;", (symbol,))
        pos = cursor.fetchone()

        if not pos:
            conn.close()
            return {"status": "ERROR", "reason": f"No open position found for {symbol}."}

        qty, entry_price, opened_at = pos
        revenue = price * qty
        cost = entry_price * qty
        pnl = revenue - cost
        pnl_pct = round(((price - entry_price) / entry_price) * 100, 2)
        now = datetime.datetime.now().isoformat()

        # Update cash
        cursor.execute("SELECT cash_balance FROM portfolio_balance WHERE currency = ?;", (curr,))
        cash = cursor.fetchone()[0]
        cursor.execute("UPDATE portfolio_balance SET cash_balance = ?, updated_at = ? WHERE currency = ?;", (cash + revenue, now, curr))

        # Record in history
        cursor.execute("""
            INSERT INTO trade_history (symbol, side, qty, entry_price, exit_price, pnl_amount, pnl_pct, opened_at, closed_at, reason)
            VALUES (?, 'SELL', ?, ?, ?, ?, ?, ?, ?, ?);
        """, (symbol, qty, entry_price, price, pnl, pnl_pct, opened_at, now, reason))

        # Remove from open positions
        cursor.execute("DELETE FROM open_positions WHERE symbol = ?;", (symbol,))
        conn.commit()
        conn.close()

        return {
            "status": "CLOSED",
            "symbol": symbol,
            "qty": qty,
            "entry_price": entry_price,
            "exit_price": price,
            "pnl_amount": round(pnl, 2),
            "pnl_pct": f"{pnl_pct}%",
            "currency": curr,
            "reason": reason,
        }

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Returns active balances, open positions with unrealized P&L, and historical stats."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Balances
        cursor.execute("SELECT currency, cash_balance, initial_capital FROM portfolio_balance;")
        balances = {row[0]: {"cash": round(row[1], 2), "initial": round(row[2], 2)} for row in cursor.fetchall()}

        # Open Positions
        cursor.execute("SELECT symbol, side, qty, avg_entry_price, current_price, stop_loss, take_profit, opened_at, reason FROM open_positions;")
        positions = []
        for r in cursor.fetchall():
            cur_price = r[4]
            entry = r[3]
            unrealized_pnl = round((cur_price - entry) * r[2], 2)
            unrealized_pct = round(((cur_price - entry) / entry) * 100, 2) if entry > 0 else 0.0
            positions.append({
                "symbol": r[0],
                "side": r[1],
                "qty": r[2],
                "entry_price": entry,
                "current_price": cur_price,
                "unrealized_pnl": unrealized_pnl,
                "unrealized_pct": f"{unrealized_pct}%",
                "stop_loss": r[5],
                "take_profit": r[6],
                "opened_at": r[7],
            })

        # History Stats
        cursor.execute("SELECT COUNT(*), SUM(pnl_amount), SUM(CASE WHEN pnl_amount > 0 THEN 1 ELSE 0 END) FROM trade_history;")
        h_row = cursor.fetchone()
        total_trades = h_row[0] or 0
        realized_pnl = round(h_row[1] or 0.0, 2)
        winning_trades = h_row[2] or 0
        win_rate = round((winning_trades / total_trades) * 100, 1) if total_trades > 0 else 0.0

        conn.close()

        return {
            "balances": balances,
            "active_positions_count": len(positions),
            "open_positions": positions,
            "performance_stats": {
                "total_completed_trades": total_trades,
                "realized_pnl": realized_pnl,
                "win_rate_pct": f"{win_rate}%",
                "winning_trades": winning_trades,
                "losing_trades": total_trades - winning_trades,
            },
        }


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Paper Trading Simulator")
    parser.add_argument("--summary", action="store_true", help="Print complete portfolio balance & positions summary")
    parser.add_argument("--buy", type=str, help="Symbol to buy")
    parser.add_argument("--sell", type=str, help="Symbol to sell")
    parser.add_argument("--price", type=float, help="Execution price")
    parser.add_argument("--qty", type=float, help="Share quantity")
    parser.add_argument("--sl", type=float, help="Stop loss price")
    parser.add_argument("--tp", type=float, help="Take profit price")
    parser.add_argument("--reason", type=str, default="Manual / AI Order", help="Trade rationale")
    args = parser.parse_args()

    sim = PaperTradingSimulator()

    if args.buy:
        if not args.price or not args.qty:
            print("Error: --price and --qty are required for buy orders.")
            return
        res = sim.buy(args.buy, price=args.price, qty=args.qty, sl=args.sl, tp=args.tp, reason=args.reason)
        print(json.dumps(res, indent=2))
    elif args.sell:
        if not args.price:
            print("Error: --price is required for sell orders.")
            return
        res = sim.sell(args.sell, price=args.price, reason=args.reason)
        print(json.dumps(res, indent=2))
    else:
        summary = sim.get_portfolio_summary()
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
