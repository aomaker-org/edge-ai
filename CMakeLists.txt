cmake_minimum_required(VERSION 3.20)
project(edge_ai LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(FATAL_ERROR "In-source builds are forbidden. Please build out-of-tree in build/")
endif()

if(MSVC)
    add_compile_options(/W4 /utf-8 /MP)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS -DNOMINMAX -DWIN32_LEAN_AND_MEAN)
endif()

add_library(edge_ai_core STATIC
    infra/win11/edge_ai_stub.cpp
)
target_include_directories(edge_ai_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_executable(edge_ai_cli
    infra/win11/main.cpp
)
target_link_libraries(edge_ai_cli PRIVATE edge_ai_core)

find_package(OpenVINO QUIET)
if(OpenVINO_FOUND)
    message(STATUS "[+] OpenVINO found. Enabling OpenVINO acceleration backend.")
    target_compile_definitions(edge_ai_core PUBLIC EDGE_AI_ENABLE_OPENVINO)
    target_link_libraries(edge_ai_core PUBLIC openvino::runtime)
else()
    message(STATUS "[i] OpenVINO not found. OpenVINO backend disabled.")
endif()

install(TARGETS edge_ai_cli edge_ai_core
    RUNTIME DESTINATION bin
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
)
