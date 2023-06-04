import mysql.connector

class create_database():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = ""
    )
    cursor = conn.cursor()
    #crea base de datos si no existe
    cursor.execute ("CREATE DATABASE IF NOT EXISTS zelda")
    print("Database 'zelda' created successfully")
    cursor.execute("USE zelda ")
    #crea tablas por si no existe el inventario
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description VARCHAR(255))")
    print("Table 'inventory' create successfully")
    ##Crear tabla de datos de los items
    cursor.execute("CREATE TABLE IF NOT EXISTS item_details (id INT AUTO_INCREMENT PRIMARY KEY, item_id INT, attack INT, rango INT, FOREIGN KEY (item_id) REFERENCES inventory(id))")
    print("Table 'item_details' created successfully")

class Item:
    def __init__(self, name, description, attack, rango):
        self.name = name
        self.description = description
        self.attack = attack
        self.rango = rango

class Inventory:
    
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="zelda"
        )
        self.cursor = self.conn.cursor()

    def add_item(self, item):
        sql_insert_inventory = "INSERT INTO inventory (name, description) VALUES (%s, %s)"
        values_inventory = (item.name, item.description)
        self.cursor.execute(sql_insert_inventory, values_inventory)
        self.conn.commit()

        item_id = self.cursor.lastrowid
        sql_insert_item_details = "INSERT INTO item_details (item_id, attack, rango) VALUES (%s, %s, %s)"
        values_item_details = (item_id, item.attack, item.rango)
        self.cursor.execute(sql_insert_item_details, values_item_details)
        self.conn.commit()

    def show_inventory(self):
        sql = "SELECT i.name, i.description, d.attack, d.rango FROM inventory i INNER JOIN item_details d ON i.id = d.item_id"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if result:
            print("Inventory:")
            for row in result:
                name, description, attack, rango = row
                print("Name:", name)
                print("Description:", description)
                print("Attack:", attack)
                print("Rango:", rango)
                print()
        else:
            print("Inventory is empty.")


    def close(self):
        self.cursor.close()
        self.conn.close()
#funcion creacion de base de datos si no existe


inventory= Inventory()
# Conexion hecha?
print(inventory.conn.is_connected())

# Añadir un nuevo elemento al inventario con sus detalles
item1 = Item("emanems", "mentirosas camilas todas",1000000, 5000)
inventory.add_item(item1)

# Cerrar la conexión con la base de datos
inventory.close()