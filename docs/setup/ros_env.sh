# ROS 2 shell environment for handheld-robotics-v1.
# Used on the Ubuntu VM and the Raspberry Pi; each line is skipped if that
# machine doesn't have the file, so the same script works on both.
# Install: see docs/setup/README.md

# ROS 2 Jazzy itself
[ -f /opt/ros/jazzy/setup.bash ] && source /opt/ros/jazzy/setup.bash

# micro-ROS agent workspace (VM today, Pi from Phase 2)
[ -f "$HOME/microros_ws/install/local_setup.bash" ] && source "$HOME/microros_ws/install/local_setup.bash"

# Keep this robot's ROS traffic separate; must match on every machine
export ROS_DOMAIN_ID=7
