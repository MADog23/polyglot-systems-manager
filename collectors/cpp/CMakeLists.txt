cmake_minimum_required(VERSION 3.16)
project(metrics_collector)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories
include_directories(include)
include_directories(external/httplib)

# Platform-specific source files
if (WIN32)
    set(PLATFORM_SOURCES
        src/cpu_usage_windows.cpp
        src/memory_usage_windows.cpp
        src/disk_usage_windows.cpp
        src/uptime_windows.cpp
    )
else()
    set(PLATFORM_SOURCES
        src/cpu_usage_linux.cpp
        src/memory_usage_linux.cpp
        src/disk_usage_linux.cpp
        src/uptime_linux.cpp
    )
endif()

# Main executable
add_executable(metrics-collector
    src/main.cpp
    src/metrics.cpp
    ${PLATFORM_SOURCES}
)

# Windows needs pdh.lib for CPU sampling
if (WIN32)
    target_link_libraries(metrics-collector pdh)
endif()
