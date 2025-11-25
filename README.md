**Overview**
This project implements a complete end-to-end ELT data analytics system using Apache Airflow, Snowflake, dbt, and a BI dashboard (Superset/Tableau).

It automates the extraction of historical stock data from the Yahoo Finance API, loads it into the Snowflake cloud data warehouse, transforms it using dbt’s staged modeling approach (staging → intermediate → mart), orchestrates these workflows with Airflow, and visualizes insights through interactive dashboards.

The pipeline computes essential technical indicators such as Moving Averages (MA3, MA7, MA30), RSI, momentum, and volatility, enabling deeper trend analysis and informed decision-making.

**Architecture:**
        
Data Source Layer
           YFinance API
Orchestration Layer
           Airflow ETL + Airflow dbt tasks
Data Warehouse Layer
           Snowflake (RAW → STAGING → INTERMEDIATE → MART → SNAPSHOT)
Transformation Layer
           dbt models (stg_stock_data, moving_averages, rsi, stock_analytics_mart)
Analytics Layer
           BI Dashboard (Superset/Tableau)

**Features**
- Automated ELT Pipeline
- Daily scheduled extraction and processing
- Automated dbt transformations and tests
- End-to-end workflow orchestration using Airflow

**Technical Analysis Metrics**
- Simple Moving Averages: MA3, MA7, MA30
- RSI (14-period)
- Price Momentum & Price Change
- Volatility (rolling standard deviation)

**Data Quality & Governance**
- dbt unique and not_null tests
- dbt_utils-based column tests
- Historical tracking with dbt SCD2 snapshot

**Visualization**
- Real-time dashboards for technical indicators
- Interactive filtering (symbol, date range)
- Charts for MA trends, RSI, volatility, and momentum

**Architecture Benefits**
- Modular and scalable design
- Easy to extend with new indicators
- Idempotent and reliable Snowflake transactions
- Reproducible transformations & documentation with dbt

**Prerequisites**
Python 3.8+
Apache Airflow 2.x
Snowflake account
dbt Core 1.10+
Docker & Docker Compose
Git
