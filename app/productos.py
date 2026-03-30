import sqlite3

# 📌 Conexión a la base de datos
def conectar():
    conn = sqlite3.connect("database/data.db")
    return conn


# 📌 Crear tabla productos
def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        referencia TEXT UNIQUE NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# 📌 Agregar producto
def agregar_producto(nombre, referencia, precio, stock):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO productos (nombre, referencia, precio, stock)
        VALUES (?, ?, ?, ?)
        """, (nombre, referencia, precio, stock))

        conn.commit()
        print("✅ Producto agregado correctamente")

    except sqlite3.IntegrityError:
        print("❌ Error: la referencia ya existe (debe ser única)")

    finally:
        conn.close()  # 🔥 ESTO SOLUCIONA EL BLOQUEO


# 📌 Listar productos
def listar_productos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conn.close()

    return productos

# 📌 Buscar producto por referencia
def buscar_producto(referencia):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE referencia = ?", (referencia,))
    producto = cursor.fetchone()

    conn.close()

    if producto:
        print("\n🔍 PRODUCTO ENCONTRADO")
        print(producto)
    else:
        print("❌ Producto no encontrado")


# 📌 Ejecutar prueba rápida
if __name__ == "__main__":
    crear_tabla()

    # Pruebas
    agregar_producto("Martillo", "MART-001", 15000, 10)
    agregar_producto("Clavos", "CLAV-001", 5000, 50)

    listar_productos()

    buscar_producto("MART-001")

def actualizar_producto(referencia_original, nombre, referencia, precio, stock):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE productos
    SET nombre = ?, referencia = ?, precio = ?, stock = ?
    WHERE referencia = ?
    """, (nombre, referencia, precio, stock, referencia_original))

    conn.commit()
    conn.close()