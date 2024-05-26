# Procesado de Facturas

Este proyecto es una aplicación para el procesamiento y análisis de facturas en formato PDF. La aplicación extrae información relevante de las facturas, consulta datos en una base de datos y genera un informe detallado. 

## Funcionalidades

- **Extracción de datos desde PDF:** La aplicación puede extraer información como número de factura, fecha, CUIT del proveedor, subtotal, impuestos, IVA, total, y las cantidades de productos.
- **Consulta de base de datos:** Utiliza una base de datos para obtener detalles de productos y proveedores.
- **Generación de informes:** Genera informes detallados con la información extraída y los datos consultados en la base de datos.

## Estructura del Proyecto

- `main.py`: Archivo principal que ejecuta el proceso de extracción, consulta y generación de informes.
- `pdf_processing.py`: Contiene la lógica para extraer datos de los archivos PDF.
- `db.py`: Funciones para interactuar con la base de datos, incluyendo la obtención de detalles de productos y proveedores.
- `output.py`: Funciones para escribir los detalles de la factura en un archivo de salida.
- `buscar_proveedor.py`: Script auxiliar para verificar la coincidencia del CUIT extraído del PDF con el almacenado en la base de datos.

