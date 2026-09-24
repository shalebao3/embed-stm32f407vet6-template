# driver：STM32 片内外设驱动层（Driver）

放置 TIM、ADC、DMA、USART、I2C、SPI 等 STM32F407 片内外设的项目驱动。

命名规则：

- 文件：`drv_<外设>.c/.h`
- 公开 API：`Drv_<Module>_...`

本模板固定使用 STM32F4xx Standard Peripheral Library。Driver 层默认通过 SPL API 配置片内外设，例如：

```c
GPIO_Init(GPIOA, &gpio_init);
TIM_TimeBaseInit(TIM1, &tim_init);
ADC_Init(ADC1, &adc_init);
DMA_Init(DMA2_Stream0, &dma_init);
```

不要把具体项目的通道、Pin Map、PWM 频率或控制策略写进 vendor 标准库。需要追底层时，进入 `Libraries/STM32F4xx_StdPeriph_Lib/.../src` 查看标准库函数对应的寄存器操作。
