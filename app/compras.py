import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("database/data.db")

def registrar_compra(proveedor_id, numero_factura_proveedor, total, productos_comprados):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO compras (fecha, total, proveedor_id, numero_factura_proveedor)
            VALUES (?, ?, ?, ?)
        """, (fecha_actual, total, proveedor_id, numero_factura_proveedor))
        
        id_compra = cursor.lastrowid
        
        for p in productos_comprados:
            referencia, cantidad, precio_costo, subtotal = p
            
            cursor.execute("""
                INSERT INTO detalle_compra (id_compra, referencia, cantidad, precio_costo, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (id_compra, referencia, cantidad, precio_costo, subtotal))
            
            cursor.execute("""
                UPDATE productos
                SET stock = stock + ?
                WHERE referencia = ?
            """, (cantidad, referencia))
            
        conn.commit()
        return True
    
    except Exception as e:
        print(f"Error al registrar compra: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()