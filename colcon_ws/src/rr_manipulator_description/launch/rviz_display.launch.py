import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    # Input Data Files
    xacro_file_name = "rr_manipulator.xacro"
    package_description = "rr_manipulator_description"

    xacro_file = os.path.join(get_package_share_directory(package_description), 'urdf', xacro_file_name)
    doc = xacro.parse(open(xacro_file))

    xacro.process_doc(doc)
    robot_description_config = doc.toxml()

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher_node",
        output="screen",
        emulate_tty=True,
        parameters=[{'use_sim_time': True, 'robot_description': robot_description_config}]
    )

    # Joint State Publisher: publishes the current states(positions, velocities) of the robot's joints
    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_node"
    )

    # RVIZ Configuration
    rviz_file = "rviz_config.rviz"
    rviz_config_dir = os.path.join(get_package_share_directory(package_description), "rviz", rviz_file)

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        name="rviz_node",
        parameters=[{'use_sim_time': True}],
        arguments=['-d', rviz_config_dir]
    )

    # Create and return Launch Description Object
    return LaunchDescription(
        [
            robot_state_publisher_node,
            joint_state_publisher_node,
            rviz_node
        ]
    )
