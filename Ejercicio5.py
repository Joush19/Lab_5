import RPi.GPIO as GPIO
import serial
import time

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)

# Pin para el botón
button_pin = 17
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Botón con resistencia pull-up

# Configuración del puerto UART
uart_port = '/dev/serial0'  # Puerto UART en Raspberry Pi
baud_rate = 9600  # Velocidad de comunicación
ser = serial.Serial(uart_port, baud_rate, timeout=1)

print("Presiona el botón para enviar el mensaje 'buzzer' a la Tiva.")

try:
    while True:
        # Leer el estado del botón
        button_state = GPIO.input(button_pin)
        
        if button_state == GPIO.LOW:  # El botón está presionado
            print("Botón presionado. Enviando mensaje 'buzzer'...")
            ser.write(b"buzzer\n")  # Enviar mensaje por UART
            time.sleep(0.5)  # Evitar rebotes del botón
except KeyboardInterrupt:
    # Detener el programa con Ctrl+C
    print("\nTerminando programa...")
finally:
    # Cerrar UART y limpiar GPIO
    ser.close()
    GPIO.cleanup()
