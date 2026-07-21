cmake_minimum_required(VERSION 3.22.1)
project("pixel10_native_engine")

set(COMMON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../../../common)

include_directories(
    ${COMMON_DIR}/include
)

add_library(pixel10_native_engine SHARED
    pixel10_native_engine.cpp
    ${COMMON_DIR}/src/ai_inference_engine.cpp
    ${COMMON_DIR}/src/adb_rpc_protocol.cpp
)

find_library(log-lib log)

target_link_libraries(pixel10_native_engine
    ${log-lib}
)
