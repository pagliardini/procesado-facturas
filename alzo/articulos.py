import fitz
from func import convertir_a_flotante

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

# Crear un diccionario para los productos
productos = {}

# Iterar sobre las líneas y rellenar el diccionario
for i in range(0, len(cantidades_lineas), 2):
    codigo = cantidades_lineas[i].strip()
    cantidad = cantidades_lineas[i + 1].strip() if i + 1 < len(cantidades_lineas) else "0"
    productos[codigo] = int(cantidad)

print("Factura:", factura.strip())
print("Fecha:", fecha.strip())
print("")
print("Detalles de la factura:")
for codigo, cantidad in productos.items():
    print(f"Código: {codigo}, Cantidad: {cantidad}")
print("")
print("Subtotal:", subtotal)
print("Imp. Internos:", imp_internos)
print("IVA:", iva)
print("")
print("Total:", total)

documento.save("documento_con_rectangulo.pdf")

documento.close()
