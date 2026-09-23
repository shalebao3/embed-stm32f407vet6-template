# Driver：STM32 片内外设驱动层

放置 TIM、ADC、DMA、USART、I2C、SPI 等 STM32F407 片内外设的项目驱动。

当前 F407 初始工程只固定 CMSIS 与启动环境，不预置具体 TIM / ADC / DMA 配置。FOC 的 PWM 频率、中心对齐模式、ADC 触发点、采样通道和 DMA 方案必须等驱动板拓扑与 Pin Map 确定后再实现。
