# Gazebo Harmonic

Onyx targets Gazebo Harmonic (Gazebo Sim 8) and ROS 2 Humble. Source your
working Harmonic-compatible ROS-Gazebo environment, then launch from the
repository root:

```bash
./run
```

This starts Gazebo, Onyx, the sensor and command bridges, and RViz. In a
second terminal, source the same ROS 2 and Harmonic `ros_gz` environment
used to start the simulation, then source this workspace and run:

```bash
source /opt/ros/humble/setup.bash
source /path/to/your/ros_gz_harmonic_overlay/install/setup.bash
source /path/to/onyx/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Drive with the keys shown by teleop. The turret accepts yaw and pitch targets
in radians on `/turret/yaw/cmd` and `/turret/pitch/cmd`.
