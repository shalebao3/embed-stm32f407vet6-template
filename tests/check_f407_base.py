#!/usr/bin/env python3
"""Verify the STM32F407VET6 Standard Peripheral Library template."""

import argparse
import json
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir", type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    firmware = root / "firmware"
    build = args.build_dir.resolve()
    library = firmware / "Libraries" / "STM32F4xx_StdPeriph_Lib"
    cmsis = library / "Libraries" / "CMSIS"
    core = cmsis / "Include"
    device = cmsis / "Device" / "ST" / "STM32F4xx"
    stdperiph = library / "Libraries" / "STM32F4xx_StdPeriph_Driver"
    project_source = firmware / "src"
    start = firmware / "Start"

    for directory in ("user", "app", "driver", "bsp", "common"):
        require((project_source / directory).is_dir(), "Missing src directory: " + directory)

    required_files = [
        library / "VENDOR_INFO.md",
        library / "LICENSE.txt",
        core / "core_cm4.h",
        core / "core_cmFunc.h",
        core / "core_cmInstr.h",
        core / "core_cmSimd.h",
        device / "Include" / "stm32f4xx.h",
        device / "Include" / "system_stm32f4xx.h",
        stdperiph / "LICENSE.txt",
        stdperiph / "inc" / "stm32f4xx_gpio.h",
        stdperiph / "inc" / "stm32f4xx_tim.h",
        stdperiph / "inc" / "stm32f4xx_adc.h",
        stdperiph / "inc" / "stm32f4xx_dma.h",
        stdperiph / "inc" / "stm32f4xx_rcc.h",
        stdperiph / "src" / "stm32f4xx_gpio.c",
        stdperiph / "src" / "stm32f4xx_tim.c",
        stdperiph / "src" / "stm32f4xx_adc.c",
        stdperiph / "src" / "stm32f4xx_dma.c",
        stdperiph / "src" / "stm32f4xx_rcc.c",
        start / "STM32F407VETX_FLASH.ld",
        start / "startup_stm32f407xx.s",
        start / "system_stm32f4xx.c",
        project_source / "user" / "main.c",
        project_source / "user" / "main.h",
        project_source / "user" / "stm32f4xx_conf.h",
        project_source / "user" / "stm32f4xx_it.c",
        project_source / "user" / "stm32f4xx_it.h",
        project_source / "common" / "com_time.c",
        project_source / "common" / "com_time.h",
    ]
    for path in required_files:
        require(path.is_file(), "Missing required file: " + str(path))

    require(
        not (firmware / "Libraries" / "CMSIS").exists(),
        "Old standalone CMSIS tree still exists",
    )

    conf = (project_source / "user" / "stm32f4xx_conf.h").read_text(
        encoding="utf-8", errors="replace"
    )
    for header in (
        "stm32f4xx_gpio.h",
        "stm32f4xx_tim.h",
        "stm32f4xx_adc.h",
        "stm32f4xx_dma.h",
        "stm32f4xx_rcc.h",
        "misc.h",
    ):
        require(header in conf, "stm32f4xx_conf.h is missing " + header)

    system_source = (start / "system_stm32f4xx.c").read_text(
        encoding="utf-8", errors="replace"
    )
    require(
        "uint32_t SystemCoreClock = 16000000" in system_source,
        "Template system clock baseline is not HSI 16 MHz",
    )
    require(
        "SetSysClock();" not in system_source,
        "Template unexpectedly auto-configures the system clock",
    )

    linker = (start / "STM32F407VETX_FLASH.ld").read_text(encoding="utf-8")
    require("LENGTH = 512K" in linker, "Flash length is not 512K")
    require("LENGTH = 128K" in linker, "SRAM length is not 128K")
    require("LENGTH = 64K" in linker, "CCMRAM length is not 64K")

    commands = json.loads((build / "compile_commands.json").read_text(encoding="utf-8"))

    expected_units = {
        "main.c": project_source / "user" / "main.c",
        "stm32f4xx_it.c": project_source / "user" / "stm32f4xx_it.c",
        "com_time.c": project_source / "common" / "com_time.c",
        "system_stm32f4xx.c": start / "system_stm32f4xx.c",
        "startup_stm32f407xx.s": start / "startup_stm32f407xx.s",
        "stm32f4xx_gpio.c": stdperiph / "src" / "stm32f4xx_gpio.c",
        "stm32f4xx_tim.c": stdperiph / "src" / "stm32f4xx_tim.c",
        "stm32f4xx_adc.c": stdperiph / "src" / "stm32f4xx_adc.c",
        "stm32f4xx_dma.c": stdperiph / "src" / "stm32f4xx_dma.c",
        "stm32f4xx_rcc.c": stdperiph / "src" / "stm32f4xx_rcc.c",
    }

    for filename, expected_path in expected_units.items():
        units = [entry for entry in commands if Path(entry["file"]).name == filename]
        require(len(units) == 1, filename + " must be compiled exactly once")
        unit = Path(units[0]["file"])
        if not unit.is_absolute():
            unit = Path(units[0]["directory"]) / unit
        require(unit.resolve() == expected_path.resolve(), filename + " source path is wrong")

    all_commands = "\n".join(
        entry.get("command", " ".join(entry.get("arguments", [])))
        for entry in commands
    )
    for token in (
        "-mcpu=cortex-m4",
        "-mfpu=fpv4-sp-d16",
        "-mfloat-abi=hard",
        "-DSTM32F40_41xxx",
        "-DUSE_STDPERIPH_DRIVER",
    ):
        require(token in all_commands, "Missing compiler target option: " + token)

    require(
        "-DSTM32F407xx" not in all_commands,
        "Build still uses the newer CMSIS device macro STM32F407xx",
    )
    require("STM32F10" not in all_commands, "Build commands reference STM32F10x")

    project = "stm32f407_std_template"
    for suffix in (".elf", ".bin", ".hex", ".map"):
        artifact = build / (project + suffix)
        require(
            artifact.is_file() and artifact.stat().st_size > 0,
            "Missing build artifact: " + str(artifact),
        )

    print(
        "PASS: STM32F407VET6 StdPeriph template, legacy CMSIS target macro, "
        "HSI startup baseline, SPL source units and firmware artifacts"
    )


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError) as exc:
        raise SystemExit("F407 StdPeriph verification failed: " + str(exc)) from exc
