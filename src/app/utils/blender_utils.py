"""
This module provides functions for managing Python packages in the Blender environment and running Blender scripts.

Functions:
1. `is_installed_module`: Checks if a given Python package is installed in the Blender environment.
2. `install_module_for_blender`: Installs a Python package in the Blender environment if it's not already installed.
3. `blender_runner`: Runs a specified Blender Python script in background mode without opening the Blender GUI.
"""

import subprocess
import os
from src.app.config import settings


def is_installed_module(package_name):
    """
    Checks if a Python package is installed in the Blender environment.

    Args:
        package_name (str): The name of the package to check.

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    filenames = os.listdir(settings.blender_exe)

    return any(package_name in filename for filename in filenames)


def install_module_for_blender(package_name):
    """
    Installs a Python package in the Blender environment if it's not already installed.

    Args:
        package_name (str): The name of the package to install.
    """
    if not is_installed_module(package_name):
        subprocess.call(
            ["pip", "install", package_name, "--upgrade", "--target", settings.blender_exe]
        )


def blender_runner(file_name):
    """
    Runs a Blender script in batch mode using the specified file.

    Args:
        file_name (str): The path to the Blender Python script to run.
    """
    subprocess.run(["blender", "-b", "-P", file_name])
