import sqlite3
from db import conectar

# 📌 Agregar producto
def agregar_producto(nombre, referencia, precio1, precio2, stock):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO productos (nombre, referencia, precio1, precio2, stock)
        VALUES (?, ?, ?, ?, ?)
        """, (nombre, referencia, precio1, precio2 , stock))

        conn.commit()
        return True  # Éxito: Le avisa a la ventana que se guardó correctamente

    except sqlite3.IntegrityError:
        return False # Error: La referencia ya existe

    finally:
        conn.close()


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
    
    return producto # Retorna la tupla con los datos, o None si no existe


# 📌 Actualizar producto
def actualizar_producto(referencia_original, nombre, referencia, precio1, precio2, stock):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        UPDATE productos
        SET nombre = ?, referencia = ?, precio1 = ?, precio2 = ?, stock = ?
        WHERE referencia = ?
        """, (nombre, referencia, precio1, precio2, stock, referencia_original))

        conn.commit()
        return True # Éxito al actualizar
        
    except sqlite3.IntegrityError:
        return False # Error: Intenta poner una referencia que ya existe
        
    finally:
        conn.close()