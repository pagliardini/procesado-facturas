import fitz
import pymssql
from func import convertir_a_flotante

# Conectar a la base de datos SQL Server
conn = pymssql.connect(server='...', user='', password='', database='')
cursor = conn.cursor()

documento = fitz.open("factura.pdf")
pagina = documento[0]  # Accedemos a la primera página

cantidad_rectangulos = fitz.Rect(10, 149, 80, 400)

subtotal_rectangulo = fitz.Rect(21, 448, 69, 465)
imp_internos_rectangulo = fitz.Rect(133, 448, 179, 465)
iva_rectangulo = fitz.Rect(248, 448, 288, 465)
total_rectangulo = fitz.Rect(367, 448, 415, 465)
factura_rectangulo = fitz.Rect(330, 15, 415, 25)
fecha_rectangulo = fitz.Rect(335, 29, 415, 39)

pagina.draw_rect(subtotal_rectangulo, color=(0, 1, 0))  # Verde
pagina.draw_rect(imp_internos_rectangulo, color=(1, 0, 0))  # Rojo
pagina.draw_rect(iva_rectangulo, color=(0, 0, 1))  # Azul
pagina.draw_rect(total_rectangulo, color=(1, 1, 0))  # Amarillo
pagina.draw_rect(factura_rectangulo, color=(1, 0, 1))  # Magenta
pagina.draw_rect(fecha_rectangulo, color=(1, 0, 1))
pagina.draw_rect(cantidad_rectangulos, color=(0, 1, 0))  # Verde

subtotal_texto = pagina.get_text("text", clip=subtotal_rectangulo)
imp_internos_texto = pagina.get_text("text", clip=imp_internos_rectangulo)
iva_texto = pagina.get_text("text", clip=iva_rectangulo)
total_texto = pagina.get_text("text", clip=total_rectangulo)
factura = pagina.get_text("text", clip=factura_rectangulo)
fecha = pagina.get_text("text", clip=fecha_rectangulo)

subtotal = convertir_a_flotante(subtotal_texto)
imp_internos = convertir_a_flotante(imp_internos_texto)
iva = convertir_a_flotante(iva_texto)
total = convertir_a_flotante(total_texto)

cantidades_texto = pagina.get_text("text", clip=cantidad_rectangulos)
cantidades_lineas = cantidades_texto.splitlines()

productos = {}

for i in range(0, len(cantidades_lineas), 2):
    codigo = cantidades_lineas[i].strip()
    cantidad = cantidades_lineas[i + 1].strip() if i + 1 < len(cantidades_lineas) else "0"
    productos[codigo] = int(cantidad)

print("Factura:", factura.strip())
print("Fecha:", fecha.strip())
print("")
print("Detalles de la factura:")

# Crear el archivo de salida
with open("detalles_factura.txt", "w") as archivo_salida:
    for codigo, cantidad in productos.items():
        try:
            cursor.execute("""
            SELECT p.Descripcion, p.Precio_Venta, p.Precio_Costo, p.Id_Producto, p.Precio_Venta1, p.Precio_Venta2, p.Precio_Venta3,
                   p.Id_Producto1, p.Id_Producto2, p.Id_Producto3, r.Descripcion AS Rubro, m.Nombre AS Marca
            FROM Productos p
            JOIN Relaciones_Codigos_CodInt rci ON p.Id = rci.Id_Producto
            LEFT JOIN Rubros r ON p.Id_Rubro = r.Id_Rubro
            LEFT JOIN Marcas m ON p.Id_Marca = m.Id_Marca
            WHERE rci.Codigo_Interno = %s
            """, (codigo,))
            resultado = cursor.fetchone()

            if resultado:
                (descripcion, precio_venta, precio_costo, id_producto, precio_venta1, precio_venta2, precio_venta3,
                 id_producto1, id_producto2, id_producto3, rubro, marca) = resultado
                cantidad_formateada = f"{cantidad:,.0f}".replace(",", ".")
                precio_costo_formateado = f"{precio_costo:,.6f}".replace(",", "").replace(".", ",")
                precio_venta_formateado = f"{precio_venta:,.5f}".replace(",", "").replace(".", ",")
                precio_venta1_formateado = f"{precio_venta1:,.5f}".replace(",", "").replace(".", ",")
                precio_venta2_formateado = f"{precio_venta2:,.5f}".replace(",", "").replace(".", ",")
                precio_venta3_formateado = f"{precio_venta3:,.5f}".replace(",", "").replace(".", ",")

                archivo_salida.write(
                    f"{rubro};{marca};{cantidad_formateada};{precio_costo_formateado};{precio_venta_formateado};"
                    f"{descripcion};{id_producto};{precio_venta1_formateado};{precio_venta2_formateado};{precio_venta3_formateado};"
                    f"{id_producto1};{id_producto2};{id_producto3}\n")
                print(
                    f"Código: {codigo}, Cantidad: {cantidad}, Descripción: {descripcion}, Precio Venta: {precio_venta}, "
                    f"Rubro: {rubro}, Marca: {marca}, Precio Costo: {precio_costo}, Id_Producto: {id_producto}, "
                    f"Precio_Venta1: {precio_venta1}, Precio_Venta2: {precio_venta2}, Precio_Venta3: {precio_venta3}, "
                    f"Id_Producto1: {id_producto1}, Id_Producto2: {id_producto2}, Id_Producto3: {id_producto3}")
            else:
                archivo_salida.write(f"Producto no cargado/sin relacion interna para el código: {codigo}\n")
                print(f"Código: {codigo}, Cantidad: {cantidad}, Producto no cargado/sin relación interna")
        except Exception as e:
            archivo_salida.write(f"Error al buscar el código {codigo}: {e}\n")
            print(f"Error al buscar el código {codigo}: {e}")

print("")
print("Subtotal:", subtotal)
print("Imp. Internos:", imp_internos)
print("IVA:", iva)
print("")
print("Total:", total)

documento.save("documento_con_rectangulo.pdf")
documento.close()
conn.close()
