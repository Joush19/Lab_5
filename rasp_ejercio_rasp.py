import serial

def main():
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        ser.flush()
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")
        return

    try:
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').rstrip()
                    if line == 'A':
                        print("Botón 1 presionado")
                    elif line == 'B':
                        print("botón 2 presionado")
                except UnicodeDecodeError as e:
                    print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Saliendo...")
    finally:
        ser.close()
        print("Puerto serial cerrado.")

if __name__ == "__main__":
    main()
