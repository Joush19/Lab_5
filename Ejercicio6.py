#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/uart.h"
#include "driverlib/pin_map.h"
#include "driverlib/interrupt.h"

// Definiciones
#define BUZZER_PIN GPIO_PIN_1  // Buzzer conectado al pin PF1

void UART0IntHandler(void);

int main(void) {
    // Configuración del reloj del sistema
    SysCtlClockSet(SYSCTL_SYSDIV_5 | SYSCTL_USE_PLL | SYSCTL_XTAL_16MHZ | SYSCTL_OSC_MAIN);

    // Habilitar periféricos UART0 y GPIOF
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);

    // Configurar pines GPIO para UART
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    // Configurar pin del buzzer como salida
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, BUZZER_PIN);

    // Configurar UART a 9600 baudios
    UARTConfigSetExpClk(UART0_BASE, SysCtlClockGet(), 9600,
                        (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE | UART_CONFIG_PAR_NONE));

    // Habilitar interrupciones UART
    IntMasterEnable();
    IntEnable(INT_UART0);
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);

    // Bucle principal
    while (1) {
        // El programa espera que llegue un mensaje a través de UART
    }
}

// Manejador de interrupciones UART
void UART0IntHandler(void) {
    uint32_t ui32Status;
    char receivedData[10] = {0};
    int i = 0;

    // Obtener y borrar el estado de la interrupción
    ui32Status = UARTIntStatus(UART0_BASE, true);
    UARTIntClear(UART0_BASE, ui32Status);

    // Leer datos desde UART
    while (UARTCharsAvail(UART0_BASE)) {
        char c = UARTCharGetNonBlocking(UART0_BASE);
        if (c == '\n') break;  // Salir si llega un salto de línea
        if (i < 9) {
            receivedData[i++] = c;
        }
    }
    receivedData[i] = '\0';  // Asegurar terminación de cadena

    // Comparar el mensaje recibido
    if (strcmp(receivedData, "buzzer") == 0) {
        // Activar el buzzer durante 2 segundos
        GPIOPinWrite(GPIO_PORTF_BASE, BUZZER_PIN, BUZZER_PIN);
        SysCtlDelay(SysCtlClockGet() / 3 * 2);  // Retraso de 2 segundos
        GPIOPinWrite(GPIO_PORTF_BASE, BUZZER_PIN, 0);  // Apagar el buzzer
    }
}
