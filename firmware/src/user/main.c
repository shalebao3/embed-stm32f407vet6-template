#include "main.h"
#include "com_time.h"

/**
 * @brief Generic STM32F407VET6 project entry point.
 * @note The template intentionally does not bind project-specific peripherals.
 *       Add peripheral configuration in driver/bsp after the hardware design is defined.
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
