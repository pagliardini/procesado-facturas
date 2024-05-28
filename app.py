from flask import Flask, render_template, request, send_file
from db import conectar_bd, obtener_producto
from pdf_processing import extraer_datos_pdf
from output import escribir_detalles_factura
from func import convertir_a_flotante
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar_factura', methods=['POST'])
def procesar_factura():
    conn = conectar_bd()
    cursor = conn.cursor()

    datos = extraer_datos_pdf("factura.pdf")

    subtotal = convertir_a_flotante(datos["subtotal_texto"])
    imp_internos = convertir_a_flotante(datos["imp_internos_texto"])
    iva = convertir_a_flotante(datos["iva_texto"])
    total = convertir_a_flotante(datos["total_texto"])

    detalles = {
        "cuit": datos["cuit"].strip(),
        "factura": datos["factura"].strip(),
        "fecha": datos["fecha"].strip(),
        "productos": datos["productos"],
        "subtotal": subtotal,
        "imp_internos": imp_internos,
        "iva": iva,
        "total": total
    }

    # salida txt
    nombre_archivo = datos["factura"].strip() + ".txt"
    with open(nombre_archivo, "w") as archivo_salida:
        escribir_detalles_factura(datos["productos"], cursor, archivo_salida)

    datos["documento"].save("factura_con_rectangulo.pdf")
    datos["documento"].close()
    conn.close()

    return render_template('factura.html', detalles=detalles, archivo_txt=nombre_archivo)

@app.route('/descargar/<nombre_archivo>')
def descargar_archivo(nombre_archivo):
    return send_file(nombre_archivo, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
