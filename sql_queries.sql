-- Smart Retail Analytics: SQLite queries
-- Run these after dashboard.py creates data/retail_sales.db.
-- SQLite table name: sales

-- 1. Preview records
SELECT * FROM sales LIMIT 10;

-- 2. Total revenue and order count
SELECT ROUND(SUM(sales), 2) AS total_revenue,
       COUNT(DISTINCT order_id) AS total_orders
FROM sales;

-- 3. Top products by revenue
SELECT product, ROUND(SUM(sales), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;

-- 4. Monthly sales trend
SELECT strftime('%Y-%m', order_date) AS month,
       ROUND(SUM(sales), 2) AS revenue
FROM sales
GROUP BY month
ORDER BY month;

-- 5. Sales by region
SELECT region, ROUND(SUM(sales), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 6. Sales by category
SELECT category, ROUND(SUM(sales), 2) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;
