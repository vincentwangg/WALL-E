# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


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

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/local/ADS/oakley/projects/walle/OpenCV

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/local/ADS/oakley/projects/walle/OpenCV/build

# Include any dependencies generated for this target.
include samples/cpp/CMakeFiles/tutorial_file_input_output.dir/depend.make

# Include the progress variables for this target.
include samples/cpp/CMakeFiles/tutorial_file_input_output.dir/progress.make

# Include the compile flags for this target's objects.
include samples/cpp/CMakeFiles/tutorial_file_input_output.dir/flags.make

samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o: samples/cpp/CMakeFiles/tutorial_file_input_output.dir/flags.make
samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o: ../samples/cpp/tutorial_code/core/file_input_output/file_input_output.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/local/ADS/oakley/projects/walle/OpenCV/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o"
	cd /home/local/ADS/oakley/projects/walle/OpenCV/build/samples/cpp && /usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o -c /home/local/ADS/oakley/projects/walle/OpenCV/samples/cpp/tutorial_code/core/file_input_output/file_input_output.cpp

samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.i"
	cd /home/local/ADS/oakley/projects/walle/OpenCV/build/samples/cpp && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/local/ADS/oakley/projects/walle/OpenCV/samples/cpp/tutorial_code/core/file_input_output/file_input_output.cpp > CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.i

samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.s"
	cd /home/local/ADS/oakley/projects/walle/OpenCV/build/samples/cpp && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/local/ADS/oakley/projects/walle/OpenCV/samples/cpp/tutorial_code/core/file_input_output/file_input_output.cpp -o CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.s

samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o.requires:

.PHONY : samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o.requires

samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o.provides: samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o.requires
	$(MAKE) -f samples/cpp/CMakeFiles/tutorial_file_input_output.dir/build.make samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o.provides.build
.PHONY : samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o.provides

samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o.provides.build: samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o


# Object files for target tutorial_file_input_output
tutorial_file_input_output_OBJECTS = \
"CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o"

# External object files for target tutorial_file_input_output
tutorial_file_input_output_EXTERNAL_OBJECTS =

bin/cpp-tutorial-file_input_output: samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o
bin/cpp-tutorial-file_input_output: samples/cpp/CMakeFiles/tutorial_file_input_output.dir/build.make
bin/cpp-tutorial-file_input_output: /usr/lib/x86_64-linux-gnu/libGLU.so
bin/cpp-tutorial-file_input_output: /usr/lib/x86_64-linux-gnu/libGL.so
bin/cpp-tutorial-file_input_output: /usr/lib/x86_64-linux-gnu/libtbb.so
bin/cpp-tutorial-file_input_output: 3rdparty/ippicv/ippicv_lnx/lib/intel64/libippicv.a
bin/cpp-tutorial-file_input_output: lib/libopencv_shape.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_stitching.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_superres.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_videostab.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_viz.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_objdetect.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_photo.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_calib3d.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_features2d.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_flann.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_highgui.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_ml.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_videoio.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_imgcodecs.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_video.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_imgproc.so.3.2.0
bin/cpp-tutorial-file_input_output: lib/libopencv_core.so.3.2.0
bin/cpp-tutorial-file_input_output: /usr/lib/x86_64-linux-gnu/libGLU.so
bin/cpp-tutorial-file_input_output: /usr/lib/x86_64-linux-gnu/libGL.so
bin/cpp-tutorial-file_input_output: samples/cpp/CMakeFiles/tutorial_file_input_output.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/local/ADS/oakley/projects/walle/OpenCV/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/cpp-tutorial-file_input_output"
	cd /home/local/ADS/oakley/projects/walle/OpenCV/build/samples/cpp && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tutorial_file_input_output.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
samples/cpp/CMakeFiles/tutorial_file_input_output.dir/build: bin/cpp-tutorial-file_input_output

.PHONY : samples/cpp/CMakeFiles/tutorial_file_input_output.dir/build

samples/cpp/CMakeFiles/tutorial_file_input_output.dir/requires: samples/cpp/CMakeFiles/tutorial_file_input_output.dir/tutorial_code/core/file_input_output/file_input_output.cpp.o.requires

.PHONY : samples/cpp/CMakeFiles/tutorial_file_input_output.dir/requires

samples/cpp/CMakeFiles/tutorial_file_input_output.dir/clean:
	cd /home/local/ADS/oakley/projects/walle/OpenCV/build/samples/cpp && $(CMAKE_COMMAND) -P CMakeFiles/tutorial_file_input_output.dir/cmake_clean.cmake
.PHONY : samples/cpp/CMakeFiles/tutorial_file_input_output.dir/clean

samples/cpp/CMakeFiles/tutorial_file_input_output.dir/depend:
	cd /home/local/ADS/oakley/projects/walle/OpenCV/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/local/ADS/oakley/projects/walle/OpenCV /home/local/ADS/oakley/projects/walle/OpenCV/samples/cpp /home/local/ADS/oakley/projects/walle/OpenCV/build /home/local/ADS/oakley/projects/walle/OpenCV/build/samples/cpp /home/local/ADS/oakley/projects/walle/OpenCV/build/samples/cpp/CMakeFiles/tutorial_file_input_output.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : samples/cpp/CMakeFiles/tutorial_file_input_output.dir/depend

