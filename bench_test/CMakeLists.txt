cmake_minimum_required(VERSION 3.23)
set(CMAKE_VERBOSE_MAKEFILE on)

project(main LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(main)
add_executable(main_bench)
if(APPLE)
	include_directories(/opt/homebrew/include /opt/homebrew/include/libelf)
	cmake_path(GET PROJECT_SOURCE_DIR PARENT_PATH PARENT_DIR)
	set(BM_PATH_HDR "${PROJECT_SOURCE_DIR}/../bm_macos/include/")
	set(BM_PATH_LIB "${PROJECT_SOURCE_DIR}/../bm_macos/build/src")

	include_directories(SYSTEM ${BM_PATH_HDR})
	target_link_directories(main_bench PRIVATE ${BM_PATH_LIB})
	target_link_libraries(main_bench benchmark pthread)

elseif(UNIX AND NOT APPLE)
    set(BM_PATH_HDR "${PROJECT_SOURCE_DIR}/../bm_linux/include/")
    set(BM_PATH_LIB "${PROJECT_SOURCE_DIR}/../bm_linux/build/src")

    include_directories(SYSTEM ${BM_PATH_HDR})
    target_link_directories(main_bench PRIVATE ${BM_PATH_LIB})
    target_link_libraries(main_bench benchmark pthread)

endif()

target_sources(main
	PRIVATE
	 	func.cpp
		main.cpp
	PUBLIC
		FILE_SET HEADERS
		BASE_DIRS
		.
		FILES
		main.hpp
)

target_sources(main_bench
	PRIVATE
		func.cpp
		main_bench.cpp
	PUBLIC
		FILE_SET HEADERS
		BASE_DIRS
		.
		FILES
		main.hpp
)
