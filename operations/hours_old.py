from datetime import date

def hours_old_since_2025(year):
    # Obtener la fecha actual
    hoy = date.today()

    # Definir el 1 de enero del año actual
    primero_de_enero = date(year, 1, 1)

    # Calcular la diferencia de días
    diferencia_dias = hoy - primero_de_enero

    # Convertir la diferencia de días a horas
    horas_transcurridas = diferencia_dias.days * 24

    # Imprimir el resultado
    print(f"Han pasado {horas_transcurridas} horas desde el 1 de enero de este año.")
    return horas_transcurridas
