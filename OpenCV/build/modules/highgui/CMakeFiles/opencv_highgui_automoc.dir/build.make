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

# Utility rule file for opencv_highgui_automoc.

# Include the progress variables for this target.
include modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/progress.make

modules/highgui/CMakeFiles/opencv_highgui_automoc:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/local/ADS/oakley/projects/walle/OpenCV/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Automatic moc for target opencv_highgui"
	cd /home/local/ADS/oakley/projects/walle/OpenCV/build/modules/highgui && /usr/bin/cmake -E cmake_autogen /home/local/ADS/oakley/projects/walle/OpenCV/build/modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/ Release

opencv_highgui_automoc: modules/highgui/CMakeFiles/opencv_highgui_automoc
opencv_highgui_automoc: modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/build.make

.PHONY : opencv_highgui_automoc

# Rule to build all files generated by this target.
modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/build: opencv_highgui_automoc

.PHONY : modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/build

modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/clean:
	cd /home/local/ADS/oakley/projects/walle/OpenCV/build/modules/highgui && $(CMAKE_COMMAND) -P CMakeFiles/opencv_highgui_automoc.dir/cmake_clean.cmake
.PHONY : modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/clean

modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/depend:
	cd /home/local/ADS/oakley/projects/walle/OpenCV/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/local/ADS/oakley/projects/walle/OpenCV /home/local/ADS/oakley/projects/walle/OpenCV/modules/highgui /home/local/ADS/oakley/projects/walle/OpenCV/build /home/local/ADS/oakley/projects/walle/OpenCV/build/modules/highgui /home/local/ADS/oakley/projects/walle/OpenCV/build/modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/highgui/CMakeFiles/opencv_highgui_automoc.dir/depend

