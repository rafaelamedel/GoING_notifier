from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def login(user: str, password: str):
    opciones = Options()
    opciones.add_argument("--headless=new") # Esto lo vuelve invisible
    opciones.add_argument("--disable-gpu")
    driver = webdriver.Edge()
    url_login = "https://sso.uc.cl/cas/login?service=https%3A%2F%2Fgo.ing.uc.cl%2Fforce"
    driver.get(url_login)

    time.sleep(3)

    campo_usuario = driver.find_element(By.XPATH, '//*[@id="username"]')
    campo_usuario.send_keys(user)

    campo_clave = driver.find_element(By.XPATH, '//*[@id="password"]')
    campo_clave.send_keys(password)
    campo_clave.send_keys(Keys.RETURN)
    time.sleep(2)

    return driver


def extraer_reservas(driver: webdriver):
    driver.get("https://go.ing.uc.cl/mis_reservas/")
    time.sleep(2)
    # Buscamos solo por la clase que identifica a las reservas
    cajas_reservas = driver.find_elements(By.CLASS_NAME, "request-item")
    lista_reservas = []

    for caja in cajas_reservas:
        texto_completo = caja.text
        if not texto_completo:
            continue
        
        lineas_texto = texto_completo.split("\n")
        fecha = None
        hora = None
        for linea in lineas_texto:
            if "calendar_today" in linea:
                # Quitamos la palabra 'calendar_today' y los espacios
                fecha = linea.replace("calendar_today", "").strip()
            elif "schedule" in linea:
                hora = linea.replace("schedule", "").strip()
        botones = caja.find_elements(By.TAG_NAME, "button")
        if len(botones) > 0:
            boton_info = botones[0]
            correo = boton_info.get_attribute("data-student-email")
            nombre = boton_info.get_attribute("data-student-name")
            descripcion = boton_info.get_attribute("data-student-description")
            curso = boton_info.get_attribute("data-course-name")

            reserva = {
                "curso": curso,
                "nombre": nombre,
                "correo": correo,
                "descripcion": descripcion,
                "fecha": fecha,
                "hora": hora
            }
            lista_reservas.append(reserva)
    return (lista_reservas)
