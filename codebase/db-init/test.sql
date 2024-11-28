-- SELECT * FROM orders WHERE id =3;

-- UPDATE orders
-- SET quantity = 2,
--     total_price = 2 * (SELECT price FROM products WHERE id = orders.product_id)
-- WHERE id = 10; -- Update the order with ID 10

-- UPDATE orders SET quantity = %s, total_price = %s WHERE id = %s RETURNING id, product_id, quantity (1, 9.99, 10)
-- UPDATE users SET sid = %s, username = %s, email = %s WHERE id = %s RETURNING id, sid, username, email ('c', 'c', 'c@example.com', 1)

