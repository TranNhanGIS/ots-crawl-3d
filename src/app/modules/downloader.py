"""
ModelDownloader Class

This module defines the ModelDownloader class, which is used to download 3D model files (OBJ) and texture files (such as images) from URLs specified in a cleaned data file. The downloaded files are saved to designated directories for models and textures.

Key Features:
- Downloads 3D model files (OBJ) and texture files (e.g., JPG, PNG).
- Saves the downloaded files to specified directories.
- Handles download errors gracefully with logging.

Usage:
    downloader = ModelDownloader(input_cleaner_file="cleaned_data.json", output_obj_dir="models/", output_texture_dir="textures/")
    downloader.process()

Dependencies:
- os
- requests
- json
- loguru
"""

import os
import requests
import json
from loguru import logger


class ModelDownloader:
    """
    A class for downloading 3D model files (OBJ) and texture files (e.g., JPG, PNG) from URLs.

    Attributes:
        input_cleaner_file (str): Path to the input cleaned data file containing model and texture URLs.
        output_obj_dir (str): Directory where downloaded 3D model files (OBJ) will be saved.
        output_texture_dir (str): Directory where downloaded texture files (e.g., JPG, PNG) will be saved.
        cleaner_file (file object): File object for the input cleaned data file.
        cleaner_data (list): List of cleaned data containing URLs for model and texture files.
    """

    def __init__(self, input_cleaner_file: str, output_obj_dir: str, output_texture_dir: str):
        """
        Initializes the ModelDownloader with the input file containing cleaned data and output directories for models and textures.

        Args:
            input_cleaner_file (str): Path to the input cleaned data file.
            output_obj_dir (str): Directory for saving downloaded model files.
            output_texture_dir (str): Directory for saving downloaded texture files.
        """
        self.input_cleaner_file = input_cleaner_file
        self.output_obj_dir = output_obj_dir
        self.output_texture_dir = output_texture_dir

        self.cleaner_file = open(self.input_cleaner_file, "r", encoding="utf-8")
        self.cleaner_data = json.load(self.cleaner_file)

    @staticmethod
    def download_file(url: str, file_name: str, output_dir: str) -> None:
        """
        Downloads a file from a given URL and saves it to the specified directory with the provided file name.

        Args:
            url (str): The URL to download the file from.
            file_name (str): The name to save the file as.
            output_dir (str): The directory where the file will be saved.

        Raises:
            requests.exceptions.RequestException: If the download fails.
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            file_path = os.path.join(output_dir, file_name)

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            logger.success(f"Downloaded: {file_name}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download: {url}; Exception: {e}")

    def process(self):
        """
        Processes the cleaned data, downloading the model and texture files for each entry.

        This method iterates through the cleaned data and downloads the model and texture files specified in each row.
        The files are saved to their respective directories: one for models and one for textures.
        """
        for row in self.cleaner_data:
            model = row["model"]
            self.download_file(model["objUrl"], model["objName"], self.output_obj_dir)
            self.download_file(model["textureUrl"], model["textureName"], self.output_texture_dir)
