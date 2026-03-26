import os


def filtrar_reservas(lista_extraida):
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    archivo_historial = os.path.join(directorio_script, "historial_vistas.txt")
    reservas_ya_vistas = []

    # 1. Leemos la memoria
    if os.path.exists(archivo_historial):
        with open(archivo_historial, "r", encoding="utf-8") as archivo:
            # ¡Aquí va con los paréntesis!
            reservas_ya_vistas = archivo.read().splitlines()

    nuevas_reservas = []
    memoria_actualizada = []

    # 2. Filtramos
    for reserva in lista_extraida:
        # Tu ID perfecto: Fecha_Hora_Correo
        id_unico = f"{reserva['fecha']}_{reserva['hora']}_{reserva['correo']}"

        # Lo guardamos para la nueva memoria
        memoria_actualizada.append(id_unico)

        # Si no lo habíamos visto, es una novedad
        if id_unico not in reservas_ya_vistas:
            nuevas_reservas.append(reserva)

    # 3. Reescribimos el archivo de memoria con los IDs actualizados
    with open(archivo_historial, "w", encoding="utf-8") as archivo:
        for id_unico in memoria_actualizada:
            archivo.write(id_unico + "\n")

    return nuevas_reservas
