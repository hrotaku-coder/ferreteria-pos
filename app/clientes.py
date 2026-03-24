import sqlite3

# 📌 Conexión
def conectar():
    return sqlite3.connect("database/data.db")


# 📌 Crear tabla clientes
def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        documento TEXT UNIQUE NOT NULL,
        telefono TEXT
    )
    """)

    conn.commit()
    conn.close()


# 📌 Agregar cliente
def agregar_cliente(nombre, documento, telefono):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO clientes (nombre, documento, telefono)
        VALUES (?, ?, ?)
        """, (nombre, documento, telefono))

        conn.commit()
        print("✅ Cliente agregado correctamente")

    except sqlite3.IntegrityError:
        print("❌ Error: ya existe un cliente con ese documento")

    finally:
        conn.close()


# 📌 Buscar cliente por documento
def buscar_cliente(documento):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM clientes WHERE documento = ?
    """, (documento,))

    cliente = cursor.fetchone()
    conn.close()

    if cliente:
        print("\n🔍 CLIENTE ENCONTRADO:")
        print(cliente)
        return cliente
    else:
        print("❌ Cliente no encontrado")
        return None


# 📌 Listar clientes (🔥 CORREGIDO)
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    conn.close()

    return clientes  # 🔥 ESTO ES LO IMPORTANTE


# 🚀 PRUEBA
if __name__ == "__main__":
    crear_tabla()

    # Pruebas
    agregar_cliente("Juan Perez", "123456", "3001234567")
    agregar_cliente("Empresa XYZ", "900123456", "3109876543")

    lista = listar_clientes()

    print("\n👤 LISTA DE CLIENTES")
    print("-" * 40)

    for c in lista:
        print(f"ID: {c[0]} | Nombre: {c[1]} | Doc: {c[2]} | Tel: {c[3]}")

    buscar_cliente("123456")