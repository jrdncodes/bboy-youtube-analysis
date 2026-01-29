## Youtube Analysis

A small project demonstrating a complete data pipeline to fetch YouTube video metadata, store it in a database, and analyze it with SQL.

## Table of Contents
- Background
- Tech Stack
- How it works

## Background
This project is a learning/demo project for working with APIs, databases, and SQL analysis. It collects video information from YouTube using the YouTube Data API, stores it safely in PostgreSQL, and allows you to run queries on the data.

The focus is on:

Clean ingestion – making sure data is correct and consistent.

Idempotency – running the pipeline multiple times won’t create duplicates.

Good database design – structured tables for easy SQL analysis.

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
