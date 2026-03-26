import os
from LoginWeb import login, extraer_reservas
from logger import filtrar_reservas
from notifier import enviar_correo

usuario_portal = os.environ.get("USUARIO_UC")
clave_portal = os.environ.get("CLAVE_UC")

if __name__ == "__main__":
    driver = login(user=usuario_portal, password=clave_portal)
    reservas = extraer_reservas(driver)
    nuevas_reservas = filtrar_reservas(reservas)
    enviar_correo(nuevas_reservas)
