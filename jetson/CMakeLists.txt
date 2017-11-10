cmake_minimum_required (VERSION 2.8)

project (hello)

find_package(OpenCV REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(cv_main main.cpp)

target_link_libraries(cv_main ${OpenCV_LIBS})
