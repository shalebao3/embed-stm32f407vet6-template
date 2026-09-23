# Start：STM32F407 启动与内核支持

本目录只负责 STM32F407VET6 的启动和链接布局，不放 FOC 业务外设初始化。

- `startup.cmake`：统一选择 CMSIS system 文件与 GNU 启动文件。
- `STM32F407VETX_FLASH.ld`：512 KiB Flash、128 KiB SRAM、64 KiB CCMRAM。
- 启动文件：`startup_stm32f407xx.s`。
- system 文件：`system_stm32f4xx.c`。

注意：CCMRAM 适合 CPU 高频数据，但 DMA1/DMA2 无法访问，后续 ADC/DMA 采样缓冲区不能放入 CCMRAM。
