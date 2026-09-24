cmake_minimum_required(VERSION 3.22)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

set(CMAKE_PROJECT_NAME stm32f407_std_template)
project(${CMAKE_PROJECT_NAME} LANGUAGES C ASM)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(MCU_FLAGS
    -mcpu=cortex-m4
    -mthumb
    -mfpu=fpv4-sp-d16
    -mfloat-abi=hard
)

set(STDPERIPH_ROOT "${CMAKE_SOURCE_DIR}/Libraries/STM32F4xx_StdPeriph_Lib")
set(STDPERIPH_DRIVER "${STDPERIPH_ROOT}/Libraries/STM32F4xx_StdPeriph_Driver")
set(CMSIS_ROOT "${STDPERIPH_ROOT}/Libraries/CMSIS")
set(CMSIS_CORE "${CMSIS_ROOT}/Include")
set(CMSIS_DEVICE "${CMSIS_ROOT}/Device/ST/STM32F4xx")

if(NOT EXISTS "${STDPERIPH_DRIVER}/src/stm32f4xx_gpio.c")
    message(FATAL_ERROR
        "STM32F4xx Standard Peripheral Library is incomplete: stm32f4xx_gpio.c is missing. "
        "Restore firmware/Libraries/STM32F4xx_StdPeriph_Lib from the repository."
    )
endif()

if(NOT EXISTS "${CMSIS_DEVICE}/Include/stm32f4xx.h")
    message(FATAL_ERROR
        "STM32F4 legacy CMSIS device header is missing. "
        "Restore firmware/Libraries/STM32F4xx_StdPeriph_Lib from the repository."
    )
endif()

include("${CMAKE_CURRENT_SOURCE_DIR}/Start/startup.cmake")

file(GLOB STDPERIPH_SOURCES CONFIGURE_DEPENDS
    "${STDPERIPH_DRIVER}/src/*.c"
)

file(GLOB_RECURSE PROJECT_SOURCES CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/src/user/*.c"
    "${CMAKE_SOURCE_DIR}/src/app/*.c"
    "${CMAKE_SOURCE_DIR}/src/driver/*.c"
    "${CMAKE_SOURCE_DIR}/src/bsp/*.c"
    "${CMAKE_SOURCE_DIR}/src/common/*.c"
)

add_library(stm32_stdperiph STATIC
    ${STDPERIPH_SOURCES}
)

target_include_directories(stm32_stdperiph PUBLIC
    "${CMAKE_SOURCE_DIR}/src/user"
    "${STDPERIPH_DRIVER}/inc"
    ${STM32_STARTUP_INCLUDE_DIRS}
)

target_compile_definitions(stm32_stdperiph PUBLIC
    STM32F40_41xxx
    USE_STDPERIPH_DRIVER
)

target_compile_options(stm32_stdperiph PRIVATE
    ${MCU_FLAGS}
    -Wall
    -ffunction-sections
    -fdata-sections
)

add_executable(${CMAKE_PROJECT_NAME}
    ${PROJECT_SOURCES}
    ${STM32_STARTUP_SOURCES}
)

set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES SUFFIX ".elf")

target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE
    src/user
    src/app
    src/driver
    src/bsp
    src/common
)

target_compile_options(${CMAKE_PROJECT_NAME} PRIVATE
    ${MCU_FLAGS}
    -Wall
    -Wextra
    -ffunction-sections
    -fdata-sections
)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_options(${CMAKE_PROJECT_NAME} PRIVATE -O0 -g3)
    target_compile_options(stm32_stdperiph PRIVATE -O0 -g3)
else()
    target_compile_options(${CMAKE_PROJECT_NAME} PRIVATE -Os)
    target_compile_options(stm32_stdperiph PRIVATE -Os)
endif()

target_link_options(${CMAKE_PROJECT_NAME} PRIVATE
    ${MCU_FLAGS}
    "-T${CMAKE_SOURCE_DIR}/Start/STM32F407VETX_FLASH.ld"
    --specs=nano.specs
    --specs=nosys.specs
    -Wl,--gc-sections
    "-Wl,-Map=${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}.map"
    -Wl,--print-memory-usage
)

target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE
    stm32_stdperiph
    m
)

add_custom_command(TARGET ${CMAKE_PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O ihex
        $<TARGET_FILE:${CMAKE_PROJECT_NAME}>
        "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}.hex"
    COMMAND ${CMAKE_OBJCOPY} -O binary
        $<TARGET_FILE:${CMAKE_PROJECT_NAME}>
        "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}.bin"
    COMMAND ${CMAKE_SIZE}
        $<TARGET_FILE:${CMAKE_PROJECT_NAME}>
    COMMENT "Generating HEX/BIN and printing firmware size"
)
