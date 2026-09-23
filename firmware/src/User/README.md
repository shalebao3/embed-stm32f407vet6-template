# User：项目入口与中断

这里保留每个工程都必须有、但不属于具体 FOC 业务模块的项目级入口：

- `main.c/.h`：系统入口与统一错误处理。
- `stm32f4xx_it.c/.h`：STM32F407 项目中断入口。

当前基线仅依赖 CMSIS，不在 User 层预置 TIM、ADC、PWM、I2C、SPI 等 FOC 外设配置。
这些实现应按职责进入 `Driver`、`Bsp` 或 `App`。
