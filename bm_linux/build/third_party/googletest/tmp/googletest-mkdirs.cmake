# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION ${CMAKE_VERSION}) # this file comes with cmake

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest/src")
  file(MAKE_DIRECTORY "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest/src")
endif()
file(MAKE_DIRECTORY
  "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest/build"
  "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest"
  "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest/tmp"
  "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest/stamp"
  "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest/download"
  "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest/stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest/stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/jng/42cursus/lmao/benchmark/build/third_party/googletest/stamp${cfgdir}") # cfgdir has leading slash
endif()
