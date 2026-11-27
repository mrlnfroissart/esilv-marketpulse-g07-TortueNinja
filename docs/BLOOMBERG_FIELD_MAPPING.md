# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
- Instructor reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` (not present in this repository when this document was written; the mapping below was checked against the two sample files above)
- Live connectivity: not demonstrated

The sample is an instructor-approved fallback fixture. Its own `provenance` field states that the values are illustrative teaching values reused from `data/sample/prices.csv` and are not certified Bloomberg historical observations. This document does not prove live Bloomberg connectivity.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

The canonical tickers (`AAPL`, `SP500`) are the identifiers used by MarketPulse and `analytics.py`. The Bloomberg identifiers belong at the provider boundary only.

## Inputs inspected

| Role | `provider_identifier` | `canonical_ticker` | Observations | First date | Last date |
|---|---|---|---|---|---|
| Instrument | AAPL US Equity | AAPL | 21 | 2026-09-01 | 2026-09-30 |
| Benchmark | SPX Index | SP500 | 21 | 2026-09-01 | 2026-09-30 |

Structure of each series in the sample: `role`, `canonical_ticker`, `provider_identifier`, and a list of `observations`. Each observation has six keys: `observation_date`, `open_value`, `high_value`, `low_value`, `close_value`, `volume_value`.

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | Present. String in `YYYY-MM-DD` format, usable as is. |
| ticker | application mapping | `AAPL` or `SP500`. The sample series also carries `canonical_ticker`. |
| open | `open_value` | Present. JSON number; some values are integers (for example `248`, `6592`), so convert with `float()`. |
| high | `high_value` | Present. Same numeric note as `open`. |
| low | `low_value` | Present. Same numeric note as `open`. |
| close | `close_value` | Present. Same numeric note as `open`. |
| volume | `volume_value` | Present. Integer. Equal to `0` for every `SPX Index` observation in the sample. |

Important: `observation_date`, `open_value`, `high_value`, `low_value`, `close_value` and `volume_value` are teaching wrapper keys. They are not Bloomberg field mnemonics. Real Bloomberg field names were not observed in this session and are not listed here.

Teaching wrapper key != Bloomberg LIVE field mnemonic.

## Canonical ticker preservation

Target canonical rows keep the MarketPulse tickers:

```python
{
    "date": "2026-09-01",
    "ticker": "SP500",
    "open": 6592.0,
    "high": 6615.0,
    "low": 6580.0,
    "close": 6600.0,
    "volume": 0,
}
```

The sample values above only illustrate the shape. `SPX Index` must never appear as a ticker in canonical rows.

## Checks done against the expected reference

- `bloomberg_reference_expected.json` has `access_mode = approved_sample` and `source_fixture = data/sample/bloomberg_reference_sample.json`.
- It contains 42 canonical rows: 21 for `AAPL` and 21 for `SP500`.
- Each canonical row uses exactly `date`, `ticker`, `open`, `high`, `low`, `close`, `volume`.

## TD10 handoff

- Access mode: APPROVED_SAMPLE (live connectivity not demonstrated)
- Instrument identifier: `AAPL US Equity` (canonical ticker `AAPL`)
- Benchmark identifier: `SPX Index` (canonical ticker `SP500`)
- Date representation: string `YYYY-MM-DD` in `observation_date`
- Input structure: `series` list; each series has `role`, `canonical_ticker`, `provider_identifier` and `observations`
- Missing fields: none in the sample
- Special normalization notes:
  - rename the teaching wrapper keys to the canonical fields (see the mapping table);
  - convert open, high, low and close to `float`, and volume to `int`;
  - keep the canonical ticker (`AAPL`, `SP500`) in the output rows, not the Bloomberg identifier;
  - `SPX Index` volume is `0` in the sample;
  - the dates in the sample have no weekend rows, and `2026-09-07` is absent, so rely on `align_series()` and do not compare rows by list position.
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
