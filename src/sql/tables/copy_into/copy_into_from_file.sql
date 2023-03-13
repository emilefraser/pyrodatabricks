COPY INTO retail_db.orders
FROM (
    SELECT order_id::int order_id, order_date::string order_date, 
        order_customer_id::int order_customer_id, order_status::string order_status
    FROM 'dbfs:/public/retail_db_json/orders'
)
FILEFORMAT = JSON;