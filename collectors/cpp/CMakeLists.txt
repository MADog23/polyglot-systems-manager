cmake_minimum_required(VERSION 3.10)
project(metrics_collector)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

set(SOURCES
    src/main.cpp
)

if (WIN32)
    list(APPEND SOURCES
        src/cpu_usage_windows.cpp
        src/memory_usage_windows.cpp
        src/uptime_windows.cpp
        src/disk_usage_windows.cpp
    )
else()
    list(APPEND SOURCES
        src/cpu_usage_linux.cpp
        src/memory_usage_linux.cpp
        src/uptime_linux.cpp
        src/disk_usage_linux.cpp
    )
endif()


add_executable(metrics-collector ${SOURCES})

if (WIN32)
    target_link_libraries(metrics-collector pdh)
endif()
