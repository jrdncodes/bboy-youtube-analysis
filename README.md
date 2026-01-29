## Overview

This project demonstrates a small end-to-end data pipeline that ingests
YouTube metadata via the YouTube Data API, loads it into PostgreSQL, and
enables SQL-based analysis.

The goal is to demonstrate clean ingestion, idempotency, and schema design
rather than scale.

## Tech Stack
- Python
- PostgreSQL
- YouTube Data API
- GitHub

## How It Works
1. Fetches video metadata via API
2. Normalizes nested JSON into a relational table
3. Inserts data safely using idempotent logic
4. Enables repeatable SQL analysis

## Future Improvements
- Enrich videos with view/like counts
- Track metric changes over time
- Schedule ingestion
