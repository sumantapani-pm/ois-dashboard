# OIS — Operational Intelligence System

**Data over dashboards. Anomalies to action.**

OIS is a proprietary operational intelligence system that closes
the gap between BI observation and operational remediation.

## Architecture
- Layer 1: Data Foundation (DuckDB + dbt Core + Prefect)
- Layer 2: Insight Engine (Threshold Rules + Anomaly State Machine)
- Layer 3: Action Layer (React + FastAPI + Resolution Tracker)

## Licence
AGPL-3.0 — see LICENSE file.

## Stack
Frontend: React + Vite + Tailwind CSS + shadcn/ui + Apache ECharts
Backend: Python FastAPI
Database: Supabase (PostgreSQL) + DuckDB
Transformation: dbt Core
Orchestration: Prefect Cloud
Hosting: Vercel (FE) + Render (BE)
