import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'simulation'

data_files = [
    ('share/ament_index/resource_index/packages',
     ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'),
     glob('launch/*.launch.py')),
    (os.path.join('share', package_name, 'worlds'),
     glob('worlds/*')),
]

# Install all model files while preserving their directory structure.
for root, dirs, files in os.walk('models'):
    for filename in files:
        source = os.path.join(root, filename)
        destination = os.path.join('share', package_name, root)
        data_files.append((destination, [source]))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ario',
    maintainer_email='ario@todo.todo',
    description='Gazebo worlds and simulation scenario management',
    license='MIT',
    extras_require={'test': ['pytest']},
    entry_points={'console_scripts': []},
)
