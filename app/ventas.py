import sqlite3
from datetime import datetime


# 📌 Conexión
def conectar():
    return sqlite3.connect("database/data.db")


# 📌 Crear tablas
def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        total REAL,
        cliente_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER,
        referencia TEXT,
        cantidad INTEGER,
        precio REAL,
        subtotal REAL
    )
    """)

    conn.commit()
    conn.close()


# 📌 Buscar cliente
def obtener_cliente(documento):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM clientes WHERE documento = ?", (documento,))
    cliente = cursor.fetchone()

    conn.close()
    return cliente


# 📌 Obtener producto
def obtener_producto(referencia):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre, precio, stock FROM productos WHERE referencia = ?", (referencia,))
    producto = cursor.fetchone()

    conn.close()
    return producto


# 📌 Actualizar stock
def actualizar_stock(cursor, referencia, cantidad):
    cursor.execute("""
    UPDATE productos
    SET stock = stock - ?
    WHERE referencia = ?
    """, (cantidad, referencia))


# 📌 Crear venta con cliente
def crear_venta(documento_cliente, productos_vendidos):
    conn = conectar()
    cursor = conn.cursor()

    total = 0
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # 🔍 Buscar cliente
        cliente = obtener_cliente(documento_cliente)

        if cliente is None:
            print("❌ Cliente no existe")
            return

        cliente_id, nombre_cliente = cliente

        # Crear venta
        cursor.execute("""
        INSERT INTO ventas (fecha, total, cliente_id)
        VALUES (?, ?, ?)
        """, (fecha, 0, cliente_id))

        id_venta = cursor.lastrowid

        for referencia, cantidad in productos_vendidos:

            producto = obtener_producto(referencia)

            if producto is None:
                print(f"❌ Producto no existe: {referencia}")
                continue

            nombre, precio, stock = producto

            if stock < cantidad:
                print(f"❌ Stock insuficiente para {nombre}")
                continue

            subtotal = precio * cantidad
            total += subtotal

            # Guardar detalle
            cursor.execute("""
            INSERT INTO detalle_venta (id_venta, referencia, cantidad, precio, subtotal)
            VALUES (?, ?, ?, ?, ?)
            """, (id_venta, referencia, cantidad, precio, subtotal))

            # Actualizar stock
            actualizar_stock(cursor, referencia, cantidad)

        # Actualizar total
        cursor.execute("UPDATE ventas SET total = ? WHERE id = ?", (total, id_venta))

        conn.commit()

        print(f"✅ Venta realizada a {nombre_cliente}. Total: {total}")

    except Exception as e:
        conn.rollback()
        print("❌ Error en la venta:", e)

    finally:
        conn.close()


# 📌 Ver ventas con cliente
def ver_ventas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT v.id, v.fecha, v.total, c.nombre
    FROM ventas v
    JOIN clientes c ON v.cliente_id = c.id
    """)

    ventas = cursor.fetchall()

    print("\n🧾 VENTAS CON CLIENTE:")
    for v in ventas:
        print(v)

    conn.close()


# 🚀 PRUEBA
if __name__ == "__main__":
    crear_tablas()

    productos = [
        ("MART-001", 2),
        ("CLAV-001", 5)
    ]

    # 👇 IMPORTANTE: usar documento del cliente
    crear_venta("123456", productos)

    ver_ventas()