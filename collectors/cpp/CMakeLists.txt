cmake_minimum_required(VERSION 3.10)
project(metrics_collector)

set(CMAKE_CXX_STANDARD 17)

include_directories(include)

add_executable(metrics-collector
    src/main.cpp
    src/metrics.cpp
)
