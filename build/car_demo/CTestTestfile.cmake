# CMake generated Testfile for 
# Source directory: /sbel/gazebo-demo/car_demo
# Build directory: /sbel/gazebo-demo/build/car_demo
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(PriusHybridPluginTest "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/sbel/gazebo-demo/build/car_demo/test_results/car_demo/PriusHybridPluginTest.gtest.xml" "--package-name" "car_demo" "--output-file" "/sbel/gazebo-demo/build/car_demo/ament_cmake_gtest/PriusHybridPluginTest.txt" "--command" "/sbel/gazebo-demo/build/car_demo/PriusHybridPluginTest" "--gtest_output=xml:/sbel/gazebo-demo/build/car_demo/test_results/car_demo/PriusHybridPluginTest.gtest.xml")
set_tests_properties(PriusHybridPluginTest PROPERTIES  LABELS "gtest" REQUIRED_FILES "/sbel/gazebo-demo/build/car_demo/PriusHybridPluginTest" TIMEOUT "60" WORKING_DIRECTORY "/sbel/gazebo-demo/build/car_demo" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/sbel/gazebo-demo/car_demo/CMakeLists.txt;87;ament_add_gtest;/sbel/gazebo-demo/car_demo/CMakeLists.txt;0;")
subdirs("gtest")
