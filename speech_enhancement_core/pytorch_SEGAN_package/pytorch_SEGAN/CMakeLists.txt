# CMakeList.txt: pytorch_SEGAN 的 CMake 项目，在此处包括源代码并定义
# 项目特定的逻辑。
#
cmake_minimum_required (VERSION 3.8)

project ("pytorch_SEGAN")
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_PREFIX_PATH "C:/DevelopmentTools/Miniconda3/libtorch/share/cmake/Torch")
include_directories("C:/DevelopmentTools/Miniconda3/libtorch/include")
include_directories("C:/DevelopmentTools/Miniconda3/libtorch/include/torch/csrc/api")
find_package(Torch REQUIRED)

# 将源代码添加到此项目的可执行文件。
add_executable (pytorch_SEGAN "pytorch_SEGAN.cpp" "pytorch_SEGAN.h")


target_link_libraries(pytorch_SEGAN ${TORCH_LIBRARIES})
set_property(TARGET pytorch_SEGAN PROPERTY CXX_STANDARD 11)