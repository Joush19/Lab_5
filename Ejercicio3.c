import RPi.GPIO as GPIO
import time

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

# Iniciar PWM con duty cycle del 50%
motor1_pwm.start(50)  # 50% ciclo de trabajo
motor2_pwm.start(50)  # 50% ciclo de trabajo

print("Motores funcionando al 50% de ciclo de trabajo. Presiona Ctrl+C para detener.")

try:
    while True:
        time.sleep(1)  
except KeyboardInterrupt:
    # Detener el programa con Ctrl+C
    print("\nDeteniendo motores...")
    motor1_pwm.stop()
    motor2_pwm.stop()
    GPIO.cleanup()
