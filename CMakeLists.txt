cmake_minimum_required(VERSION 3.20)
project(GodotCppTemplate)

set(EXTENSION_NAME "myextension" CACHE STRING "Name of the GDExtension library")

# Map CMAKE_BUILD_TYPE to GODOTCPP_TARGET if not explicitly set
if(NOT GODOTCPP_TARGET)
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
        set(GODOTCPP_TARGET "template_release" CACHE STRING "")
    else()
        set(GODOTCPP_TARGET "template_debug" CACHE STRING "")
    endif()
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Use ccache/sccache if available (speeds up local rebuilds)
if(NOT CMAKE_C_COMPILER_LAUNCHER)
    find_program(CCACHE_PROGRAM ccache sccache)
    if(CCACHE_PROGRAM)
        set(CMAKE_C_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
        set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
    endif()
endif()

if(APPLE AND NOT CMAKE_SYSTEM_NAME STREQUAL "iOS")
    set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64" CACHE STRING "macOS architectures")
endif()

set(BUILD_TESTS OFF CACHE BOOL "Build unit tests")

add_subdirectory(third_party/godot-cpp)
add_subdirectory(cpp)

if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()