import json
import pymssql

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

def conectar_bd():
    config = cargar_configuracion()
    return pymssql.connect(server=config['server'], user=config['user'], password=config['password'], database=config['database'])

def obtener_producto(cursor, codigo):
    query = """
    SELECT p.Descripcion, p.Precio_Venta, p.Precio_Costo, p.Id_Producto, p.Precio_Venta1, p.Precio_Venta2, p.Precio_Venta3,
           p.Id_Producto1, p.Id_Producto2, p.Id_Producto3, r.Descripcion AS Rubro, m.Nombre AS Marca
    FROM Productos p
    JOIN Relaciones_Codigos_CodInt rci ON p.Id = rci.Id_Producto
    LEFT JOIN Rubros r ON p.Id_Rubro = r.Id_Rubro
    LEFT JOIN Marcas m ON p.Id_Marca = m.Id_Marca
    WHERE rci.Codigo_Interno = %s
    """
    cursor.execute(query, (codigo,))
    return cursor.fetchone()

def obtener_proveedor(cursor, numero_documento):
    query = """
    SELECT Nombre
    FROM Proveedores
    WHERE Numero_Documento = %s
    """
    cursor.execute(query, (numero_documento,))
    nombre_proveedor = cursor.fetchone()
    return nombre_proveedor[0] if nombre_proveedor else None

