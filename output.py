from db import obtener_producto


def escribir_detalles_factura(productos, cursor, archivo_salida):
    for codigo, cantidad in productos.items():
        try:
            resultado = obtener_producto(cursor, codigo)
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
                    f"Código: {codigo}, Cantidad: {cantidad}, Descripción: {descripcion}")
            else:
                archivo_salida.write(f"Producto no cargado/sin relacion interna para el código: {codigo}\n")
                print(f"Código: {codigo}, Cantidad: {cantidad}, Producto no cargado/sin relación interna")
        except Exception as e:
            archivo_salida.write(f"Error al buscar el código {codigo}: {e}\n")
            print(f"Error al buscar el código {codigo}: {e}")
