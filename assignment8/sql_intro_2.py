import sqlite3
import pandas as pd

# Connect to the lesson.db database
try:
    conn = sqlite3.connect('../db/lesson.db')
    print("Successfully connected to lesson.db!")
    
    # Import CSV data into database (only if tables don't exist)
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    if not cursor.fetchone():
        print("Importing data from CSV files...")
        
        # Read products CSV and create table
        products_df = pd.read_csv('../csv/products.csv')
        products_df.to_sql('products', conn, if_exists='replace', index=False)
        print("Products table created and populated.")
        
        # Read line_items CSV and create table
        line_items_df = pd.read_csv('../csv/line_items.csv')
        line_items_df.to_sql('line_items', conn, if_exists='replace', index=False)
        print("Line_items table created and populated.")
    else:
        print("Tables already exist.")
    
    # Read data into DataFrame using JOIN
    print("\n--- Reading data into DataFrame ---\n")
    
    query = """
        SELECT 
            line_items.line_item_id,
            line_items.quantity,
            line_items.product_id,
            products.product_name,
            products.price
        FROM line_items
        JOIN products ON line_items.product_id = products.product_id
    """
    
    df = pd.read_sql_query(query, conn)
    
    print(f"DataFrame created with {len(df)} rows")
    print(f"\nFirst 5 rows of the DataFrame:")
    print(df.head())
    
    # Add a 'total' column (quantity * price)
    df['total'] = df['quantity'] * df['price']
    
    print(f"\nFirst 5 rows with 'total' column:")
    print(df.head())
    
    # Group by product_id and aggregate
    grouped_df = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    })
    
    print(f"\nGrouped DataFrame (first 5 rows):")
    print(grouped_df.head())
    
    # Sort by product_name
    grouped_df = grouped_df.sort_values('product_name')
    
    print(f"\nSorted by product_name (first 5 rows):")
    print(grouped_df.head())
    
    # Write DataFrame to CSV file
    output_file = 'order_summary.csv'
    grouped_df.to_csv(output_file)
    print(f"\nDataFrame written to {output_file}")
    
    # Close the connection
    conn.close()
    print("\nConnection closed.")
    
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
except FileNotFoundError as e:
    print(f"CSV file not found: {e}")
