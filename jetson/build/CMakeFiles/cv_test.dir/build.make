# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ubuntu/src/jetson

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ubuntu/src/jetson/build

# Include any dependencies generated for this target.
include CMakeFiles/cv_test.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/cv_test.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/cv_test.dir/flags.make

CMakeFiles/cv_test.dir/test.cpp.o: CMakeFiles/cv_test.dir/flags.make
CMakeFiles/cv_test.dir/test.cpp.o: ../test.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/ubuntu/src/jetson/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/cv_test.dir/test.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/cv_test.dir/test.cpp.o -c /home/ubuntu/src/jetson/test.cpp

CMakeFiles/cv_test.dir/test.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cv_test.dir/test.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/ubuntu/src/jetson/test.cpp > CMakeFiles/cv_test.dir/test.cpp.i

CMakeFiles/cv_test.dir/test.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cv_test.dir/test.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/ubuntu/src/jetson/test.cpp -o CMakeFiles/cv_test.dir/test.cpp.s

CMakeFiles/cv_test.dir/test.cpp.o.requires:
.PHONY : CMakeFiles/cv_test.dir/test.cpp.o.requires

CMakeFiles/cv_test.dir/test.cpp.o.provides: CMakeFiles/cv_test.dir/test.cpp.o.requires
	$(MAKE) -f CMakeFiles/cv_test.dir/build.make CMakeFiles/cv_test.dir/test.cpp.o.provides.build
.PHONY : CMakeFiles/cv_test.dir/test.cpp.o.provides

CMakeFiles/cv_test.dir/test.cpp.o.provides.build: CMakeFiles/cv_test.dir/test.cpp.o

# Object files for target cv_test
cv_test_OBJECTS = \
"CMakeFiles/cv_test.dir/test.cpp.o"

# External object files for target cv_test
cv_test_EXTERNAL_OBJECTS =

cv_test: CMakeFiles/cv_test.dir/test.cpp.o
cv_test: CMakeFiles/cv_test.dir/build.make
cv_test: /usr/lib/libopencv_vstab.so.2.4.8
cv_test: /usr/lib/libopencv_tegra.so.2.4.8
cv_test: /usr/lib/libopencv_imuvstab.so.2.4.8
cv_test: /usr/lib/libopencv_facedetect.so.2.4.8
cv_test: /usr/lib/libopencv_videostab.so.2.4.8
cv_test: /usr/lib/libopencv_video.so.2.4.8
cv_test: /usr/lib/libopencv_ts.a
cv_test: /usr/lib/libopencv_superres.so.2.4.8
cv_test: /usr/lib/libopencv_stitching.so.2.4.8
cv_test: /usr/lib/libopencv_softcascade.so.2.4.8
cv_test: /usr/lib/libopencv_photo.so.2.4.8
cv_test: /usr/lib/libopencv_objdetect.so.2.4.8
cv_test: /usr/lib/libopencv_ml.so.2.4.8
cv_test: /usr/lib/libopencv_legacy.so.2.4.8
cv_test: /usr/lib/libopencv_imgproc.so.2.4.8
cv_test: /usr/lib/libopencv_highgui.so.2.4.8
cv_test: /usr/lib/libopencv_gpu.so.2.4.8
cv_test: /usr/lib/libopencv_flann.so.2.4.8
cv_test: /usr/lib/libopencv_features2d.so.2.4.8
cv_test: /usr/lib/libopencv_core.so.2.4.8
cv_test: /usr/lib/libopencv_contrib.so.2.4.8
cv_test: /usr/lib/libopencv_calib3d.so.2.4.8
cv_test: /usr/local/cuda-6.0/lib/libcudart.so
cv_test: /usr/local/cuda-6.0/lib/libnppc.so
cv_test: /usr/local/cuda-6.0/lib/libnppi.so
cv_test: /usr/local/cuda-6.0/lib/libnpps.so
cv_test: /usr/local/cuda-6.0/lib/libcufft.so
cv_test: /usr/lib/libopencv_photo.so.2.4.8
cv_test: /usr/lib/libopencv_legacy.so.2.4.8
cv_test: /usr/lib/libopencv_video.so.2.4.8
cv_test: /usr/lib/libopencv_objdetect.so.2.4.8
cv_test: /usr/lib/libopencv_ml.so.2.4.8
cv_test: /usr/lib/libopencv_calib3d.so.2.4.8
cv_test: /usr/lib/libopencv_features2d.so.2.4.8
cv_test: /usr/lib/libopencv_highgui.so.2.4.8
cv_test: /usr/lib/libopencv_imgproc.so.2.4.8
cv_test: /usr/lib/libopencv_flann.so.2.4.8
cv_test: /usr/lib/libopencv_core.so.2.4.8
cv_test: CMakeFiles/cv_test.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable cv_test"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cv_test.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/cv_test.dir/build: cv_test
.PHONY : CMakeFiles/cv_test.dir/build

CMakeFiles/cv_test.dir/requires: CMakeFiles/cv_test.dir/test.cpp.o.requires
.PHONY : CMakeFiles/cv_test.dir/requires

CMakeFiles/cv_test.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/cv_test.dir/cmake_clean.cmake
.PHONY : CMakeFiles/cv_test.dir/clean

CMakeFiles/cv_test.dir/depend:
	cd /home/ubuntu/src/jetson/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ubuntu/src/jetson /home/ubuntu/src/jetson /home/ubuntu/src/jetson/build /home/ubuntu/src/jetson/build /home/ubuntu/src/jetson/build/CMakeFiles/cv_test.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/cv_test.dir/depend

