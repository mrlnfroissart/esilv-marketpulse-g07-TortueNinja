# Checkpoint B - Marlon Froissart (mrlnfroissart)

Team repository: mrlnfroissart/esilv-marketpulse-g07-TortueNinja

## 01_pull_request.png
PR #5 `feat: add Yahoo Finance provider`, opened by me from `feature/yahoo-provider` into `main`.
It adds `src/providers/__init__.py` and `src/providers/yahoo_provider.py`, records `yfinance`
in `requirements.txt` and switches `src/main.py` to the Yahoo provider path.
Review requested from josephgardon.

## 02_code_review.png
My review of Joseph's TD07 PR (`feature/analytics-comparison`), after running it locally.
I checked that `align_series()` builds both series from the same common dates, that relative
performance is instrument minus benchmark, that `analytics.py` has no provider-specific
identifier, and that no percentage is hard-coded. Inline comments suggest raising a clear
error when there are no common dates and guarding against a zero first close.

## 03_yahoo_market_data.png
`python src/main.py` retrieving live data from Yahoo Finance via yfinance
(period `1mo`, interval `1d`). AAPL and SP500 each return 23 daily observations
from 2026-10-26 to 2026-11-25. The benchmark keeps its canonical ticker `SP500`;
the Yahoo symbol `^GSPC` is used only inside the provider.

## 04_instrument_benchmark.png
The same Yahoo run fed into the unchanged TD07 `analytics.py`:
AAPL +3.39%, SP500 -6.43%, relative performance +9.83 percentage points
(instrument minus benchmark). Base 100: AAPL 100.00 -> 103.39, SP500 100.00 -> 93.57.
