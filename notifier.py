# notifier.py
import smtplib
import os
from email.message import EmailMessage

def enviar_correo(nuevas_reservas):
    # Si por alguna razón llega una lista vacía, no hacemos nada
    if not nuevas_reservas:
        return

    # --- TUS CREDENCIALES ---
    email_origen = os.environ.get("GMAIL_SENDER")
    # Recuerda: Esta es la "Contraseña de aplicación" de 16 letras de Google, NO tu clave normal
    password =  os.environ.get("CLAVE_GMAIL")
    email_destino = os.environ.get("CORREO_UC")  # Te lo envías a ti mismo
    
    # --- ARMANDO EL CORREO ---
    msg = EmailMessage()
    msg['Subject'] = f"🔔 ¡Alerta! Tienes {len(nuevas_reservas)} nuevas reservas"
    msg['From'] = email_origen
    msg['To'] = email_destino
    
    # Construimos el texto del mensaje sumando cada reserva
    cuerpo = "Hola Max, tu bot ha detectado nuevas reservas en el portal:\n\n"
    
    for reserva in nuevas_reservas:
        cuerpo += f"📚 Curso: {reserva['curso']}\n"
        cuerpo += f"📅 Cuándo: {reserva['fecha']} | ⏰ {reserva['hora']}\n"
        cuerpo += f"👤 Estudiante: {reserva['nombre']}\n"
        cuerpo += f"📧 Correo: {reserva['correo']}\n"
        cuerpo += f"📝 Descripción: {reserva['descripcion']}\n"
        cuerpo += "-" * 40 + "\n"
        
    msg.set_content(cuerpo)
    
    # --- ENVIANDO EL CORREO ---
    try:
        print("Conectando con Gmail para enviar la alerta...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Esto encripta la conexión por seguridad
        server.login(email_origen, password)
        server.send_message(msg)
        server.quit()
        print("¡Correo enviado exitosamente!")
    except Exception as e:
        print(f"Error crítico al intentar enviar el correo: {e}")