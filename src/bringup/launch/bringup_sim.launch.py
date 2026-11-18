from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('simulation'),
                'launch',
                'simulation.launch.py',
            ])
        ),
        launch_arguments={
            'headless': LaunchConfiguration('headless'),
            'world_name': LaunchConfiguration('world'),
            'seed': LaunchConfiguration('seed'),
            'min_obstacles': LaunchConfiguration('min_obstacles'),
            'max_obstacles': LaunchConfiguration('max_obstacles'),
            'publish_world_tf': LaunchConfiguration('publish_world_tf'),
        }.items(),
    )

    base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('bringup'),
                'launch',
                'bringup_base.launch.py',
            ])
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'mode': LaunchConfiguration('mode'),
            'train': LaunchConfiguration('train'),
            'policy': LaunchConfiguration('policy'),
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='arena',
            description='Simulation world to load: arena or tekno.',
        ),
        DeclareLaunchArgument(
            'mode',
            default_value='mppi',
            description='Controller selection: mppi, rl, or mppi_rl.',
        ),
        DeclareLaunchArgument(
            'train',
            default_value='false',
            description='Enable RL training mode.',
        ),
        DeclareLaunchArgument(
            'policy',
            default_value='',
            description='Saved policy file for RL evaluation.',
        ),
        DeclareLaunchArgument(
            'headless',
            default_value='false',
            description='Run Gazebo in headless mode.',
        ),
        DeclareLaunchArgument(
            'seed',
            default_value='-1',
            description='Random seed for arena layout (-1 for random).',
        ),
        DeclareLaunchArgument(
            'min_obstacles',
            default_value='3',
            description='Minimum active obstacles on reset.',
        ),
        DeclareLaunchArgument(
            'max_obstacles',
            default_value='10',
            description='Maximum active obstacles on reset.',
        ),
        DeclareLaunchArgument(
            'publish_world_tf',
            default_value='true',
            description='Publish ground-truth world->odom TF.',
        ),
        simulation,
        base,
    ])
