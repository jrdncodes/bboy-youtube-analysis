-- schema.sql
-- Initializes database objects for the YouTube B-boy analysis project

CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS public.videos (
    video_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    published_at DATE NOT NULL,
    view_count BIGINT,
    ingested_at TIMESTAMP DEFAULT now()
);
