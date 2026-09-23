#include "main.h"
#include "Com_Time.h"

/**
 * @brief FOC project entry point.
 * @note The base project intentionally does not bind TIM/ADC/PWM/I2C/SPI yet.
 *       Peripheral configuration will be added after the driver-board pin map is frozen.
 */
int main(void)
{
    SystemCoreClockUpdate();

    if (Com_Time_Init() != SUCCESS)
    {
        Error_Handler();
    }

    while (1)
    {
    }
}

void Error_Handler(void)
{
    __disable_irq();

    while (1)
    {
    }
}
