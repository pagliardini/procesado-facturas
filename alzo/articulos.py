import fitz
from func import convertir_a_flotante

# Abre el documento
documento = fitz.open("factura.pdf")
pagina = documento[0]  # Accedemos a la primera página

# Define las áreas de los rectángulos para los detalles de la factura
# Estos son ejemplos; debes ajustarlos según la posición exacta en tu PDF
cantidad_rectangulos = [fitz.Rect(10,149 + i * 20, 40, 400 + i * 20) for i in range(10)]
codigo_rectangulos = [fitz.Rect(40, 149 + i * 40, 82, 400 + i * 20) for i in range(10)]

# Extrae y convierte los valores del texto a flotantes
subtotal_rectangulo = fitz.Rect(21, 448, 69, 465)
imp_internos_rectangulo = fitz.Rect(133, 448, 179, 465)
iva_rectangulo = fitz.Rect(248, 448, 288, 465)
total_rectangulo = fitz.Rect(367, 448, 415, 465)
factura_rectangulo = fitz.Rect(330, 15, 415, 25)
fecha_rectangulo = fitz.Rect(335, 29, 415, 39)

#dibujar estos rectangulos
pagina.draw_rect(subtotal_rectangulo, color=(0, 1, 0))  # Verde
pagina.draw_rect(imp_internos_rectangulo, color=(1, 0, 0))  # Rojo
pagina.draw_rect(iva_rectangulo, color=(0, 0, 1))  # Azul
pagina.draw_rect(total_rectangulo, color=(1, 1, 0))  # Amarillo
pagina.draw_rect(factura_rectangulo, color=(1, 0, 1))  # Magenta
pagina.draw_rect(fecha_rectangulo, color=(1, 0, 1))
pagina.draw_rect(cantidad_rectangulos[0], color=(0, 1, 0))  # Verde
pagina.draw_rect(codigo_rectangulos[0], color=(0, 1, 0))  # Verde

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

# Extraer cantidades y códigos de artículos
cantidades = [pagina.get_text("text", clip=rect).strip() for rect in cantidad_rectangulos]
codigos = [pagina.get_text("text", clip=rect).strip() for rect in codigo_rectangulos]

# Crear un diccionario para relacionar cantidades con códigos de artículos
detalles_factura = {}
for cantidad, codigo in zip(cantidades, codigos):
    if cantidad and codigo:
        detalles_factura[codigo] = cantidad

# Imprimir el resultado
print("Factura:", factura.strip())
print("Fecha:", fecha.strip())
print("Subtotal:", subtotal)
print("Imp. Internos:", imp_internos)
print("IVA:", iva)
print("Total:", total)

# Imprimir los detalles de la factura
print("Detalles de la factura:", cantidades, codigos)


# Guardar el documento modificado
documento.save("documento_con_rectangulo.pdf")

# Cerrar el documento
documento.close()
