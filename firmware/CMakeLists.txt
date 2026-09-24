cmake_minimum_required(VERSION 3.22)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

set(CMAKE_PROJECT_NAME stm32f407_template)
project(${CMAKE_PROJECT_NAME} LANGUAGES C ASM)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(MCU_FLAGS
    -mcpu=cortex-m4
    -mthumb
    -mfpu=fpv4-sp-d16
    -mfloat-abi=hard
)

set(CMSIS_ROOT "${CMAKE_SOURCE_DIR}/Libraries/CMSIS")
set(CMSIS_CORE "${CMSIS_ROOT}/Core/Include")
set(CMSIS_DEVICE "${CMSIS_ROOT}/Device/ST/STM32F4xx")

if(NOT EXISTS "${CMSIS_DEVICE}/Include/stm32f407xx.h")
    message(FATAL_ERROR
        "STM32F407 CMSIS device files are incomplete. "
        "Restore firmware/Libraries/CMSIS from the repository."
    )
endif()

include("${CMAKE_CURRENT_SOURCE_DIR}/Start/startup.cmake")

file(GLOB_RECURSE PROJECT_SOURCES CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/src/user/*.c"
    "${CMAKE_SOURCE_DIR}/src/app/*.c"
    "${CMAKE_SOURCE_DIR}/src/driver/*.c"
    "${CMAKE_SOURCE_DIR}/src/bsp/*.c"
    "${CMAKE_SOURCE_DIR}/src/common/*.c"
)

add_executable(${CMAKE_PROJECT_NAME}
    ${PROJECT_SOURCES}
    ${STM32_STARTUP_SOURCES}
)

# CMake's Generic platform does not guarantee an executable suffix.
# Force the firmware ELF name so local builds and CI have a stable artifact contract.
set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES SUFFIX ".elf")

target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE
    src/user
    src/app
    src/driver
    src/bsp
    src/common
    ${STM32_STARTUP_INCLUDE_DIRS}
)

target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE
    STM32F407xx
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
else()
    target_compile_options(${CMAKE_PROJECT_NAME} PRIVATE -Os)
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
