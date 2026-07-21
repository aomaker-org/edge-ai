cmake_minimum_required(VERSION 3.18)
project(pixel6a_infer_cli CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(COMMON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../common)

include_directories(
    ${COMMON_DIR}/include
)

add_executable(pixel6a_infer_cli
    main.cpp
    ${COMMON_DIR}/src/ai_inference_engine.cpp
    ${COMMON_DIR}/src/adb_rpc_protocol.cpp
)

target_compile_definitions(pixel6a_infer_cli PRIVATE PIXEL_DEVICE_6A=1)
