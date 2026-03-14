# Youtube Analysis Pipeline
## A data pipeline for collecting, storing, and analyzing YouTube video metadata

## Introduction
Youtube Analysis Pipeline is a backend data pipeline that collects video metadata from Youtube. It transforms the data into a structured format, and stores it in PostGreSql for analysis.

The pipeline enables users to query and analyse video performance data. This includes views, published data and engagement metrics.

The current dataset focuses on Bboy-battle videos, however you may
change it to whatever you like.

This project is useful for anyone who want to explore youtube metadata and perform analytics on videos.

## Tech Stack
- Python
- PostgreSQL
- YouTube Data API
  
## Installation 

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/youtube-analysis.git
cd youtube-analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API credentials

Create a `.env` file in the project root and add your YouTube Data API key:

```env
YOUTUBE_API_KEY=your_api_key_here
```

### 4. Set up the database

Create a PostgreSQL database:

```sql
CREATE DATABASE youtube_analysis;
```

Run the schema file to initialize the tables:

```bash
psql youtube_analysis < schema.sql
```

### 5. Run the ingestion pipeline

```bash
python ingest.py
```
