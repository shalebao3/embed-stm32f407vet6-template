# STM32F4xx Standard Peripheral Library vendor snapshot

- Package: `STM32F4xx_DSP_StdPeriph_Lib_V1.9.0`
- Target used by this template: `STM32F40_41xxx` / STM32F407VET6
- Source snapshot repository: `AbdelrahmanAbdelkhalekA/STM32Project`
- Source commit: `cad815ec39da3f1ef050160dca37c6fb34da4860`
- Vendored content: the legacy CMSIS headers required by Cortex-M4/STM32F4 plus the Standard Peripheral Library headers and sources selected for the official `STM32F40_41xxx` configuration.

The source snapshot is pinned so template builds do not depend on a moving branch or Git submodule.

Do not modify files under `Libraries/CMSIS` or `Libraries/STM32F4xx_StdPeriph_Driver` for project-specific behavior. Put project-owned peripheral configuration in `firmware/src/driver`.

The project startup/system baseline lives under `firmware/Start`; it intentionally keeps reset HSI 16 MHz instead of inheriting the legacy evaluation-board 168 MHz/HSE clock policy.
