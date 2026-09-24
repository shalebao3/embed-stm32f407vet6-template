# user：项目入口、中断与标准库配置

这里保留每个工程都必须有、但不属于具体业务模块的项目级入口：

- `main.c/.h`：系统入口与统一错误处理。
- `stm32f4xx_it.c/.h`：STM32F407 项目中断入口。
- `stm32f4xx_conf.h`：STM32F4 Standard Peripheral Library 头文件配置。

CMake 定义 `STM32F40_41xxx` 和 `USE_STDPERIPH_DRIVER`，因此 `stm32f4xx.h` 会自动包含 `stm32f4xx_conf.h`。

ADC、TIM、DMA、电机等具体实现不要堆进 `user`；它们应进入 `driver`、`bsp` 或 `app`。
