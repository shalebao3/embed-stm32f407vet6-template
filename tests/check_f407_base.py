#!/usr/bin/env python3
"""Verify the STM32F407VET6 base-project layout and build outputs."""

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
    cmsis = firmware / "Libraries" / "CMSIS"
    device = cmsis / "Device" / "ST" / "STM32F4xx"
    core = cmsis / "Core" / "Include"
    project_source = firmware / "src"

    for directory in ("user", "app", "driver", "bsp", "common"):
        require((project_source / directory).is_dir(), "Missing src directory: " + directory)

    required_files = [
        core / "core_cm4.h",
        core / "cmsis_version.h",
        core / "cmsis_compiler.h",
        core / "cmsis_gcc.h",
        core / "mpu_armv7.h",
        device / "Include" / "stm32f4xx.h",
        device / "Include" / "stm32f407xx.h",
        device / "Include" / "system_stm32f4xx.h",
        device / "Source" / "Templates" / "system_stm32f4xx.c",
        device / "Source" / "Templates" / "gcc" / "startup_stm32f407xx.s",
        firmware / "Start" / "STM32F407VETX_FLASH.ld",
        project_source / "user" / "main.c",
        project_source / "user" / "main.h",
        project_source / "user" / "stm32f4xx_it.c",
        project_source / "user" / "stm32f4xx_it.h",
        project_source / "common" / "com_time.c",
        project_source / "common" / "com_time.h",
    ]
    for path in required_files:
        require(path.is_file(), "Missing required file: " + str(path))

    require(
        not (firmware / "Libraries" / "STM32F10x_StdPeriph_Lib").exists(),
        "Legacy STM32F10x vendor library still exists",
    )
    require(
        not (firmware / "Start" / "STM32F103xx_FLASH.ld").exists(),
        "Legacy STM32F103 linker script still exists",
    )
    require(
        not (project_source / "user" / "stm32f10x_it.c").exists(),
        "Legacy STM32F10x interrupt file still exists",
    )

    linker = (firmware / "Start" / "STM32F407VETX_FLASH.ld").read_text(encoding="utf-8")
    require("LENGTH = 512K" in linker, "Flash length is not 512K")
    require("LENGTH = 128K" in linker, "SRAM length is not 128K")
    require("LENGTH = 64K" in linker, "CCMRAM length is not 64K")

    commands = json.loads((build / "compile_commands.json").read_text(encoding="utf-8"))

    expected_units = {
        "main.c": project_source / "user" / "main.c",
        "stm32f4xx_it.c": project_source / "user" / "stm32f4xx_it.c",
        "com_time.c": project_source / "common" / "com_time.c",
        "system_stm32f4xx.c": device / "Source" / "Templates" / "system_stm32f4xx.c",
        "startup_stm32f407xx.s": device / "Source" / "Templates" / "gcc" / "startup_stm32f407xx.s",
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
        "-DSTM32F407xx",
    ):
        require(token in all_commands, "Missing compiler target option: " + token)

    require("STM32F10" not in all_commands, "Build commands still reference STM32F10x")

    project = "stm32f407_template"
    for suffix in (".elf", ".bin", ".hex", ".map"):
        artifact = build / (project + suffix)
        require(
            artifact.is_file() and artifact.stat().st_size > 0,
            "Missing build artifact: " + str(artifact),
        )

    print(
        "PASS: STM32F407VET6 CMSIS base, lowercase source layout, Cortex-M4F flags, "
        "startup/system units, memory layout and firmware artifacts"
    )


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError) as exc:
        raise SystemExit("F407 base verification failed: " + str(exc)) from exc
