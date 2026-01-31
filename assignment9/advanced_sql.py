import sqlite3

# Connect to the database
conn = sqlite3.connect("../db/lesson.db")
conn.execute("PRAGMA foreign_keys = 1")

cursor = conn.cursor()

# SQL query: Find the total price of each of the first 5 orders
# Joins orders, line_items, and products tables
# Groups by order_id and sums the product of price and quantity
sql_query = """
SELECT 
    o.order_id, 
    SUM(p.price * li.quantity) as total_price
FROM orders o
JOIN line_items li ON o.order_id = li.order_id
JOIN products p ON li.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id
LIMIT 5
"""

try:
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    print("Order ID | Total Price")
    print("-" * 30)
    for row in results:
        order_id, total_price = row
        print(f"{order_id:8} | ${total_price:.2f}")
        
except sqlite3.Error as e:
    print(f"Error executing query: {e}")

finally:
    conn.close()
    print("\nDatabase connection closed.")

# Task 2: Understanding Subqueries
print("\n" + "="*60)
print("Task 2: Average Order Price per Customer (using subquery)")
print("="*60 + "\n")

# Reconnect to the database
conn = sqlite3.connect("../db/lesson.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

# SQL query with subquery: Find average price of orders for each customer
# Subquery calculates total price for each order
# Main query joins customers with order totals and averages them per customer
sql_query_2 = """
SELECT 
    c.customer_name, 
    AVG(order_totals.total_price) as average_total_price
FROM customers c
LEFT JOIN (
    SELECT 
        o.customer_id AS customer_id_b, 
        SUM(p.price * li.quantity) as total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id, o.customer_id
) AS order_totals ON c.customer_id = order_totals.customer_id_b
GROUP BY c.customer_id, c.customer_name
ORDER BY c.customer_name
"""

try:
    cursor.execute(sql_query_2)
    results = cursor.fetchall()
    
    print("Customer Name                        | Avg Order Price")
    print("-" * 60)
    for row in results:
        customer_name, avg_price = row
        if avg_price is not None:
            print(f"{customer_name:40} | ${avg_price:.2f}")
        else:
            print(f"{customer_name:40} | No orders")

except sqlite3.Error as e:
    print(f"Error executing query: {e}")

finally:
    conn.close()
    print("\nDatabase connection closed.")

# Task 3: An Insert Transaction Based on Data
print("\n" + "="*60)
print("Task 3: Create New Order Transaction")
print("="*60 + "\n")

# Reconnect to the database
conn = sqlite3.connect("../db/lesson.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

try:
    # Begin transaction
    conn.execute("BEGIN TRANSACTION")

    # Step 1: Get customer_id for 'Perez and Sons'
    cursor.execute("SELECT customer_id FROM customers WHERE customer_name = ?", 
                   ('Perez and Sons',))
    customer_result = cursor.fetchone()
    if not customer_result:
        raise Exception("Customer 'Perez and Sons' not found")
    customer_id = customer_result[0]
    print(f"Customer ID for 'Perez and Sons': {customer_id}")

    # Step 2: Get employee_id for Miranda Harris
    cursor.execute("SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?",
                   ('Miranda', 'Harris'))
    employee_result = cursor.fetchone()
    if not employee_result:
        raise Exception("Employee 'Miranda Harris' not found")
    employee_id = employee_result[0]
    print(f"Employee ID for 'Miranda Harris': {employee_id}")

    # Step 3: Get 5 least expensive products
    cursor.execute("SELECT product_id, product_name, price FROM products ORDER BY price LIMIT 5")
    products = cursor.fetchall()
    print(f"\n5 Least Expensive Products:")
    for product in products:
        print(f"  Product ID {product[0]}: {product[1]} - ${product[2]:.2f}")

    # Step 4: Create new order with today's date
    cursor.execute("""
        INSERT INTO orders (customer_id, employee_id, date) 
        VALUES (?, ?, ?) 
        RETURNING order_id
    """, (customer_id, employee_id, '2026-01-30'))

    order_result = cursor.fetchone()
    order_id = order_result[0]
    print(f"\nCreated Order ID: {order_id}")

    # Step 5: Create line_items for each of the 5 products (10 of each)
    print("\nCreating line items...")
    for product in products:
        product_id = product[0]
        cursor.execute("""
            INSERT INTO line_items (order_id, product_id, quantity)
            VALUES (?, ?, ?)
        """, (order_id, product_id, 10))
        print(f"  Added 10 units of product {product_id}")

    # Commit the transaction
    conn.commit()
    print("\nTransaction committed successfully!")

    # Step 6: Query the line_items with JOIN to show the result
    cursor.execute("""
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
        WHERE li.order_id = ?
    """, (order_id,))

    line_items = cursor.fetchall()

    print(f"\nLine Items for Order {order_id}:")
    print("-" * 60)
    print("Line Item ID | Quantity | Product Name")
    print("-" * 60)
    for item in line_items:
        print(f"{item[0]:12} | {item[1]:8} | {item[2]}")

except sqlite3.Error as e:
    conn.rollback()
    print(f"Transaction failed and rolled back: {e}")
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
finally:
    conn.close()
    print("\nDatabase connection closed.")

# Task 4: Aggregation with HAVING
print("\n" + "="*60)
print("Task 4: Employees with More Than 5 Orders")
print("="*60 + "\n")

# Reconnect to the database
conn = sqlite3.connect("../db/lesson.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

# SQL query: Find employees with more than 5 orders
# Uses JOIN, GROUP BY, COUNT, and HAVING
sql_query_4 = """
SELECT 
    e.employee_id, 
    e.first_name, 
    e.last_name, 
    COUNT(o.order_id) as order_count
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC
"""

try:
    cursor.execute(sql_query_4)
    results = cursor.fetchall()

    print("Employee ID | First Name    | Last Name     | Order Count")
    print("-" * 60)
    for row in results:
        emp_id, first_name, last_name, order_count = row
        print(f"{emp_id:11} | {first_name:13} | {last_name:13} | {order_count}")

except sqlite3.Error as e:
    print(f"Error executing query: {e}")

finally:
    conn.close()
    print("\nDatabase connection closed.")
