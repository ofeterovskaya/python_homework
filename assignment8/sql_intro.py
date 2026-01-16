import sqlite3

# Connect to SQLite database
try:
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect('../db/magazines.db')
    conn.execute("PRAGMA foreign_keys = 1")
    print("Successfully connected to the database!")
    
    # Create a cursor object
    cursor = conn.cursor()
    
    # Create publishers table
    try:
        cursor.execute('''
            CREATE TABLE publishers (
                publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        print("Publishers table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating publishers table: {e}")
    
    # Create magazines table
    try:
        cursor.execute('''
            CREATE TABLE magazines (
                magazine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
            )
        ''')
        print("Magazines table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating magazines table: {e}")
    
    # Create subscribers table
    try:
        cursor.execute('''
            CREATE TABLE subscribers (
                subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        print("Subscribers table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating subscribers table: {e}")
    
    # Create subscriptions table
    try:
        cursor.execute('''
            CREATE TABLE subscriptions (
                subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id)
            )
        ''')
        print("Subscriptions table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating subscriptions table: {e}")
    
    # Commit the changes
    conn.commit()
    print("All changes committed to the database.")
    
    # Define functions to add entries to tables
    
    def add_publisher(name):
        """Add a publisher to the database. Returns publisher_id."""
        try:
            # Check if publisher already exists
            cursor.execute("SELECT publisher_id FROM publishers WHERE name = ?", (name,))
            result = cursor.fetchone()
            
            if result:
                print(f"Publisher '{name}' already exists with ID {result[0]}")
                return result[0]
            
            # Insert new publisher
            cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
            conn.commit()
            publisher_id = cursor.lastrowid
            print(f"Publisher '{name}' added with ID {publisher_id}")
            return publisher_id
            
        except sqlite3.Error as e:
            print(f"Error adding publisher: {e}")
            return None
    
    def add_magazine(name, publisher_id):
        """Add a magazine to the database. Returns magazine_id."""
        try:
            # Check if magazine already exists
            cursor.execute("SELECT magazine_id FROM magazines WHERE name = ?", (name,))
            result = cursor.fetchone()
            
            if result:
                print(f"Magazine '{name}' already exists with ID {result[0]}")
                return result[0]
            
            # Verify publisher exists
            cursor.execute("SELECT publisher_id FROM publishers WHERE publisher_id = ?", (publisher_id,))
            if not cursor.fetchone():
                print(f"Error: Publisher with ID {publisher_id} does not exist")
                return None
            
            # Insert new magazine
            cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", 
                         (name, publisher_id))
            conn.commit()
            magazine_id = cursor.lastrowid
            print(f"Magazine '{name}' added with ID {magazine_id}")
            return magazine_id
            
        except sqlite3.Error as e:
            print(f"Error adding magazine: {e}")
            return None
    
    def add_subscriber(name, address):
        """Add a subscriber to the database. Returns subscriber_id.
        Checks for duplicate name AND address combination."""
        try:
            # Check if subscriber with same name AND address already exists
            cursor.execute(
                "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?", 
                (name, address)
            )
            result = cursor.fetchone()
            
            if result:
                print(f"Subscriber '{name}' at '{address}' already exists with ID {result[0]}")
                return result[0]
            
            # Insert new subscriber
            cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", 
                         (name, address))
            conn.commit()
            subscriber_id = cursor.lastrowid
            print(f"Subscriber '{name}' added with ID {subscriber_id}")
            return subscriber_id
            
        except sqlite3.Error as e:
            print(f"Error adding subscriber: {e}")
            return None
    
    def add_subscription(subscriber_id, magazine_id, expiration_date):
        """Add a subscription to the database. Returns subscription_id."""
        try:
            # Check if subscription already exists
            cursor.execute(
                "SELECT subscription_id FROM subscriptions WHERE subscriber_id = ? AND magazine_id = ?",
                (subscriber_id, magazine_id)
            )
            result = cursor.fetchone()
            
            if result:
                print(f"Subscription already exists with ID {result[0]}")
                return result[0]
            
            # Verify subscriber exists
            cursor.execute("SELECT subscriber_id FROM subscribers WHERE subscriber_id = ?", 
                         (subscriber_id,))
            if not cursor.fetchone():
                print(f"Error: Subscriber with ID {subscriber_id} does not exist")
                return None
            
            # Verify magazine exists
            cursor.execute("SELECT magazine_id FROM magazines WHERE magazine_id = ?", 
                         (magazine_id,))
            if not cursor.fetchone():
                print(f"Error: Magazine with ID {magazine_id} does not exist")
                return None
            
            # Insert new subscription
            cursor.execute(
                "INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)",
                (subscriber_id, magazine_id, expiration_date)
            )
            conn.commit()
            subscription_id = cursor.lastrowid
            print(f"Subscription added with ID {subscription_id}")
            return subscription_id
            
        except sqlite3.Error as e:
            print(f"Error adding subscription: {e}")
            return None
    
    # Populate tables with data
    print("\n--- Populating tables with data ---\n")
    
    # Add publishers
    pub1 = add_publisher("National Geographic")
    pub2 = add_publisher("Time Inc.")
    pub3 = add_publisher("Conde Nast")
    
    # Add magazines
    mag1 = add_magazine("National Geographic Magazine", pub1)
    mag2 = add_magazine("Time Magazine", pub2)
    mag3 = add_magazine("Vogue", pub3)
    mag4 = add_magazine("Wired", pub3)
    
    # Add subscribers
    sub1 = add_subscriber("Alice Johnson", "123 Main St, New York, NY")
    sub2 = add_subscriber("Bob Smith", "456 Oak Ave, Los Angeles, CA")
    sub3 = add_subscriber("Carol Davis", "789 Pine Rd, Chicago, IL")
    sub4 = add_subscriber("Alice Johnson", "321 Elm St, Boston, MA")  # Same name, different address
    
    # Add subscriptions
    add_subscription(sub1, mag1, "2026-12-31")
    add_subscription(sub1, mag2, "2026-06-30")
    add_subscription(sub2, mag3, "2027-03-15")
    add_subscription(sub3, mag1, "2026-09-30")
    add_subscription(sub4, mag4, "2027-01-31")
    
    # Final commit
    conn.commit()
    print("\n--- All data committed to database ---\n")
    
    # Task 4: SQL Queries
    print("\n--- SQL Queries ---\n")
    
    # Query to retrieve all information from the subscribers table
    try:
        cursor.execute("SELECT * FROM subscribers")
        subscribers = cursor.fetchall()
        
        print("All Subscribers:")
        print("-" * 70)
        for subscriber in subscribers:
            print(f"ID: {subscriber[0]}, Name: {subscriber[1]}, Address: {subscriber[2]}")
        print()
        
    except sqlite3.Error as e:
        print(f"Error retrieving subscribers: {e}")
    
    # Query to retrieve all magazines sorted by name
    try:
        cursor.execute("SELECT * FROM magazines ORDER BY name")
        magazines = cursor.fetchall()
        
        print("All Magazines (sorted by name):")
        print("-" * 70)
        for magazine in magazines:
            print(f"ID: {magazine[0]}, Name: {magazine[1]}, Publisher ID: {magazine[2]}")
        print()
        
    except sqlite3.Error as e:
        print(f"Error retrieving magazines: {e}")
    
    # Query to find magazines for a particular publisher using JOIN
    try:
        cursor.execute("""
            SELECT m.magazine_id, m.name, p.name as publisher_name
            FROM magazines m
            JOIN publishers p ON m.publisher_id = p.publisher_id
            WHERE p.name = 'Conde Nast'
        """)
        conde_nast_magazines = cursor.fetchall()
        
        print("Magazines published by 'Conde Nast':")
        print("-" * 70)
        for magazine in conde_nast_magazines:
            print(f"ID: {magazine[0]}, Magazine: {magazine[1]}, Publisher: {magazine[2]}")
        print()
        
    except sqlite3.Error as e:
        print(f"Error retrieving magazines for publisher: {e}")
    
    # Close the connection
    conn.close()
    print("Connection closed.")
    
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
