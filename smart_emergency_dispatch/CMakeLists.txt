cmake_minimum_required(VERSION 3.10)
project(SmartEmergencyDispatch VERSION 0.6.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(MSVC)
    add_compile_options(/W4 /O2)
else()
    add_compile_options(-Wall -Wextra -pedantic -O3)
endif()

include_directories(include)

file(GLOB_RECURSE SRC_FILES "src/*.cpp")
list(FILTER SRC_FILES EXCLUDE REGEX "src/main.cpp")

add_library(dispatch_core STATIC ${SRC_FILES})

# Main Interactive CLI
add_executable(dispatch_sim src/main.cpp)
target_link_libraries(dispatch_sim PRIVATE dispatch_core)

# Tests
enable_testing()
add_executable(test_algorithms tests/test_algorithms.cpp)
target_link_libraries(test_algorithms PRIVATE dispatch_core)
add_test(NAME TestAlgorithms COMMAND test_algorithms)

add_executable(test_dispatch tests/test_dispatch.cpp)
target_link_libraries(test_dispatch PRIVATE dispatch_core)
add_test(NAME TestDispatch COMMAND test_dispatch)
