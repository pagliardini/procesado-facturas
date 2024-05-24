import fitz

def extraer_datos_pdf(nombre_archivo):
    documento = fitz.open(nombre_archivo)
    pagina = documento[0]  # Accedemos a la primera página

    cantidad_rectangulos = fitz.Rect(10, 149, 80, 400)
    subtotal_rectangulo = fitz.Rect(21, 448, 69, 465)
    imp_internos_rectangulo = fitz.Rect(133, 448, 179, 465)
    iva_rectangulo = fitz.Rect(248, 448, 288, 465)
    total_rectangulo = fitz.Rect(367, 448, 415, 465)
    factura_rectangulo = fitz.Rect(330, 15, 415, 25)
    fecha_rectangulo = fitz.Rect(335, 29, 415, 39)

    # Obtener textos
    subtotal_texto = pagina.get_text("text", clip=subtotal_rectangulo)
    imp_internos_texto = pagina.get_text("text", clip=imp_internos_rectangulo)
    iva_texto = pagina.get_text("text", clip=iva_rectangulo)
    total_texto = pagina.get_text("text", clip=total_rectangulo)
    factura = pagina.get_text("text", clip=factura_rectangulo)
    fecha = pagina.get_text("text", clip=fecha_rectangulo)

    # Obtener cantidades de productos
    cantidades_texto = pagina.get_text("text", clip=cantidad_rectangulos)
    cantidades_lineas = cantidades_texto.splitlines()

    productos = {}
    for i in range(0, len(cantidades_lineas), 2):
        codigo = cantidades_lineas[i].strip()
        cantidad = cantidades_lineas[i + 1].strip() if i + 1 < len(cantidades_lineas) else "0"
        productos[codigo] = int(cantidad)

    return {
        "subtotal_texto": subtotal_texto,
        "imp_internos_texto": imp_internos_texto,
        "iva_texto": iva_texto,
        "total_texto": total_texto,
        "factura": factura,
        "fecha": fecha,
        "productos": productos,
        "documento": documento
    }
