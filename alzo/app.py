import fitz
from func import convertir_a_flotante

# abre el documento
documento = fitz.open("factura.pdf")


pagina = documento[0]  # accedemos a la primera página

# Rectángulo 1 - Subtotal
subtotal_rectangulo = fitz.Rect(21, 448, 69, 465)
pagina.draw_rect(subtotal_rectangulo, color=(0, 1, 0))  # Verde

# Rectángulo 2 - Imp. Internos
imp_internos_rectangulo = fitz.Rect(133, 448, 179, 465)
pagina.draw_rect(imp_internos_rectangulo, color=(1, 0, 0))  # Rojo

# Rectángulo 3 - IVA
iva_rectangulo = fitz.Rect(248, 448, 288, 465)
pagina.draw_rect(iva_rectangulo, color=(0, 0, 1))  # Azul

# Rectángulo 4 - Total
total_rectangulo = fitz.Rect(367, 448, 415, 465)
pagina.draw_rect(total_rectangulo, color=(1, 1, 0))  # Amarillo

# Rectángulo 5 - Factura
factura_rectangulo = fitz.Rect(330, 15, 415, 25)
pagina.draw_rect(factura_rectangulo, color=(1, 0, 1))  # Magenta

# Rectángulo 6 - Fecha
fecha_rectangulo = fitz.Rect(335, 29, 415, 39)
pagina.draw_rect(fecha_rectangulo, color=(1, 0, 1))  # Magenta

# Extraemos el texto dentro del rectángulo
subtotal_texto = pagina.get_text("text", clip=subtotal_rectangulo)
imp_internos_texto = pagina.get_text("text", clip=imp_internos_rectangulo)
iva_texto = pagina.get_text("text", clip=iva_rectangulo)
total_texto = pagina.get_text("text", clip=total_rectangulo)
factura = pagina.get_text("text", clip=factura_rectangulo)
fecha = pagina.get_text("text", clip=fecha_rectangulo)

# Convertir los valores de texto a flotantes
subtotal = convertir_a_flotante(subtotal_texto)
imp_internos = convertir_a_flotante(imp_internos_texto)
iva = convertir_a_flotante(iva_texto)
total = convertir_a_flotante(total_texto)


# Imprimimos el resultado
print("Factura:", factura)
print("Fecha:", fecha)
print("Subtotal:", subtotal)
print("Imp. Internos:", imp_internos)
print("IVA:", iva)
print("Total:", total)


# Guardamos el documento modificado
documento.save("documento_con_rectangulo.pdf")

# Cerramos el documento
documento.close()
