# STM32F407VET6 startup glue for the legacy Standard Peripheral Library template.
# Inputs from parent CMakeLists.txt:
#   CMSIS_CORE   -> legacy CMSIS Cortex-M4 headers
#   CMSIS_DEVICE -> legacy STM32F4 CMSIS device component

set(CMSIS_DEVICE_INCLUDE "${CMSIS_DEVICE}/Include")
set(SYSTEM_SOURCE "${CMAKE_CURRENT_LIST_DIR}/system_stm32f4xx.c")
set(STARTUP_FILE "${CMAKE_CURRENT_LIST_DIR}/startup_stm32f407xx.s")

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
