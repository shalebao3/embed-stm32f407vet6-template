#include "main.h"
#include "com_time.h"

/**
 * @brief STM32F407VET6 Standard Peripheral Library template entry point.
 * @note Project-specific peripheral initialization belongs in driver/bsp/app.
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
