# driver：STM32 片内外设驱动层（Driver）

放置 TIM、ADC、DMA、USART、I2C、SPI 等 STM32F407 片内外设的项目驱动。

命名规则：

- 文件：`drv_<外设>.c/.h`
- 公开 API：`Drv_<Module>_...`

模板只固定 CMSIS 与启动环境，不预置具体 TIM / ADC / DMA 配置。外设工作模式、触发关系和 DMA 方案应根据具体项目硬件拓扑与 Pin Map 再实现。
