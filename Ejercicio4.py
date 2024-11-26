import RPi.GPIO as GPIO

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)

# Pines PWM para los motores
motor1_pin = 18
motor2_pin = 19

# Configurar los pines como salida
GPIO.setup(motor1_pin, GPIO.OUT)
GPIO.setup(motor2_pin, GPIO.OUT)

# Inicializar PWM con una frecuencia de 100 Hz
motor1_pwm = GPIO.PWM(motor1_pin, 100)  # Motor 1
motor2_pwm = GPIO.PWM(motor2_pin, 100)  # Motor 2

# Iniciar PWM con duty cycle al 50%
motor1_pwm.start(50)
motor2_pwm.start(50)

print("Motores funcionando. Puedes modificar el ciclo de trabajo mediante SSH.")
print("Ejemplo: Ingresa '40 60' para ajustar motor1 al 40% y motor2 al 60%.")
print("Presiona Ctrl+C para salir.")

try:
    while True:
        # Solicitar al usuario que ingrese los duty cycles mediante SSH
        input_data = input("Introduce duty cycles (motor1 motor2): ")
        try:
            # Parsear los valores ingresados
            duty1, duty2 = map(float, input_data.split())
            if 0 <= duty1 <= 100 and 0 <= duty2 <= 100:
                # Ajustar el ciclo de trabajo de los motores
                motor1_pwm.ChangeDutyCycle(duty1)
                motor2_pwm.ChangeDutyCycle(duty2)
                print(f"Motor 1 ajustado al {duty1}% y Motor 2 al {duty2}%")
            else:
                print("Error: Los valores deben estar entre 0 y 100.")
        except ValueError:
            print("Error: Ingresa dos valores numéricos separados por un espacio.")
except KeyboardInterrupt:
    # Detener el programa con Ctrl+C
    print("\nDeteniendo motores...")
    motor1_pwm.stop()
    motor2_pwm.stop()
    GPIO.cleanup()
