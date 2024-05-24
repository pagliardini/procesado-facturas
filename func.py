def convertir_a_flotante(texto):
    texto = texto.replace("$", "").replace(",", "").replace(".", "").replace(" ", "")
    try:
        return float(texto) / 100
    except ValueError:
        return 0.0
