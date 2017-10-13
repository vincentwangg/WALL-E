# CMake generated Testfile for 
# Source directory: /home/local/ADS/oakley/projects/walle/OpenCV/modules/superres
# Build directory: /home/local/ADS/oakley/projects/walle/OpenCV/build/modules/superres
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_superres "/home/local/ADS/oakley/projects/walle/OpenCV/build/bin/opencv_test_superres" "--gtest_output=xml:opencv_test_superres.xml")
set_tests_properties(opencv_test_superres PROPERTIES  LABELS "Main;opencv_superres;Accuracy" WORKING_DIRECTORY "/home/local/ADS/oakley/projects/walle/OpenCV/build/test-reports/accuracy")
add_test(opencv_perf_superres "/home/local/ADS/oakley/projects/walle/OpenCV/build/bin/opencv_perf_superres" "--gtest_output=xml:opencv_perf_superres.xml")
set_tests_properties(opencv_perf_superres PROPERTIES  LABELS "Main;opencv_superres;Performance" WORKING_DIRECTORY "/home/local/ADS/oakley/projects/walle/OpenCV/build/test-reports/performance")
add_test(opencv_sanity_superres "/home/local/ADS/oakley/projects/walle/OpenCV/build/bin/opencv_perf_superres" "--gtest_output=xml:opencv_perf_superres.xml" "--perf_min_samples=1" "--perf_force_samples=1" "--perf_verify_sanity")
set_tests_properties(opencv_sanity_superres PROPERTIES  LABELS "Main;opencv_superres;Sanity" WORKING_DIRECTORY "/home/local/ADS/oakley/projects/walle/OpenCV/build/test-reports/sanity")
