cmake_minimum_required(VERSION 3.10)
project(metrics_collector)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

set(SOURCES
    src/main.cpp
)

if (WIN32)
    message(STATUS "Building for Windows")
    list(APPEND SOURCES src/cpu_usage_windows.cpp)
else()
    message(STATUS "Building for Linux")
    list(APPEND SOURCES src/cpu_usage_linux.cpp)
endif()

add_executable(metrics-collector ${SOURCES})

if (WIN32)
    target_link_libraries(metrics-collector pdh)
endif()
