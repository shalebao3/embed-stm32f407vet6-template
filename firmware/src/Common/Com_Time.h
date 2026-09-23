#ifndef COM_TIME_H
#define COM_TIME_H

#include <stdint.h>
#include "stm32f4xx.h"

/**
 * @brief Configure a 1 ms SysTick time base from the current SystemCoreClock.
 */
ErrorStatus Com_Time_Init(void);

/**
 * @brief Return accumulated milliseconds. Unsigned subtraction is wrap-safe.
 */
uint32_t Com_Time_GetMs(void);

/**
 * @brief Blocking millisecond delay.
 * @note Do not call from an ISR or with interrupts globally disabled.
 */
void Com_Time_DelayMs(uint32_t delay_ms);

/**
 * @brief Advance the software tick by 1 ms. Called only from SysTick_Handler().
 */
void Com_Time_Tick(void);

#endif /* COM_TIME_H */
