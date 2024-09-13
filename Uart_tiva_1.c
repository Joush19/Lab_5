#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/uart.h"
#include "driverlib/usb.h"
#include "driverlib/interrupt.h"
#include "usb_serial_structs.h"
#include "utils/uartstudio.h"

void UART0IntHandler(void) {
    UARTIntClear(UART0_BASE, UARTIntStatus(UART0_BASE, true));
}

void setupUART(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);

    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    UARTConfigSetExpClk(UART0_BASE, SysCtlClockGet(), 115200,
                        (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE | UART_CONFIG_PAR_NONE));

    IntEnable(INT_UART0);
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);
}

void setupButtons(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
}

int main(void) {
    SysCtlClockSet(SYSCTL_SYSDIV_5 | SYSCTL_USE_PLL | SYSCTL_OSC_MAIN | SYSCTL_XTAL_16MHZ);

    setupUART();
    setupButtons();

    while (1) {
        if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {
            UARTCharPut(UART0_BASE, 'A');  // Mensaje para el botón interno
            while (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0);  // Espera a que se suelte el botón
        }
        if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {
            UARTCharPut(UART0_BASE, 'B');  // Mensaje para el otro botón
            while (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0);  // Espera a que se suelte el botón
        }
    }
}