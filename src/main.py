from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices


DATA_DIR = Path("data/sample")

# "yahoo" for remote Yahoo Finance data, "csv" for the local sample.
PROVIDER = "yahoo"
PROVIDER_LABELS = {
    "yahoo": "Yahoo Finance via yfinance",
    "csv": "Local CSV sample",
}

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
YAHOO_PERIOD = "1mo"
YAHOO_INTERVAL = "1d"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def get_market_prices(instrument, benchmark):
    if PROVIDER == "yahoo":
        instrument_prices = fetch_yahoo_prices(
            symbol=YAHOO_SYMBOLS[instrument["ticker"]],
            canonical_ticker=instrument["ticker"],
            period=YAHOO_PERIOD,
            interval=YAHOO_INTERVAL,
        )
        benchmark_prices = fetch_yahoo_prices(
            symbol=YAHOO_SYMBOLS[benchmark["ticker"]],
            canonical_ticker=benchmark["ticker"],
            period=YAHOO_PERIOD,
            interval=YAHOO_INTERVAL,
        )
        return instrument_prices, benchmark_prices

    prices = [normalize_price_row(row) for row in load_prices()]
    return (
        filter_prices(prices, instrument["ticker"]),
        filter_prices(prices, benchmark["ticker"]),
    )


def display_market_summary(title, market, prices):
    currency = market.get("currency", "")
    print(title)
    print(f"{market['ticker']} - {market['name']}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(f"First close  : {float(prices[0]['close']):.2f} {currency}")
    print(f"Last close   : {float(prices[-1]['close']):.2f} {currency}")


def display_market_metadata(title, market):
    print(f"{title} metadata")
    print(f"Ticker   : {market['ticker']}")
    print(f"Name     : {market['name']}")
    print(f"Currency : {market['currency']}")
    print(f"Market   : {market.get('market', 'N/A')}")


def display_comparison(instrument, benchmark, instrument_prices, benchmark_prices):
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    print("Comparison")
    print(f"Common observations : {len(aligned_instrument)}")
    print(f"Common period       : {get_first_date(aligned_instrument)} -> {get_last_date(aligned_instrument)}")
    print()
    print("Period return")
    print(f"{instrument['ticker']:<6}: {instrument_return:.2f}%")
    print(f"{benchmark['ticker']:<6}: {benchmark_return:.2f}%")
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} percentage points"
    )
    print()
    print("Base 100")
    print(
        f"{instrument['ticker']:<6}: "
        f"{instrument_base_100[0]['value']:.2f} -> "
        f"{instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<6}: "
        f"{benchmark_base_100[0]['value']:.2f} -> "
        f"{benchmark_base_100[-1]['value']:.2f}"
    )


def main():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices, benchmark_prices = get_market_prices(
        instrument,
        benchmark,
    )

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(PROVIDER_LABELS[PROVIDER])
    print()
    display_market_summary("Instrument", instrument, instrument_prices)
    print()
    display_market_summary("Benchmark", benchmark, benchmark_prices)
    print()
    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {LOOKBACK_LABEL}")
    print(f"Interval   : {INTERVAL_LABEL}")

    print()
    display_market_metadata("Instrument", instrument)
    print()
    display_market_metadata("Benchmark", benchmark)

    print()
    display_comparison(
        instrument,
        benchmark,
        instrument_prices,
        benchmark_prices,
    )


if __name__ == "__main__":
    main()