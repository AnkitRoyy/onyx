from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.conditions import UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackagePrefix, FindPackageShare


def generate_launch_description():
    world_file = PathJoinSubstitution([
        FindPackageShare('simulation'), 'worlds', 'navigation_arena.sdf'])
    sim_flags = PythonExpression([
        "'-r -s ' if '", LaunchConfiguration('headless'),
        "' == 'true' else '-r '"])
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={'gz_args': [sim_flags, world_file], 'gz_version': '8'}.items(),
    )
    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare('description'), 'launch', 'description.launch.py'])),
        launch_arguments={'use_sim_time': 'true'}.items(),
    )
    spawn = TimerAction(period=5.0, actions=[Node(
        package='ros_gz_sim', executable='create', output='screen',
        arguments=['-world', 'onyx_arena', '-topic', '/robot_description',
                   '-name', 'onyx'],
    )])
    bridges = Node(
        package='ros_gz_bridge', executable='parameter_bridge', output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/lidar/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/imu/data@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/gps/fix@sensor_msgs/msg/NavSatFix[gz.msgs.NavSat',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/front_cam/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/front_cam/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            '/rear_cam/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/rear_cam/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            '/aiming_cam/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/aiming_cam/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/turret/yaw/cmd@std_msgs/msg/Float64]gz.msgs.Double',
            '/turret/pitch/cmd@std_msgs/msg/Float64]gz.msgs.Double',
            '/arena/contact@ros_gz_interfaces/msg/Contacts[gz.msgs.Contacts',
            '/world/onyx_arena/dynamic_pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
        ],
    )
    manager = Node(
        package='simulation', executable='arena_env', name='arena_env', output='screen',
        parameters=[{
            'use_sim_time': True,
            'seed': ParameterValue(LaunchConfiguration('seed'), value_type=int),
            'min_obstacles': ParameterValue(LaunchConfiguration('min_obstacles'), value_type=int),
            'max_obstacles': ParameterValue(LaunchConfiguration('max_obstacles'), value_type=int),
            'publish_world_tf': ParameterValue(LaunchConfiguration('publish_world_tf'), value_type=bool),
        }],
    )
    rviz = Node(
        package='rviz2', executable='rviz2', output='screen',
        arguments=['-d', PathJoinSubstitution([
            FindPackageShare('simulation'), 'rviz', 'onyx_lidar.rviz'])],
        parameters=[{'use_sim_time': True}],
        condition=UnlessCondition(LaunchConfiguration('headless')),
    )
    gps_visualizer = Node(
        package='simulation', executable='onyx_gps_visualizer', output='screen',
        parameters=[{'use_sim_time': True}],
    )
    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='false'),
        DeclareLaunchArgument('seed', default_value='-1',
            description='-1 for random seed; otherwise repeat the same layout.'),
        DeclareLaunchArgument('min_obstacles', default_value='3',
            description='Minimum active cones on reset, from 0 to 10.'),
        DeclareLaunchArgument('max_obstacles', default_value='10',
            description='Maximum active cones on reset, from 0 to 10.'),
        DeclareLaunchArgument('publish_world_tf', default_value='false',
            description='Publish ground-truth world->odom; disable if localization publishes it.'),
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', [
            FindPackageShare('simulation'), ':',
            PathJoinSubstitution([FindPackagePrefix('description'), 'share']), ':',
            EnvironmentVariable('GZ_SIM_RESOURCE_PATH', default_value='')]),
        description, gazebo, bridges, spawn, manager, gps_visualizer, rviz,
    ])
