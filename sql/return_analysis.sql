-- return_analysis.sql

-- Return rate by category
SELECT 
  category,
  COUNT(*) AS total_orders,
  SUM(is_returned) AS total_returns,
  ROUND(SUM(is_returned) * 100.0 / COUNT(*), 2) AS return_rate_pct
FROM orders
GROUP BY category
ORDER BY return_rate_pct DESC;

-- Return rate by seller (top 20)
SELECT 
  seller_id,
  COUNT(*) AS total_orders,
  SUM(is_returned) AS total_returns,
  ROUND(SUM(is_returned) * 100.0 / COUNT(*), 2) AS return_rate_pct
FROM orders
GROUP BY seller_id
HAVING COUNT(*) >= 50
ORDER BY return_rate_pct DESC
LIMIT 20;

-- Return rate by region
SELECT 
  region,
  COUNT(*) AS total_orders,
  SUM(is_returned) AS total_returns,
  ROUND(SUM(is_returned) * 100.0 / COUNT(*), 2) AS return_rate_pct
FROM orders
GROUP BY region
ORDER BY return_rate_pct DESC;

-- 30-day rolling return rate overall
-- (For engines supporting window functions like Postgres/BigQuery)
WITH daily AS (
  SELECT
    order_date::date AS dt,
    COUNT(*) AS total_orders,
    SUM(is_returned) AS total_returns
  FROM orders
  GROUP BY 1
)
SELECT
  dt,
  SUM(total_returns) OVER (ORDER BY dt ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)::float
  / NULLIF(SUM(total_orders) OVER (ORDER BY dt ROWS BETWEEN 29 PRECEDING AND CURRENT ROW),0) AS rolling_30d_return_rate
FROM daily
ORDER BY dt;

-- Category x Region risk matrix
SELECT
  category,
  region,
  COUNT(*) AS total_orders,
  SUM(is_returned) AS total_returns,
  ROUND(SUM(is_returned) * 100.0 / COUNT(*), 2) AS return_rate_pct
FROM orders
GROUP BY category, region
HAVING COUNT(*) >= 50
ORDER BY return_rate_pct DESC;