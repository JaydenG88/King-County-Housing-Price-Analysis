# System Design

> The ETL pipeline (dashed box below) is disabled as of October 2026 — see the status note in [README.md](README.md).
> The API and frontend are unaffected and still serve the last data collected.

```mermaid
flowchart TD
    subgraph ETL["ETL Pipeline (GitHub Actions, weekly cron — currently disabled)"]
        direction TB
        Scraper["scraper.py<br/>Selenium + selenium-stealth<br/>scrapes Redfin listings per city"]
        Cleaning["data_cleaning.py<br/>Pandas/NumPy/SciPy<br/>dedupe, validate, winsorize outliers,<br/>compute price/sqft, price quartiles"]
        Analysis["data_analysis.py<br/>Pandas aggregation<br/>averages, correlations, best-valued listings,<br/>price-category frequency, price trends"]
        Scraper --> Cleaning --> Analysis
    end

    Redfin[("Redfin.com")]
    Redfin -.->|HTML listings| Scraper

    subgraph DB["MongoDB Atlas"]
        direction TB
        RawColl[("raw_king_co_listings_data")]
        CleanColl[("cleaned_king_co_listings_data")]
        FindingsColl[("king_co_housing_findings")]
    end

    Scraper -->|raw listings| RawColl
    Cleaning -->|cleaned listings| CleanColl
    Analysis -->|findings| FindingsColl

    subgraph API["Backend: Flask REST API (Render)"]
        Routes["routes.py<br/>/api/averages, /api/correlations,<br/>/api/lowest_price_per_sqft, /api/price_trends,<br/>/api/price_category_frequency, /api/regions, /api/date"]
        Services["housing_services.py<br/>queries findings, sanitizes NaN -> null"]
        Routes --> Services
    end

    FindingsColl -->|pymongo queries| Services

    subgraph Frontend["Frontend: Next.js Dashboard (Vercel)"]
        Dashboard["Charts: averages bar chart, price trends time-series,<br/>correlation heatmap, price quartile histogram,<br/>best-valued listings by region<br/>(Recharts / ApexCharts)"]
    end

    Services -->|JSON| Dashboard
    User(("User browser")) --> Dashboard
```

## Component notes

- **ETL pipeline** (`backend/data_pipeline/`) — ran weekly via GitHub Actions (`.github/workflows/main.yml`), scraping all King County cities listed in `scraper_config.py`, cleaning/validating with Pandas, and writing aggregate findings to MongoDB. Disabled because Redfin blocks GitHub-hosted runner IPs.
- **Database** (`backend/database/`) — MongoDB Atlas (free M0 tier). Three collections: raw scraped listings, cleaned/validated listings, and precomputed findings the API serves directly (so the API never does heavy aggregation at request time).
- **Backend API** (`backend/housing_data_API/`) — Flask app on Render, rate-limited with Flask-Limiter, reads precomputed findings from MongoDB and returns JSON to the frontend.
- **Frontend** (`frontend/king-county-dashboard/`) — Next.js dashboard on Vercel, renders the charts described in the main README.
