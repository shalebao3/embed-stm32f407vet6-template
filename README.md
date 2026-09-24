# STM32F407VET6 工程模板

用于后续电子设计竞赛、控制类项目和嵌入式实验的 STM32F407VET6 基础脚手架。

当前 `main` 固定为：

- MCU：STM32F407VET6（Cortex-M4F）
- Flash：512 KiB
- SRAM1 + SRAM2：128 KiB
- CCMRAM：64 KiB
- CMSIS Core + STM32F4 CMSIS Device
- 目标宏：`STM32F407xx`
- FPU：FPv4-SP-D16，hard-float ABI
- arm-none-eabi-gcc
- CMake + Ninja
- VSCode + Cortex-Debug
- ST-Link
- 当前系统时钟：复位默认 HSI 16 MHz
- 不使用 CubeMX
- 不预置 HAL
- 不预置 STM32F4 Standard Peripheral Library

模板只保留可跨项目复用的工程基础设施。ADC、TIM、DMA、PWM、编码器、电机驱动等具体业务配置不预置，避免上一项目的实现污染下一项目。

## 目录分层

```text
.
├── .github/
│   └── workflows/
│       └── firmware-build.yml
├── .vscode/
├── firmware/
│   ├── Start/
│   │   ├── startup.cmake
│   │   ├── STM32F407VETX_FLASH.ld
│   │   └── README.md
│   ├── Libraries/
│   │   └── CMSIS/
│   │       ├── Core/
│   │       ├── Device/
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
| `Start` | 启动文件、CMSIS system、链接脚本 |
| `user` | main、中断入口和项目级错误处理 |
| `app` | 项目业务流程、状态机、算法编排 |
| `driver` | STM32 片内 ADC/TIM/DMA/UART/I2C/SPI 等驱动 |
| `bsp` | 板级 GPIO、外部器件与硬件接口映射 |
| `common` | 与具体项目无关的通用组件 |

当前 `common` 预置 `com_time.c/.h`，统一提供 1 ms SysTick 时间基准。

### 自定义源码命名规范

自定义目录和文件统一使用小写 `snake_case`，减少 macOS / Linux 大小写差异带来的构建问题：

- `app/app_<功能>.c/.h`，公开 API 使用 `App_<Module>_...`；
- `driver/drv_<外设>.c/.h`，公开 API 使用 `Drv_<Module>_...`；
- `bsp/bsp_<器件>.c/.h`，公开 API 使用 `Bsp_<Module>_...`；
- `common/com_<组件>.c/.h`，公开 API 使用 `Com_<Module>_...`；
- `user` 中的 `main.c`、`stm32f4xx_it.c/.h` 等 STM32 约定文件保留官方命名。

文件名负责表达模块归属，函数名前缀负责表达“软件层 + 模块 + 动作”。不要混用 `App_Xxx.c`、`bsp_Xxx.c`、`Driver_xxx.c` 等文件命名风格。

### CMSIS 管理

`firmware/Libraries/CMSIS` 已作为普通 Git tracked files 固化到模板仓库，不使用 Git Submodule。

当前保留 STM32F407VET6 初始工程实际需要的：

- Cortex-M4 CMSIS Core 头文件；
- STM32F407xx Device 头文件；
- `system_stm32f4xx.c`；
- `startup_stm32f407xx.s`。

固定上游来源与提交记录在 `firmware/Libraries/CMSIS/VENDOR_INFO.md`。业务开发不要修改该目录中的 vendor 文件。

## 为什么不预置 ADC、TIM、DMA 和电机控制配置

STM32F407VET6 后续项目可能使用完全不同的外设组合，例如：

- TIM1/TIM8 互补 PWM
- TIM Encoder Mode
- 输入捕获
- TIM 触发 ADC
- ADC + DMA
- 多 ADC 同步采样
- UART / SPI / I2C
- CAN
- 电机、电源、传感器等外部器件

这些配置与具体项目的引脚、时钟树、采样时序和硬件拓扑强相关，因此模板只保留分层位置，不提前绑定固定外设方案。

另外，STM32F407 的 64 KiB CCMRAM 不能被 DMA1/DMA2 访问；后续 ADC/DMA 等缓冲区不要放入 CCMRAM。

## 首次使用

仓库已经包含构建所需的 CMSIS 文件，无需执行任何 submodule 初始化命令。

确认工具链：

```bash
arm-none-eabi-gcc --version
cmake --version
ninja --version
```

## 构建

从仓库根目录执行：

```bash
cmake -S firmware -B firmware/build/Debug -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_TOOLCHAIN_FILE=firmware/cmake/gcc-arm-none-eabi.cmake

cmake --build firmware/build/Debug
```

当前构建输出：

```text
firmware/build/Debug/
├── stm32f407_template.elf
├── stm32f407_template.hex
├── stm32f407_template.bin
└── stm32f407_template.map
```

> 当前模板默认 `CMAKE_PROJECT_NAME` 为 `stm32f407_template`。通过模板创建新项目后，应将其修改为对应项目名。

GitHub Actions 会同时验证 Debug / Release，并检查：

- Cortex-M4F / FPU 编译参数；
- `STM32F407xx` 目标宏；
- F407 startup / system 编译来源；
- 512 KiB Flash / 128 KiB SRAM / 64 KiB CCMRAM 链接布局；
- BIN / HEX / MAP 构建产物。

## 新项目的推荐起步方式

1. 通过 GitHub 的 **Use this template** 创建新的项目仓库。
2. 修改 `firmware/CMakeLists.txt` 中的 `CMAKE_PROJECT_NAME`。
3. 在 `app/` 创建业务入口，例如 `app_xxx.c/.h`，公开 API 使用 `App_Xxx_...` 前缀。
4. 按实际方案在 `driver/` 增加 ADC、TIM、DMA、SPI、I2C 等片内外设驱动，例如 `drv_tim.c/.h`。
5. 按实际硬件在 `bsp/` 增加板级引脚和外部器件控制，例如 `bsp_motor.c/.h`。
6. 在 `main.c` 中完成初始化，并在主循环调用对应的 `App_Xxx_Task()`。
7. 本地 Debug 构建通过后再提交，由 GitHub Actions 验证 Debug / Release。

CMake 已使用 `CONFIGURE_DEPENDS` 自动发现 `user/app/driver/bsp/common` 下新增的 `.c` 文件，因此通常不需要每增加一个模块就手工修改源码列表。

## 架构原则

```text
main / IRQ
    │
    ▼
   App
  / | \
 ▼  ▼  ▼
Driver Bsp Common
   \   |   /
    CMSIS Device
        │
        ▼
      寄存器
        │
        ▼
 STM32F407VET6
```

核心边界：

- App 决定“做什么”。
- Driver 决定“STM32 片内外设怎么工作”。
- Bsp 决定“当前板子具体接到哪里、怎么驱动外部器件”。
- Common 只放真正跨项目通用的能力。
- Start 只维护启动、system 和链接布局。
- 不修改固定版本的 CMSIS vendor 文件。

## GitHub Template Repository

建议在仓库 **Settings → General** 中勾选 **Template repository**。

以后新建 STM32F407VET6 项目时，可以直接：

```text
embed-stm32f407vet6-template
          ↓
    Use this template
          ↓
    embed-xxxx-xxxx
          ↓
 app + driver + bsp
```

这样无需复制旧项目历史，也不需要每次重新搭建启动文件、链接脚本、CMake、VSCode 和 CI 基础环境。
