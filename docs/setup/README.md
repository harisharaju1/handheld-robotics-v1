# Machine setup

`ros_env.sh` holds the shell settings every ROS machine in this project needs
(ROS 2 Jazzy, the micro-ROS workspace, `ROS_DOMAIN_ID=7`). Each machine keeps
its own `~/.bashrc`; that file isn't in the repo, so this is the record of what
goes in it.

## Install on the Pi (run on the Mac, from the repo folder)

```bash
scp docs/setup/ros_env.sh ubuntu@fetcher.local:~/ros_env.sh
ssh ubuntu@fetcher.local "grep -qxF 'source ~/ros_env.sh' ~/.bashrc || echo 'source ~/ros_env.sh' >> ~/.bashrc"
```

## Install on the Ubuntu VM

Copy `ros_env.sh` into the VM's home folder (shared clipboard, or `scp` from the
VM: `scp harisharaju@<mac-ip>:~/Documents/robotics-projects/handheld-robotics-v1/docs/setup/ros_env.sh ~/`
if Remote Login is on), then in the VM:

```bash
grep -qxF 'source ~/ros_env.sh' ~/.bashrc || echo 'source ~/ros_env.sh' >> ~/.bashrc
```

## Check

Open a new terminal and run:

```bash
echo $ROS_DOMAIN_ID     # 7
ros2 --help | head -1   # ROS is on the path
```

The ROS lines added to `~/.bashrc` by hand earlier can stay; sourcing twice is
harmless. To tidy up, delete them with `nano ~/.bashrc` so `source ~/ros_env.sh`
is the only ROS line.

When a setting changes (new workspace, different domain), edit `ros_env.sh`
here, commit it, and copy it to each machine again.
