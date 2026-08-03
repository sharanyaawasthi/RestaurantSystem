import mysql.connector

# Connecting python to mysql
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gungun05@mysql",  
    database="restaurant_db"
)


cursor = db.cursor()

# MySQL Helper Reference:
# - cursor.execute(): Runs/executes an SQL query in MySQL.
# - cursor.fetchall(): Retrieves/fetches all resulting rows from a SELECT query.
# - cursor.fetchone(): Retrieves/fetches a single resulting row from a SELECT query.
# - cursor.lastrowid: Returns the auto-generated primary key ID created by the latest INSERT.
# - db.commit(): Saves changes (like INSERT or UPDATE) permanently to the database.

#Since the menu would be shown frequently, I created a function for easier printing of the menu
def display_menu():
    print("\n--- MENU ITEMS ---")
    cursor.execute("SELECT item_id, item_name, category, price FROM MenuItems WHERE is_available = TRUE;")
    for item_id, name, category, price in cursor.fetchall():
        print(f"ID: {item_id} | {name} ({category}) - ${price}")

while True:
    print("\n================ ONLINE RESTAURANT SYSTEM ================")
    print("1. Customer Sign Up")
    print("2. Customer Sign In")
    print("3. Staff Sign In")
    print("4. Exit")
    
    choice = input("\nSelect an option (1-4): ").strip()

    #Customer sign up:
    if choice == '1':
        print("\n--- CUSTOMER SIGN UP ---")
        full_name = input("Enter Full Name: ").strip()
        email = input("Enter Email: ").strip()
        phone = input("Enter Phone Number: ").strip()

        cursor.execute(
            "INSERT INTO Customers (full_name, email, phone_nb) VALUES (%s, %s, %s);",
            (full_name, email, phone)
        )
        db.commit()
        customer_id = cursor.lastrowid

        print("\n--- ENTER ADDRESS DETAILS ---")
        street = input("Street Address: ").strip()
        city = input("City: ").strip()
        state = input("State: ").strip()
        zip_code = input("Zip Code: ").strip()

        cursor.execute(
            "INSERT INTO Addresses (customer_id, street_address, city, state, zip_code) VALUES (%s, %s, %s, %s, %s);",
            (customer_id, street, city, state, zip_code)
        )
        db.commit()

        print(f"\nSuccess! Registration complete. Your Customer ID is: {customer_id}")

    #Customer Sign In:
    elif choice == '2':
        customer_id = int(input("\nEnter your Customer ID: "))
        cursor.execute("SELECT customer_id, full_name FROM Customers WHERE customer_id = %s;", (customer_id,))
        customer = cursor.fetchone()

        if not customer:
            print("Customer ID not found!")
            continue

        print(f"\nWelcome back, {customer[1]}!")

        while True:
            print(f"\n--- CUSTOMER MENU (ID: {customer_id}) ---")
            print("1. View Menu")
            print("2. Place an Order")
            print("3. View Order History")
            print("4. Sign Out")

            c_choice = input("Select an option (1-4): ").strip()

            if c_choice == '1':
                display_menu()

            elif c_choice == '2':
                # Get customer saved address
                cursor.execute("SELECT address_id, street_address FROM Addresses WHERE customer_id = %s;", (customer_id,))
                addresses = cursor.fetchall()
                
                if not addresses:
                    print("No address found for this customer.")
                    continue

                print("\nSaved Addresses:")
                for addr in addresses:
                    print(f"Address ID: {addr[0]} | {addr[1]}")
                address_id = int(input("Select Address ID for delivery: "))

                # Create Order record
                cursor.execute("INSERT INTO Orders (customer_id, address_id, order_status) VALUES (%s, %s, 'Placed');", (customer_id, address_id))
                db.commit()
                order_id = cursor.lastrowid

                total_cost = 0.0

                # Multi-item ordering loop
                while True:
                    display_menu()
                    item_id = int(input("\nEnter Menu Item ID to order: "))
                    quantity = int(input("Enter Quantity: "))

                    cursor.execute("SELECT price FROM MenuItems WHERE item_id = %s;", (item_id,))
                    result = cursor.fetchone()
                    
                    if result:
                        price = float(result[0])
                        cursor.execute("INSERT INTO OrderItems (order_id, item_id, quantity) VALUES (%s, %s, %s);", (order_id, item_id, quantity))
                        total_cost += price * quantity
                        print(f"Added item to order. Current total: ${total_cost:.2f}")
                    else:
                        print("Invalid Menu Item ID.")

                    more = input("\nDo you want to add anything else? (y/n): ").strip().lower()
                    if more != 'y':
                        break

                db.commit()
                print(f"\nOrder #{order_id} placed successfully! Total cost: ${total_cost:.2f}")

            #See order history
            elif c_choice == '3':
                print("\n--- ORDER HISTORY ---")
                query = """
                    SELECT o.order_id, o.order_date, m.item_name, oi.quantity, (m.price * oi.quantity), o.order_status
                    FROM Orders o
                    JOIN OrderItems oi ON o.order_id = oi.order_id
                    JOIN MenuItems m ON oi.item_id = m.item_id
                    WHERE o.customer_id = %s;
                """
                cursor.execute(query, (customer_id,))
                orders = cursor.fetchall()
                if not orders:
                    print("No order history found.")
                else:
                    for r in orders:
                        print(f"Order #{r[0]} | Date: {r[1]} | Item: {r[2]} (x{r[3]}) | Total: ${r[4]:.2f} | Status: {r[5]}")

            elif c_choice == '4':
                break

    #Staff sign in:
    elif choice == '3':
        staff_id = int(input("\nEnter Staff ID: "))
        cursor.execute("SELECT staff_id, full_name FROM Staff WHERE staff_id = %s;", (staff_id,))
        staff = cursor.fetchone()

        if not staff:
            print("Staff ID not found. Creating new staff entry...")
            name = input("Enter Full Name: ").strip()
            role = input("Enter Role: ").strip()
            cursor.execute("INSERT INTO Staff (full_name, staff_role) VALUES (%s, %s);", (name, role))
            db.commit()
            staff_id = cursor.lastrowid
            print(f"New Staff created with ID: {staff_id}")

        while True:
            print(f"\n--- STAFF MENU (ID: {staff_id}) ---")
            print("1. Add New Menu Item")
            print("2. Change Order Status")
            print("3. View Order Statistics")
            print("4. Sign Out")

            s_choice = input("Select an option (1-4): ").strip()

            if s_choice == '1':
                name = input("Enter Item Name: ").strip()
                category = input("Enter Category: ").strip()
                price = float(input("Enter Price: "))
                cursor.execute("INSERT INTO MenuItems (item_name, category, price) VALUES (%s, %s, %s);", (name, category, price))
                db.commit()
                print(f"Item '{name}' added to menu.")

            elif s_choice == '2':
                order_id = int(input("Enter Order ID: "))
                new_status = input("Enter New Status (Placed, Out for Delivery, Delivered): ").strip()
                cursor.execute("UPDATE Orders SET order_status = %s WHERE order_id = %s;", (new_status, order_id))
                db.commit()
                print(f"Order #{order_id} status updated to '{new_status}'.")

            elif s_choice == '3':
                print("\n--- ORDER STATISTICS ---")
                print("1. Total revenue collected so far")
                print("2. Most purchased item")
                print("3. Customers that spent more than $50")
                print("4. Customers who bought Lobster Risotto")

                stat_choice = input("\nSelect a statistic option (1-4): ").strip()

                if stat_choice == '1':
                    cursor.execute("""
                        SELECT SUM(m.price * oi.quantity) 
                        FROM OrderItems oi 
                        JOIN MenuItems m ON oi.item_id = m.item_id;
                    """)
                    rev_res = cursor.fetchone()[0]
                    total_rev = float(rev_res) if rev_res else 0.0
                    print(f"\nTotal Revenue Collected so far: ${total_rev:.2f}")

                elif stat_choice == '2':
                    cursor.execute("""
                        SELECT m.item_name, SUM(oi.quantity) AS total_sold
                        FROM OrderItems oi
                        JOIN MenuItems m ON oi.item_id = m.item_id
                        GROUP BY m.item_id, m.item_name
                        ORDER BY total_sold DESC
                        LIMIT 1;
                    """)
                    top = cursor.fetchone()
                    if top:
                        print(f"\nMost Purchased Item: {top[0]} ({top[1]} units sold)")
                    else:
                        print("\nNo items sold yet.")

                elif stat_choice == '3':
                    print("\n--- CUSTOMERS WHO SPENT MORE THAN $50 ---")
                    cursor.execute("""
                        SELECT c.full_name, SUM(m.price * oi.quantity) AS total_spent
                        FROM Customers c
                        JOIN Orders o ON c.customer_id = o.customer_id
                        JOIN OrderItems oi ON o.order_id = oi.order_id
                        JOIN MenuItems m ON oi.item_id = m.item_id
                        GROUP BY c.customer_id, c.full_name
                        HAVING total_spent > 50;
                    """)
                    rows = cursor.fetchall()
                    if not rows:
                        print("No customers have spent more than $50 yet.")
                    else:
                        for name, spent in rows:
                            print(f"Customer: {name} | Total Spent: ${spent:.2f}")

                elif stat_choice == '4':
                    print("\n--- CUSTOMERS WHO BOUGHT LOBSTER RISOTTO ---")
                    cursor.execute("""
                        SELECT DISTINCT c.full_name
                        FROM Customers c
                        JOIN Orders o ON c.customer_id = o.customer_id
                        JOIN OrderItems oi ON o.order_id = oi.order_id
                        JOIN MenuItems m ON oi.item_id = m.item_id
                        WHERE m.item_name LIKE '%Lobster%';
                    """)
                    lobster_custs = cursor.fetchall()
                    if not lobster_custs:
                        print("No customers have ordered Lobster Risotto yet.")
                    else:
                        for r in lobster_custs:
                            print(f"Customer: {r[0]}")
                else:
                    print("Invalid statistic option.")

            elif s_choice == '4':
                break

    #Exit
    elif choice == '4':
        print("\nThank you so much!")
        cursor.close()
        db.close()
        break

    #Invalid choice:
    else:
        print("\nInvalid choice. Please enter a number between 1 and 4.")