from db import conectar_bd, obtener_producto
from pdf_processing import extraer_datos_pdf
from output import escribir_detalles_factura
from func import convertir_a_flotante



def main():
    conn = conectar_bd()
    cursor = conn.cursor()

    datos = extraer_datos_pdf("factura.pdf")

    subtotal = convertir_a_flotante(datos["subtotal_texto"])
    imp_internos = convertir_a_flotante(datos["imp_internos_texto"])
    iva = convertir_a_flotante(datos["iva_texto"])
    total = convertir_a_flotante(datos["total_texto"])
    print("Cuit:", datos["cuit"].strip())
    print("Factura:", datos["factura"].strip())
    print("Fecha:", datos["fecha"].strip())
    print("")
    print("Detalles de la factura:")

    # Crear el archivo de salida
    with open("detalles_factura.txt", "w") as archivo_salida:
        escribir_detalles_factura(datos["productos"], cursor, archivo_salida)

    print("")
    print("Subtotal:", subtotal)
    print("Imp. Internos:", imp_internos)
    print("IVA:", iva)
    print("")
    print("Total:", total)

    datos["documento"].save("factura_con_rectangulo.pdf")
    datos["documento"].close()
    conn.close()

if __name__ == "__main__":
    main()
