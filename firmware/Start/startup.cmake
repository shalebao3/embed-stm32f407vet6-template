# STM32F407VET6 startup and CMSIS entry point.
# Inputs from parent CMakeLists.txt:
#   CMSIS_CORE   -> CMSIS Cortex-M core headers
#   CMSIS_DEVICE -> STM32F4 CMSIS device component
# Outputs:
#   STM32_STARTUP_SOURCES
#   STM32_STARTUP_INCLUDE_DIRS

set(CMSIS_DEVICE_INCLUDE "${CMSIS_DEVICE}/Include")
set(SYSTEM_SOURCE "${CMSIS_DEVICE}/Source/Templates/system_stm32f4xx.c")
set(STARTUP_FILE "${CMSIS_DEVICE}/Source/Templates/gcc/startup_stm32f407xx.s")

set(STM32_STARTUP_SOURCES
    "${SYSTEM_SOURCE}"
    "${STARTUP_FILE}"
)

set(STM32_STARTUP_INCLUDE_DIRS
    "${CMSIS_CORE}"
    "${CMSIS_DEVICE_INCLUDE}"
)

foreach(_startup_source IN LISTS STM32_STARTUP_SOURCES)
    if(NOT EXISTS "${_startup_source}")
        message(FATAL_ERROR "STM32F407 startup file is missing: ${_startup_source}")
    endif()
endforeach()

unset(_startup_source)
