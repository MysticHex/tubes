import json
import sqlite3

# Connect to the database
conn = sqlite3.connect('tubes.db')
c = conn.cursor()

# Drop tables if they exist
c.execute('DROP TABLE IF EXISTS users')
c.execute('DROP TABLE IF EXISTS food_delivery')
c.execute('DROP TABLE IF EXISTS laundry')
c.execute('DROP TABLE IF EXISTS cleaning')

# Create tables
c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    role TEXT,
    password TEXT
)
''')

c.execute('''
CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
''')

c.execute('''
CREATE TABLE laundry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_customer INTEGER,
    nama TEXT,
    alamat TEXT,
    jenis TEXT,
    berat INTEGER,
    service TEXT
)
''')

c.execute('''
CREATE TABLE order_laundry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
''')


c.execute('''
CREATE TABLE menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    name TEXT,
    harga INTEGER,
    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
)
''')


# Insert data into users table
c.execute("INSERT INTO users (username, role, password) VALUES (?,?,?)", 
          ('user1', 'user', '12345'))

c.execute("INSERT INTO restaurants(name) VALUES ('Ayam Arjana')")
c.execute("INSERT INTO menus(restaurant_id,name,harga) VALUES (?,?,?)",(1,'Ayam Geprek',15000))
c.execute("INSERT INTO menus(restaurant_id,name,harga) VALUES (?,?,?)",(1,'Ayam Sambel Rica',18000))
# Commit changes and close the connection
conn.commit()
conn.close()