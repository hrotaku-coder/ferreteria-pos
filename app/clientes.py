import sqlite3
from db import conectar  # Importamos la conexión desde tu archivo central

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
        return True  # Le avisa a la interfaz que se guardó correctamente

    except sqlite3.IntegrityError:
        return False # Le avisa a la interfaz que el documento ya existe

    finally:
        conn.close()


# 📌 Buscar cliente por documento
def buscar_cliente(documento):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes WHERE documento = ?", (documento,))
    cliente = cursor.fetchone()
    conn.close()

    return cliente  # Retorna los datos o "None" si no existe


# 📌 Listar clientes
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()

    return clientes