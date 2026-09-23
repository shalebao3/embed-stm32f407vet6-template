# CMSIS vendor source

本目录只保留 STM32F407VET6 初始工程实际需要的 CMSIS 文件，不使用 Git Submodule。

## CMSIS Core

来源：`STMicroelectronics/STM32CubeF4`

固定提交：

`89e6d4466578bc9eab83de8fcd1e397ceb5e5cc9`

保留 Cortex-M4 GCC 构建所需的 Core 头文件。

## STM32F4 CMSIS Device

来源：`STMicroelectronics/cmsis-device-f4`

固定提交：

`a833f4af71410f25b01468f976560d7ff63a2fc9`

目标器件：`STM32F407xx`，实际芯片：`STM32F407VET6`。

第三方文件按各自 LICENSE 保留；业务开发不要修改 vendor 文件。
