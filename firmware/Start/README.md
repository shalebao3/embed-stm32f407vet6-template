# Start：STM32F407 启动与链接支持

本目录只负责 STM32F407VET6 的启动和链接布局，不放项目业务外设初始化。

- `startup.cmake`：把启动文件、system 文件和 legacy CMSIS include 路径交给 CMake。
- `startup_stm32f407xx.s`：STM32F407 向量表与 Reset_Handler。
- `system_stm32f4xx.c`：模板级 CMSIS system 实现；启动阶段保持复位 HSI 16 MHz，不自动切换到外部晶振或 168 MHz。
- `STM32F407VETX_FLASH.ld`：512 KiB Flash、128 KiB SRAM、64 KiB CCMRAM。

标准外设库和 legacy CMSIS headers 固定在 `Libraries/STM32F4xx_StdPeriph_Lib`。

具体项目需要高主频时，应在项目初始化阶段基于实际板卡晶振使用 RCC Standard Peripheral Library 配置时钟，而不是修改 vendor 驱动。

注意：CCMRAM 适合 CPU 高频数据，但 DMA1/DMA2 无法访问，ADC/DMA 采样缓冲区不能放入 CCMRAM。
