# STM32F407VET6 标准库工程模板

用于电子设计竞赛、控制类项目和嵌入式实验的 STM32F407VET6 基础脚手架。

当前 `main` 固定为：

- MCU：STM32F407VET6（Cortex-M4F）
- Flash：512 KiB
- SRAM1 + SRAM2：128 KiB
- CCMRAM：64 KiB
- STM32F4xx Standard Peripheral Library（SPL）V1.9.0
- CMSIS Cortex-M4 + STM32F4 legacy Device headers
- 目标宏：`STM32F40_41xxx`
- 标准库开关：`USE_STDPERIPH_DRIVER`
- FPU：FPv4-SP-D16，hard-float ABI
- arm-none-eabi-gcc
- CMake + Ninja
- VSCode + Cortex-Debug
- ST-Link
- 模板默认系统时钟：复位 HSI 16 MHz
- 不使用 CubeMX
- 不使用 HAL

模板的目标是与 STM32F103C8T6 标准库模板保持同一开发范式：项目代码优先调用 Standard Peripheral Library API，例如 `GPIO_Init()`、`TIM_TimeBaseInit()`、`ADC_Init()`、`DMA_Init()`；需要理解底层时，再从标准库函数继续追到寄存器实现。

模板只保留可跨项目复用的基础设施，不预置具体 ADC 通道、TIM 工作模式、PWM、编码器、电机控制或项目状态机。

## 目录分层

```text
.
├── .github/
├── .vscode/
├── firmware/
│   ├── Start/
│   │   ├── startup.cmake
│   │   ├── startup_stm32f407xx.s
│   │   ├── system_stm32f4xx.c
│   │   ├── STM32F407VETX_FLASH.ld
│   │   └── README.md
│   ├── Libraries/
│   │   └── STM32F4xx_StdPeriph_Lib/
│   │       ├── Libraries/
│   │       │   ├── CMSIS/
│   │       │   └── STM32F4xx_StdPeriph_Driver/
│   │       ├── LICENSE.txt
│   │       └── VENDOR_INFO.md
│   ├── cmake/
│   ├── src/
│   │   ├── user/
│   │   ├── app/
│   │   ├── driver/
│   │   ├── bsp/
│   │   └── common/
│   ├── CMakeLists.txt
│   └── CMakePresets.json
├── tests/
└── README.md
```

### 分层职责

| 目录 | 职责 |
| --- | --- |
| `Start` | 启动文件、system、链接脚本；保持模板级启动基线 |
| `user` | `main`、中断入口、`stm32f4xx_conf.h` |
| `app` | 项目业务流程、状态机、算法编排 |
| `driver` | 基于 SPL 的 STM32 片内 ADC/TIM/DMA/UART/I2C/SPI 等驱动 |
| `bsp` | 板级 GPIO、外部器件与硬件接口映射 |
| `common` | 与具体项目无关的通用组件 |

### 自定义源码命名规范

- `app/app_<功能>.c/.h`，公开 API 使用 `App_<Module>_...`；
- `driver/drv_<外设>.c/.h`，公开 API 使用 `Drv_<Module>_...`；
- `bsp/bsp_<器件>.c/.h`，公开 API 使用 `Bsp_<Module>_...`；
- `common/com_<组件>.c/.h`，公开 API 使用 `Com_<Module>_...`；
- `user` 中的 `main.c`、`stm32f4xx_it.c/.h`、`stm32f4xx_conf.h` 保留 STM32 约定命名。

## 标准外设库

`firmware/Libraries/STM32F4xx_StdPeriph_Lib` 固定保存 F4 legacy Standard Peripheral Library 所需文件，不使用 Git Submodule。

当前目标是 `STM32F40_41xxx`，因此 `user/stm32f4xx_conf.h` 使用 ST 模板对该系列启用的外设头文件。项目自己的 Driver 层不要修改 vendor 源码；需要封装 TIM、ADC、DMA 等功能时，在 `src/driver` 新建 `drv_xxx.c/.h`。

典型调用链：

```text
App / BSP
    ↓
Driver
    ↓
STM32F4xx Standard Peripheral Library
    ↓
CMSIS Device
    ↓
寄存器
    ↓
STM32F407VET6
```

例如：

```c
GPIO_Init(GPIOA, &gpio_init);
TIM_TimeBaseInit(TIM1, &tim_init);
ADC_Init(ADC1, &adc_init);
DMA_Init(DMA2_Stream0, &dma_init);
```

当你需要理解底层时，可以继续进入 `stm32f4xx_gpio.c`、`stm32f4xx_tim.c` 等文件查看这些函数如何配置寄存器。

## 时钟基线

模板启动阶段保持 STM32 复位后的 HSI 16 MHz，不自动绑定某块开发板的 HSE 晶振，也不默认切到 168 MHz。

具体项目如果需要 168 MHz，应在项目初始化代码中基于实际晶振参数使用 RCC 标准库配置，并随后调用 `SystemCoreClockUpdate()`。如果使用 HSE，必须让 `HSE_VALUE` 与真实晶振频率一致。

这样模板不会因为不同 F407 核心板的晶振差异而在启动阶段失效。

## 构建

```bash
cmake -S firmware -B firmware/build/Debug -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_TOOLCHAIN_FILE=firmware/cmake/gcc-arm-none-eabi.cmake

cmake --build firmware/build/Debug
```

构建输出：

```text
firmware/build/Debug/
├── stm32f407_std_template.elf
├── stm32f407_std_template.hex
├── stm32f407_std_template.bin
└── stm32f407_std_template.map
```

## 新项目推荐起步方式

1. 使用 **Use this template** 创建新仓库。
2. 修改 `CMAKE_PROJECT_NAME`。
3. 在 `driver/` 用 SPL API 封装实际外设工作模式。
4. 在 `bsp/` 绑定当前硬件引脚和外部器件。
5. 在 `app/` 编排状态机和控制算法。
6. 在 `main.c` 初始化并调度 App。
7. 本地 Debug 构建通过后再提交，由 GitHub Actions 验证 Debug / Release。

另外，STM32F407 的 64 KiB CCMRAM 不能被 DMA1/DMA2 访问；ADC/DMA 等缓冲区不要放入 CCMRAM。
