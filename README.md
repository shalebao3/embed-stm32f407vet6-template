# embed-FOC

STM32F407VET6 的 FOC 学习与三相电机控制工程。

当前仓库已从 STM32F103C8T6 模板迁移为 **STM32F407VET6 初始工程**。本阶段只冻结 MCU、启动、链接、CMSIS 和工程分层，不提前绑定具体 Gate Driver、FOC 外设方案和引脚。

## 当前基线

- MCU：STM32F407VET6（Cortex-M4F）
- Flash：512 KiB
- SRAM1 + SRAM2：128 KiB
- CCMRAM：64 KiB
- 编译器：arm-none-eabi-gcc
- 构建：CMake + Ninja
- 调试：ST-Link / Cortex-Debug
- CMSIS Device：STM32F407xx
- FPU：FPv4-SP-D16，hard-float ABI
- 当前系统时钟：复位默认 HSI 16 MHz
- 当前不预置 HAL / Standard Peripheral Library
- 当前不预置 TIM / ADC / DMA / I2C / SPI / PWM 业务配置

先保持 CMSIS-only，是为了把“C8T6 模板迁移到 F407”和“FOC 外设/驱动板设计”拆开。等 Gate Driver、采样拓扑和 Pin Map 确定后，再按实际方案加入 Driver，避免把未经确认的 PWM/ADC 配置固化进初始工程。

## 目录

```text
.
├── .github/workflows/
├── .vscode/
├── firmware/
│   ├── Libraries/
│   │   └── CMSIS/
│   ├── Start/
│   │   ├── startup.cmake
│   │   ├── STM32F407VETX_FLASH.ld
│   │   └── README.md
│   ├── cmake/
│   ├── src/
│   │   ├── User/
│   │   ├── App/
│   │   ├── Driver/
│   │   ├── Bsp/
│   │   └── Common/
│   ├── CMakeLists.txt
│   └── CMakePresets.json
├── tests/
└── README.md
```

## 分层职责

| 目录 | 职责 |
| --- | --- |
| `User` | main 与中断入口 |
| `App` | FOC 状态机、控制模式与算法编排 |
| `Driver` | STM32 片内 TIM / ADC / DMA / I2C / SPI 等驱动 |
| `Bsp` | FOC 驱动板引脚、Gate Driver、编码器等板级映射 |
| `Common` | 时间基准等跨模块通用能力 |
| `Start` | 启动文件、CMSIS system、链接布局 |

当前 `Common` 保留 `Com_Time`，使用 SysTick 提供 1 ms 软件时间基准。

## 构建

从仓库根目录执行：

```bash
cmake -S firmware -B firmware/build/Debug -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_TOOLCHAIN_FILE=firmware/cmake/gcc-arm-none-eabi.cmake

cmake --build firmware/build/Debug
```

输出：

```text
firmware/build/Debug/
├── embed_foc.elf
├── embed_foc.hex
├── embed_foc.bin
└── embed_foc.map
```

GitHub Actions 同时编译 Debug / Release，并验证：

- Cortex-M4F / FPU 编译参数；
- `STM32F407xx` 目标宏；
- F407 startup / system 只编译一份；
- 512 KiB Flash / 128 KiB SRAM / 64 KiB CCMRAM 链接布局；
- BIN / HEX / MAP 构建产物。

## FOC 后续外设方向

驱动板原理图和 Pin Map 确定后再落代码，预计使用：

- TIM1：三相互补 PWM、Dead Time、Break、ADC 触发；
- ADC1 / ADC2：相电流采样；
- DMA：是否使用取决于最终采样时序；
- I2C：AS5600；
- SPI：若 Gate Driver 采用 SPI 配置；
- GPIO / EXTI：Enable、Fault 等。

## 当前边界

- 不把 DRV8301 / DRV8323、AS5600 或 FOC 算法提前塞进初始工程。
- 不提前固定 TIM1 / ADC / SPI / I2C 引脚，等驱动板 Pin Map 冻结后再配置。
- ADC / DMA 缓冲区不要放进 CCMRAM；STM32F407 的 DMA1 / DMA2 无法访问 CCMRAM。
- `firmware/Libraries/CMSIS` 是固定 vendor 代码，不在业务开发中修改。
