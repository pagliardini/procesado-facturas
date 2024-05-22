def convertir_a_flotante(valor_texto):
    valor_texto = valor_texto.replace('.', '').replace(',', '.')
    return float(valor_texto)
