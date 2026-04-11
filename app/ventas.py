import sqlite3
from datetime import datetime
from db import conectar, obtener_siguiente_factura

# 📌 Buscar cliente
def obtener_cliente(documento):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM clientes WHERE documento = ?", (documento,))
    cliente = cursor.fetchone()

    conn.close()
    return cliente


# 📌 Obtener producto
def obtener_producto(referencia): #
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre, precio1, precio2, stock FROM productos WHERE referencia = ?", (referencia,))
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
            return False # Le avisa a la UI que el cliente no existe

        cliente_id, nombre_cliente = cliente

        # Validar stock y calcular total ANTES de registrar la venta
        for referencia, cantidad, precio, tipo in productos_vendidos:
            producto = obtener_producto(referencia)

            if producto is None:
                continue

            nombre, precio1, precio2, stock = producto

            if stock < cantidad:
                return False # Le avisa a la UI que no hay stock suficiente

            precio = precio1  # usamos precio1 como base temporal
            subtotal = precio * cantidad
            total += subtotal
            
        if total == 0:
            return False # No hay productos válidos para vender
        
        # Generar el número de factura
        numero_factura = obtener_siguiente_factura()

        # Guardar encabezado de la venta
        cursor.execute("""
        INSERT INTO ventas (numero_factura, fecha, total, cliente_id)
        VALUES (?, ?, ?, ?)
        """, (numero_factura, fecha, total, cliente_id))

        id_venta = cursor.lastrowid

        # Guardar el detalle de los productos y restar stock
        for referencia, cantidad, precio, tipo in productos_vendidos:
            producto = obtener_producto(referencia)

            if producto is None:
                continue

            nombre, _, _, stock = producto

            if stock < cantidad:
                return False

            subtotal = precio * cantidad
            total += subtotal
            
            if stock < cantidad:
                continue

            subtotal = precio * cantidad

            # Guardar detalle
            cursor.execute("""
            INSERT INTO detalle_venta (id_venta, referencia, cantidad, precio_unitario, tipo_precio, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (id_venta, referencia, cantidad, precio, tipo, subtotal))

            # Actualizar stock
            actualizar_stock(cursor, referencia, cantidad)

        conn.commit()
        
        # Si todo salió perfecto, retorna el número de factura para que la UI imprima el PDF
        return numero_factura 

    except Exception as e:
        conn.rollback() # Si algo falla en el proceso, cancela todo para no dañar la base de datos
        return False

    finally:
        conn.close()


# 📌 Ver ventas con cliente
def ver_ventas(): # Esta función es para mostrar un listado de ventas en la UI, con el nombre del cliente en lugar de su ID
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT v.id, v.fecha, v.total, c.nombre
    FROM ventas v
    JOIN clientes c ON v.cliente_id = c.id
    """)

    ventas = cursor.fetchall()

    conn.close()
    return ventas