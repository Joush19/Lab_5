import serial
import RPi.GPIO as GPIO

# Configuración UART
ser = serial.Serial('/dev/serial0', 9600)

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
motor1_pin = 18
motor2_pin = 19
GPIO.setup(motor1_pin, GPIO.OUT)
GPIO.setup(motor2_pin, GPIO.OUT)

motor1_pwm = GPIO.PWM(motor1_pin, 100)  # 100 Hz
motor2_pwm = GPIO.PWM(motor2_pin, 100)  # 100 Hz
motor1_pwm.start(0)
motor2_pwm.start(0)

while True:
    if ser.in_waiting > 0:
        message = ser.readline().decode().strip()
        if message == "motor1":
            motor1_pwm.ChangeDutyCycle(50)
        elif message == "motor2":
            motor2_pwm.ChangeDutyCycle(50)
