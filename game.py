import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# Diccionario para almacenar información de usuarios registrados y hacer seguimiento a los recaptcha y las credenciales
usuarios = {}
intentos_recaptcha = {}
intentos_credenciales = {}

# Constantes para el número máximo de intentos de recaptcha y credenciales
MAX_INTENTOS_RECAPTCHA = 3
MAX_INTENTOS_CREDENCIALES = 3

# Función para generar un recaptcha aleatorio
def generar_recaptcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operadores = ["+", "-", "*", "/"]
    operador = random.choice(operadores)
    respuesta = eval(f"{num1} {operador} {num2}")
    return num1, num2, operador, respuesta

# Función para registrar un nuevo usuario
def registrar_usuario():
    nombre = simpledialog.askstring("Registro", "Ingrese su nombre:")
    usuario_correo = simpledialog.askstring("Registro", "Ingrese su usuario de correo:")
    contrasena = simpledialog.askstring("Registro", "Ingrese su contraseña:")

    recaptcha_num1, recaptcha_num2, recaptcha_operador, recaptcha_respuesta = generar_recaptcha()

    recaptcha_usuario = simpledialog.askfloat(
        "Recaptcha",
        f"Resuelva el siguiente recaptcha:\n{recaptcha_num1} {recaptcha_operador} {recaptcha_num2}\nIngrese su respuesta:"
    )

    if recaptcha_usuario != recaptcha_respuesta:
        messagebox.showerror("Error", "Recaptcha incorrecto. Registro fallido.")
        return

    usuarios[usuario_correo] = {
        "nombre": nombre,
        "contrasena": contrasena,
        "puntaje": 0,
        "vidas": 5,
    }
    messagebox.showinfo("Registro", "Registro exitoso.")

# Función para iniciar sesión
def iniciar_sesion():
    usuario_correo = simpledialog.askstring("Inicio de Sesión", "Ingrese su usuario de correo:")

    # Verificar si la cuenta de correo no existe
    if usuario_correo not in usuarios:
        messagebox.showerror("Error", "La cuenta no existe.")
        return

    # Verificar intentos de recaptcha bloqueados
    if usuario_correo in intentos_recaptcha and intentos_recaptcha[usuario_correo] >= MAX_INTENTOS_RECAPTCHA:
        messagebox.showerror("Bloqueado", "Has sido bloqueado. Comunica con el administrador o el área de soporte.")
        return

    # Proceso de validación de recaptcha y credenciales
    intentos_recaptcha[usuario_correo] = 0
    while intentos_recaptcha[usuario_correo] < MAX_INTENTOS_RECAPTCHA:
        recaptcha_num1, recaptcha_num2, recaptcha_operador, recaptcha_respuesta = generar_recaptcha()

        recaptcha_usuario = simpledialog.askfloat(
            "Recaptcha",
            f"Resuelva el siguiente recaptcha:\n{recaptcha_num1} {recaptcha_operador} {recaptcha_num2}\nIngrese su respuesta:"
        )

        if usuario_correo in usuarios and recaptcha_usuario == recaptcha_respuesta:
            intentos_credenciales[usuario_correo] = 0

            contrasena = simpledialog.askstring("Inicio de Sesión", "Ingrese su contraseña:")

            if usuarios[usuario_correo]["contrasena"] == contrasena:
                messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")
                jugar(usuario_correo)
                break
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")
                intentos_credenciales[usuario_correo] = intentos_credenciales.get(usuario_correo, 0) + 1
                if intentos_credenciales[usuario_correo] >= MAX_INTENTOS_CREDENCIALES:
                    messagebox.showerror("Bloqueado", "Has excedido el número máximo de intentos de credenciales. Bloqueando recaptcha.")
                    intentos_recaptcha[usuario_correo] = MAX_INTENTOS_RECAPTCHA
                    return
        else:
            messagebox.showerror("Error", "Credenciales o recaptcha incorrectos.")
            intentos_recaptcha[usuario_correo] += 1

    if intentos_recaptcha[usuario_correo] >= MAX_INTENTOS_RECAPTCHA:
        messagebox.showerror("Bloqueado", "Has sido bloqueado. Comunica con el administrador o el área de soporte.")

# Función para jugar al juego de matemáticas
def jugar(usuario_correo):
    messagebox.showinfo("Bienvenido", "¡Bienvenido al juego de matemáticas!")

    while usuarios[usuario_correo]["vidas"] > 0:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operador = random.choice(["+", "-", "*", "/"])

        respuesta_correcta = eval(f"{num1} {operador} {num2}")

        opcion = simpledialog.askinteger(
            "Opción",
            f"Pregunta: ¿Cuánto es {num1} {operador} {num2}?\n\nOpción 1: Responder la pregunta\nOpción 2: Salir del juego",
            minvalue=1, maxvalue=2
        )

        if opcion == 1:
            respuesta_usuario = simpledialog.askfloat("Respuesta", f"¿Cuánto es {num1} {operador} {num2}?")
            
            if respuesta_usuario == respuesta_correcta:
                messagebox.showinfo("Respuesta Correcta", "¡Respuesta correcta!")
                usuarios[usuario_correo]["puntaje"] += 50  # Asignar 50 puntos por respuesta correcta
                messagebox.showinfo("Puntos", f"Tu puntaje actual es: {usuarios[usuario_correo]['puntaje']}")
            else:
                messagebox.showwarning("Respuesta Incorrecta", "Respuesta incorrecta. Pierdes una vida.")
                usuarios[usuario_correo]["vidas"] -= 1

                if usuarios[usuario_correo]["vidas"] == 0:
                    messagebox.showwarning("Perdiste", "¡Perdiste todas tus vidas!")
                    mostrar_resultados(usuario_correo)

        elif opcion == 2:
            messagebox.showinfo("Salida", "Saliendo del juego.")
            break

# Función para mostrar los resultados al final del juego
def mostrar_resultados(usuario_correo):
    messagebox.showinfo("Resultados", f"Tu puntaje total es: {usuarios[usuario_correo]['puntaje']}")

# Función principal del programa
def main():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    while True:
        opcion = simpledialog.askinteger(
            "Menú Principal",
            "Seleccione una opción:\n\n1. Registrarse\n2. Iniciar sesión\n3. Salir del juego",
            minvalue=1, maxvalue=3
        )

        if opcion == 1:
            registrar_usuario()
        elif opcion == 2:
            iniciar_sesion()
        elif opcion == 3:
            messagebox.showinfo("Salida", "Saliendo del juego.")
            break

# Ejecución del programa si se ejecuta directamente
if __name__ == "__main__":
    main()