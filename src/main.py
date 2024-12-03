"""
Main execution script for the 3D model pipeline.

This script automates the process of crawling, cleaning, downloading, and converting 3D models and textures. The pipeline involves the following steps:

1. **Crawl Data**: Extracts building information from a grid by running the `BuildingCrawler`.
2. **Clean Data**: Processes the raw data collected by the crawler, cleaning and organizing it using the `DataCleaner`.
3. **Download Models and Textures**: Downloads 3D models and textures based on the cleaned data using the `ModelDownloader`.
4. **Convert Models**: Converts the downloaded models into a desired format (e.g., GLB, FBX) using Blender, by invoking a script through the `blender_runner`.

Each step is executed sequentially, with logging at each stage to track progress and handle errors.

Dependencies:
- asyncio
- loguru
- datetime
- src.app.modules.crawler.BuildingCrawler
- src.app.modules.downloader.ModelDownloader
- src.app.modules.cleaner.DataCleaner
- src.app.utils.blender_utils.install_module_for_blender
- src.app.utils.blender_utils.blender_runner
"""

import os
import asyncio
from loguru import logger
from datetime import datetime
from src.app.modules.crawler import BuildingCrawler
from src.app.modules.downloader import ModelDownloader
from src.app.modules.cleaner import DataCleaner
from src.app.utils.blender_utils import install_module_for_blender, blender_runner

# Directories for input and output data
crawler_dir = "data/output/crawler"
cleaner_dir = "data/output/cleaner"
downloader_dir = "D:/Tools/ots-crawl-3d/data/output/downloader"
obj_dir = "data/output/downloader/obj"
texture_dir = "data/output/downloader/texture"

input_grid_file = "data/input/grid_lv3.geojson"
crawler_file = os.path.join(crawler_dir, "data.csv")
cleaner_csv_file = os.path.join(cleaner_dir, "data.csv")
cleaner_json_file = os.path.join(cleaner_dir, "data.json")


def main():
    """
    Main function to execute the full pipeline of crawling, cleaning, downloading, and converting 3D models and textures.

    The function runs the following steps:
    1. Executes the crawler to extract building data.
    2. Cleans the crawled data for further processing.
    3. Downloads the models and textures based on the cleaned data.
    4. Converts the downloaded models into the desired format (GLB/FBX).

    Each step logs progress and handles exceptions.
    """
    logger.info("-----------------------------------")
    logger.info("** Started at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Step 1: Run the crawler to extract building data from the grid
    logger.info("Step 1: Run the crawler...")
    crawler = BuildingCrawler(
        input_grid_file=input_grid_file, output_crawler_file=crawler_file, num_pages=3
    )
    try:
        asyncio.run(crawler.run())
        logger.info("Crawler completed successfully.")
    except Exception as e:
        logger.error(f"Error in crawling: {e}")
        return

    # Step 2: Clean the crawled data to organize and prepare it for the next steps
    logger.info("Step 2: Clean the crawled data...")
    cleaner = DataCleaner(
        input_crawler_file=crawler_file,
        output_cleaner_csv_file=cleaner_csv_file,
        output_cleaner_json_file=cleaner_json_file,
    )
    try:
        cleaner.run()
        logger.info("Data cleaning completed successfully.")
    except Exception as e:
        logger.error(f"Error in data cleaning: {e}")
        return

    # Step 3: Download models and textures based on the cleaned data
    logger.info("Step 3: Downloading models and textures...")
    downloader = ModelDownloader(
        input_cleaner_file=cleaner_json_file,
        output_obj_dir=obj_dir,
        output_texture_dir=texture_dir,
    )
    try:
        downloader.process()
        logger.info("Model and texture download completed successfully.")
    except Exception as e:
        logger.error(f"Error in downloading models and textures: {e}")
        return

    # Step 4: Convert the downloaded models to the desired format (GLB/FBX) using Blender
    logger.info("Step 4: Convert models to the desired format...")
    install_module_for_blender("loguru")  # Install necessary Blender modules
    try:
        blender_runner("src/app/modules/converter.py")  # Run Blender conversion script
        logger.info("Model conversion completed successfully.")
    except Exception as e:
        logger.error(f"Error in model conversion: {e}")
        return

    logger.info("** Finished at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("-----------------------------------")


if __name__ == "__main__":
    # Ensure necessary directories exist
    os.makedirs(crawler_dir, exist_ok=True)
    os.makedirs(cleaner_dir, exist_ok=True)
    os.makedirs(downloader_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    os.makedirs(texture_dir, exist_ok=True)

    # Start the main process
    main()
