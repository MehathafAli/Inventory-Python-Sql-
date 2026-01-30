 

# ---------------- DB CONNECTION ----------------

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ali@78612",
    database="fruit_store"
)
cursor = db.cursor()

# ---------------- OWNER FUNCTIONS ----------------

def add_fruit():
    name = input("Fruit name: ").lower()
    cursor.execute("select id,name from fruits where name=%s",(name,))
    data = cursor.fetchone()
    if data:
        print("Fruit alredy exits")
        return
    
    qty = float(input("Quantity: "))
    cp = int(input("Cost price: "))
    sp = int(input("Selling price: "))

    
    cursor.execute(
        "INSERT INTO fruits (name, quantity, cost_price, selling_price) VALUES (%s,%s,%s,%s)",
        (name, qty, cp, sp)
    )
    db.commit()
    print("Fruit added successfully")


def remove_fruit():
    name = input("Fruit to remove: ").lower()

    cursor.execute("SELECT id FROM fruits WHERE name=%s", (name,))
    data = cursor.fetchone()
    if not data:
        print("Fruit not found")
        return
    fid = data[0]
    cursor.execute("SELECT COUNT(*) FROM sales WHERE fruit_id=%s", (fid,))
    count = cursor.fetchone()[0]
    if count > 0:
        print("Cannot delete fruit. Sales history exists.")
        return
    cursor.execute("DELETE FROM fruits WHERE id=%s", (fid,))
    db.commit()
    print("Fruit removed")


def update_fruit():
    name = input("Fruit to update: ").lower()
    cursor.execute("Select id,name from fruits where name=%s",(name,))
    data=cursor.fetchone()
    if not data:
        print("Fruit not found")
        return 
    qty = float(input("New quantity: "))
    cp = int(input("New cost price: "))
    sp = int(input("New selling price: "))

    cursor.execute("""
        UPDATE fruits 
        SET quantity=%s, cost_price=%s, selling_price=%s
        WHERE name=%s
    """, (qty, cp, sp, name))

    db.commit()
    print("Fruit updated")

def view_inventory():
    cursor.execute("SELECT name, quantity, selling_price FROM fruits")

    print(f"{'ITEM':<12} {'QTY':>6} {'PRICE':>8}")
    print("-" * 28)

    for name, qty, price in cursor.fetchall():
        print(f"{name:<12} {qty:>6} {price:>8}")

def customer_report():
    date = input("Enter date (YYYY-MM-DD): ")

    cursor.execute("""
        SELECT c.id, c.name, c.phone,
               SUM(s.total) AS total_spent,
               DATE(s.sale_date) AS sale_day
        FROM customers c
        JOIN sales s ON c.id = s.customer_id
        WHERE DATE(s.sale_date) = %s
        GROUP BY c.id, sale_day
        ORDER BY sale_day DESC
    """, (date,))

    rows = cursor.fetchall()
    if not rows:
        print("No customers found for this date")
        return

    print(f"\n{'ID':<4} {'NAME':<12} {'PHONE':<12} {'TOTAL':>8} {'DATE':<12}")
    print("-" * 50)

    for id, name, phone, total, sale_day in rows:
        print(f"{id:<4} {name:<12} {phone:<12} {total:>8} {sale_day:%Y-%m-%d}")

def profit_report():
    date = input("Enter date (YYYY-MM-DD): ")

    cursor.execute("""
        SELECT f.name, s.sale_date,
               SUM((f.selling_price - f.cost_price) * s.qty) AS profit
        FROM sales s
        JOIN fruits f ON s.fruit_id = f.id
        WHERE s.sale_date = %s
        GROUP BY f.name, s.sale_date
    """, (date,))

    rows = cursor.fetchall()
    if not rows:
        print("No sales found for this date")
        return

    total_profit = 0

    print(f"\n{'FRUIT':<12} {'DATE':<12} {'PROFIT':>8}")
    print("-" * 34)

    for name, sale_date, profit in rows:
        total_profit += profit
        print(f"{name:<12} {sale_date:%Y-%m-%d} {profit:>8}")

    print("-" * 34)
    print(f"{'TOTAL PROFIT':<26}{total_profit:>8}")



# ---------------- CUSTOMER FUNCTIONS ----------------
def add_to_cart(cart):
    print("--------ITEMS MENU---------")
    cursor.execute("SELECT name, quantity, selling_price FROM fruits")

    print(f"{'ITEM':<12} {'QTY':>6} {'PRICE':>8}")
    print("-" * 28)

    for name, qty, price in cursor.fetchall():
        print(f"{name:<12} {qty:>6} {price:>8}")


    #adding to cart
    item = input("Fruit name: ").lower()
    qty = float(input("Qty: "))

    cursor.execute("SELECT id, quantity FROM fruits WHERE name=%s", (item,))
    data = cursor.fetchone()
    if not data:
        print("Fruit not found")
        return

    fid, stock = data
    if qty > stock:
        print("Not enough stock")
        return
    
    cart[item] = cart.get(item, 0) + qty  #update in cart if present
    db.commit()
    print("Added to cart")
    def update_owner_item():
        cursor.execute(
            "UPDATE fruits SET quantity = quantity - %s  WHERE id=%s",
            (qty, fid)
        )

def remove_from_cart(cart):
    item = input("Fruit to remove: ").lower()
    if item not in cart:
        print("Not in cart")
        return

    qty = cart[item] #takes the item value as it is dict
    cursor.execute(
        "UPDATE fruits SET quantity = quantity + %s WHERE name=%s",
        (qty, item)
    )
    del cart[item]
    db.commit()
    print("Removed from cart")

def update_cart(cart):
    item = input("Fruit to update: ").lower()
    if item not in cart:
        print("Not in cart")
        return

    new_qty = float(input("New qty: "))
    old_qty = cart[item]
    diff = new_qty - old_qty

    cursor.execute("SELECT id, quantity FROM fruits WHERE name=%s", (item,))
    data = cursor.fetchone()
    if not data:
        print("Fruit not found")
        return

    fid, stock = data
    if diff > stock:
        print("Not enough stock")
        return

    cursor.execute(
        "UPDATE fruits SET quantity = quantity - %s WHERE id=%s",
        (diff, fid)
    )

    if new_qty == 0:
        del cart[item]
    else:
        cart[item] = new_qty

    db.commit()
    print("Cart updated")

def view_cart(cart):
    if not cart:
        print("Cart empty")
        return

    total = 0
    print(f"{'ITEM':<12}{'QTY':<10}{'PRICE':<10}{'SUBTOTAL':<10}")
    print("-" * 42)

    for item, qty in cart.items():
        cursor.execute(
            "SELECT selling_price FROM fruits WHERE name=%s", (item,)
        )
        price = cursor.fetchone()[0]

        subtotal = price * qty
        total += subtotal

        print(f"{item:<12}{qty:<10}{price:<10}{subtotal:<10}")

    print("-" * 42)
    print(f"{'TOTAL':<34}{total}")


def bill(cart):
    if not cart:
        print("Cart empty")
        return

    name = input("Customer name: ")

    # ---- phone validation ----
    while True:
        phone = input("Phone (10 digits): ")
        if phone.isdigit() and len(phone) == 10:
            break
        print("Invalid phone number. Try again.")
    # --------------------------

    cursor.execute(
        "INSERT INTO customers (name, phone) VALUES (%s,%s)",
        (name, phone)
    )
    db.commit()
    cust_id = cursor.lastrowid

    total = 0

    print(f"\n{'ITEM':<12}{'QTY':<10}{'PRICE':<10}{'SUBTOTAL':<10}")
    print("-" * 42)

    for item, qty in cart.items():
        cursor.execute(
            "SELECT id, selling_price FROM fruits WHERE name=%s", (item,)
        )
        data = cursor.fetchone()
        if not data:
            continue

        fid, price = data
        subtotal = price * qty
        total += subtotal

        cursor.execute(
            "INSERT INTO sales (customer_id, fruit_id, qty, total) VALUES (%s,%s,%s,%s)",
            (cust_id, fid, qty, subtotal)
        )

        print(f"{item:<12}{qty:<10}{price:<10}{subtotal:<10}")

    print("-" * 42)
    print(f"{'TOTAL':<32}{total}")
    update_owner_item()
    db.commit()
    cart.clear()


# ---------------- MAIN LOOP ----------------
while True:
    print("\n1. OWNER\n2. CUSTOMER\n3. EXIT")

    try:
        role = int(input("Choice: "))
    except ValueError:
        print("Enter a valid number")
        continue

    if role == 1:
        if input("Password: ").capitalize() != "Ali":
            continue

        while True:
            print("\n1.Add 2.Remove 3.Update 4.View 5.Profit 6.Customer_details  7.Back")
            try:
                ch = int(input("Choice: "))
            except ValueError:
                print("Enter a valid number")
                continue

            if ch == 1: add_fruit()
            elif ch == 2: remove_fruit()
            elif ch == 3: update_fruit()
            elif ch == 4: view_inventory()
            elif ch == 5: profit_report()
            elif ch == 6: customer_report()
            elif ch == 7: break

    elif role == 2:
        cart = {}
        while True:
           

            print("\n1.Add 2.Remove 3.Update 4.View 5.Bill 6.Back")
            try:
                ch = int(input("Choice: "))
            except ValueError:
                print("Enter a valid number")
                continue

            if ch == 1: add_to_cart(cart)
            elif ch == 2: remove_from_cart(cart)
            elif ch == 3: update_cart(cart)
            elif ch == 4: view_cart(cart)
            elif ch == 5: bill(cart)
            elif ch == 6: break

    elif role == 3:
        print("Shop Closed")
        break





















