#!/bin/bash
# 这一步把系统的 ROS 库路径加到 Pixi 的环境变量里
export PYTHONPATH=$PYTHONPATH:/opt/ros/noetic/lib/python3/dist-packages
export CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH:/opt/ros/noetic
source /opt/ros/noetic/setup.bash