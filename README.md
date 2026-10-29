# QuantFoundation

Tests whether AI adoption by US healthcare companies is priced by the stock market, using public data on FDA device clearances, SEC filings, clinical trials, patents and private funding from 2015 onward.

## Research Questions

1. Does a firm-level Medical AI exposure score explain cross-sectional stock returns after controlling for the Fama-French five factors and momentum?
2. How do stock prices respond to FDA clearances of AI-enabled devices, large funding rounds and acquisitions? Is the reaction complete on announcement, or does the price keep drifting afterward?

Medical AI here covers imaging, diagnostics, drug discovery, clinical NLP, surgical robotics and remote monitoring.

## Approach

Data from each source is fetched into its raw form, normalized into a shared schema stored as Parquet and queried with DuckDB. Company names from different sources are matched to a single company identifier, so that an FDA clearance, a patent and a 10-K filing can be linked to the same listed stock.

### Medical AI Exposure Factor

Only 30 to 80 US-listed companies are pure-play Medical AI, which is too few for cross-sectional tests. Instead, every US healthcare stock (about 500) receives a continuous exposure score built from:

- similarity between the business description in its 10-K and Medical AI topics, measured with text embeddings
- FDA clearances of AI-enabled devices
- patents in health informatics and machine learning classes (CPC G16H, G06N)
- registered clinical trials involving AI

Stocks are sorted on the score into a long-short portfolio. Its returns are regressed on the Fama-French five factors plus momentum to estimate alpha. Fama-MacBeth cross-sectional regressions test whether the score predicts returns after controlling for firm characteristics.

### Event Study

Events are FDA clearances of AI-enabled devices, funding rounds, acquisitions and trial results. For each event, abnormal returns are measured against a market model and a Fama-French model estimated on a pre-event window. Cumulative abnormal returns over short windows around the announcement measure the immediate reaction. Longer post-event windows test for drift, which would indicate the information is not priced at once.

## Data Sources

All sources are public and free.

| Source | Data | Used for |
|---|---|---|
| yfinance | Daily prices | Returns for both studies |
| Kenneth French Data Library | Daily factor returns (FF5, momentum) | Risk adjustment |
| FDA AI-Enabled Medical Devices list, openFDA | Device clearances (510(k), De Novo, PMA) | Exposure score, events |
| SEC EDGAR | 10-K text, 8-K filings, Form D | Exposure score, events, private funding |
| ClinicalTrials.gov API | Trial registrations and results | Exposure score, events |
| PatentsView | Patent applications and grants | Exposure score |

## Methodology Safeguards

- **Point-in-time data.** Every record stores two dates: when the event happened and when it became public. A patent is filed about 18 months before it is published. A 10-K is filed 60 to 90 days after the fiscal year ends. Features at date *t* use only records already public at *t*.
- **No random splits.** Models are validated with walk-forward splits in time order. A final out-of-sample period is held back and used once.
- **Survivorship.** Ticker history is stored with validity dates, so delisted companies stay in the universe for the periods they traded.
- **Trading costs.** Backtests deduct transaction costs and slippage.

## Repository Structure

```
configs/          universe lists and parameters
dashboard/        Streamlit app
data/raw/         source files as downloaded (not tracked)
data/processed/   normalized Parquet tables (not tracked)
notebooks/        exploratory analysis
src/data/         fetchers, normalization, entity resolution
src/features/     exposure score, event calendar
src/models/       factor regressions, event study
src/backtest/     portfolio construction, costs, walk-forward
tests/
```

## Getting Started

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/AughustN/QuantFoundation.git
cd QuantFoundation
uv sync
cp .env.example .env    # add SEC User-Agent and openFDA key
uv run pytest
```
