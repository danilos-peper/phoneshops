import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("""
     CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity REAL NOT NULL,
        order_date DATE NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
""")
conn.commit()


# cursor.execute("""
#     INSERT INTO products (name, category, price) VALUES
#         ('iPhone 14', 'смартфони', 1000.00),
#         ('Samsung Galaxy S23', 'смартфони', 900.00),
#         ('Dell XPS 13', 'ноутбуки', 1200.00),
#         ('MacBook Air', 'ноутбуки', 1100.00),
#         ('iPad Pro', 'планшети', 800.00),
#         ('Samsung Tab S8', 'планшети', 700.00),
#         ('Sony WH-1000XM5', 'навушники', 350.00);
# """)


# conn.commit()

# cursor.execute("""
#     INSERT INTO customers (first_name, last_name, email) VALUES
#     ('Іван', 'Петренко', 'ivan.petrenko@example.com'),
#     ('Марія', 'Сидоренко', 'maria.sydorenko@example.com'),
#     ('Олексій', 'Коваленко', 'oleksiy.kovalenko@example.com'),
#     ('Анна', 'Іваненко', 'anna.ivanenko@example.com');
# """)


# conn.commit()

# cursor.execute("""
#     INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
#     (1, 1, 2, '2026-01-01'),
#     (2, 3, 1, '2026-01-02'),
#     (1, 5, 3, '2026-01-03'),
#     (3, 2, 1, '2026-01-04'),
#     (4, 7, 4, '2026-01-05'),
#     (2, 4, 1, '2026-01-06'),
#     (3, 6, 2, '2026-01-07');
# """)

# conn.commit()


def total_price():
    cursor.execute("""
        SELECT SUM(orders.quantity * products.price)
        FROM orders
        INNER JOIN products ON orders.product_id = products.product_id
    """)
    result = cursor.fetchone()[0]
    print(f"Загальний обсяг продажів - {result}")


def total_orders_per_customer():
    cursor.execute("""
        SELECT customers.first_name, customers.last_name, COUNT(orders.order_id)
        FROM customers
        INNER JOIN orders ON customers.customer_id = orders.customer_id
        GROUP BY customers.customer_id
    """)
    
    for first_name, last_name, count in cursor.fetchall():
        print(f"{first_name} {last_name}: {count} замовлень")

def average_price():
    cursor.execute("""
        SELECT AVG(orders.quantity * products.price)
        FROM orders
        INNER JOIN products ON orders.product_id = products.product_id
    """)
    result = cursor.fetchone()[0]

    if result is None:
        print("Замовлень поки немає. Середній чек = 0")
    else:
        print(f"Середній чек замовлення - {round(result, 2)}")


def popular_category():
    cursor.execute("""
        SELECT products.category, COUNT(orders.quantity * products.price)
        FROM orders
        INNER JOIN products ON orders.product_id = orders.product_id
        GROUP BY products.category
        ORDER BY SUM(orders.quantity) DESC
        LIMIT 1
        
""")
    result = cursor.fetchall()
    print(f"Найбільш популярна категорія - {result}")

while 1:
    print("""\n------------------------------------------------------------
1. Загальний обсяг продажів (сума) за ісі замовлення.
2. Кількість замовлень для кожного клієнта
3. Середній чек замовлення
4. Найбільш популярна категорія товарів
6. Завершити роботу.
------------------------------------------------------------\n""")
    try:
        choice = int(input("Ваш вибір:"))
        if choice == 6:
            break
        elif choice == 1:
            total_price()
        elif choice == 2:
            total_orders_per_customer()
        elif choice == 3:
            average_price()
        elif choice == 4:
            popular_category()
    except ValueError:
        print("Введіть число!")

conn.close()