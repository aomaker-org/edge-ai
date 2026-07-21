cmake_minimum_required(VERSION 3.18)
project(pixel10_infer_cli CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(COMMON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../common)

include_directories(
    ${COMMON_DIR}/include
)

add_executable(pixel10_infer_cli
    main.cpp
    ${COMMON_DIR}/src/ai_inference_engine.cpp
    ${COMMON_DIR}/src/adb_rpc_protocol.cpp
)

target_compile_definitions(pixel10_infer_cli PRIVATE PIXEL_DEVICE_10_PRO_XL=1)
