{% snapshot stock_prices_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='symbol || date_ts',
      strategy='check',
      check_cols=['close', 'volume'],
    )
}}

SELECT
    symbol,
    date_ts,
    open,
    high,
    low,
    close,
    volume
FROM {{ source('raw', 'stock_data') }}

{% endsnapshot %}