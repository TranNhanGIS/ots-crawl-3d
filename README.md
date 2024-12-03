
# 3D Model Crawler Pipeline Project

This project automates the process of crawling, cleaning, downloading, and converting 3D models and textures. It leverages various tools, including Python, Blender, and asyncio, to create a smooth pipeline for handling large amounts of 3D model data. 

## Requirements

### Software Dependencies:
- Python 3.11 or above
- Blender (for model conversion)
- Pip or Poetry (for managing Python dependencies)
- Docker (for containerized environments, optional)
- `loguru` for logging

### Python Packages:
This project uses several Python libraries, including:
- `requests`: for downloading model and texture files.
- `asyncio`: for asynchronous crawling.
- `loguru`: for logging.
- `bpy`: for Blender Python scripting.
- `json`: for handling JSON data.

### Blender:
Make sure Blender is installed and accessible via the command line. You can download Blender from [here](https://www.blender.org/download/).

## Project Structure

The project is organized as follows:

```
.
├── data/
│   ├── input/                # Input files like grid geojson.
│   └── output/
│       ├── crawler/          # Data generated by the crawler.
│       ├── cleaner/          # Cleaned data (CSV, JSON).
│       └── downloader/       # Downloaded 3D models and textures.
│       └── converter/        # Converted models in GLB or FBX format.
├── src/
│   ├── app/
│       ├── modules/          # Python modules for different steps of the pipeline.
│       ├── utils/            # Utility functions like Blender helpers.
└── main.py                   # Main script that runs the entire pipeline.
```

## Change the `BLENDER_EXE` Environment Variable

Please update the `BLENDER_EXE` environment variable to reflect the correct path for your Blender installation. The current path may need to be modified based on your Blender version or installation location.

For example, the environment variable might look like this:

```bash
BLENDER_EXE=C:/Users/PC.GIS-CHANDTN/AppData/Roaming/Blender Foundation/Blender/4.3/scripts/modules
```

## Setup Instructions

### Step 1: Install Dependencies

If you haven't done so already, make sure to install all dependencies:

```bash
poetry install
```

### Step 2: Set up Directories

Ensure the following directories exist or are created:

```bash
mkdir -p data/output/crawler
mkdir -p data/output/cleaner
mkdir -p data/output/downloader
mkdir -p data/output/downloader/obj
mkdir -p data/output/downloader/texture
```

### Step 3: Running the Pipeline

To run the pipeline, simply execute the `main.py` script. This will start the whole process from crawling data, cleaning, downloading models, and converting them to the desired formats:

```bash
poetry run python -m src.main
```

The script will:

1. **Crawl** data using the `BuildingCrawler` class.
2. **Clean** the crawled data using `DataCleaner`.
3. **Download** models and textures using `ModelDownloader`.
4. **Convert** models using Blender and save them in the desired format (e.g., GLB or FBX).

### Step 4: View Logs

Logs are generated using `loguru` and will be printed to the console. If you want to save the logs to a file, you can modify the `main.py` script to log to a file by configuring the logger.

## Development

### Type Checking

Run MyPy for static type checks:
```bash
poetry run mypy src
```

### Formatting and Linting

Format the code:
```bash
poetry run black src
```

Lint the code:
```bash
poetry run pylint src
```

## Notes

- The pipeline assumes you have a valid grid GeoJSON file (`grid_lv3.geojson`) that specifies the area for crawling. Modify the input grid file path as needed.
- The `BuildingCrawler` class uses a pagination mechanism (`num_pages` parameter) to crawl a specific number of pages. You can adjust this according to your needs.
- The Blender conversion step requires that Blender be installed on your system. The script uses Blender's Python API (`bpy`) to perform model conversions, so make sure Blender is configured properly.

## Troubleshooting

- If you encounter errors related to missing packages, ensure all dependencies are installed using the commands above.
- If Blender fails to run, check that the Blender installation is correct and the `blender_runner` utility can locate the Blender executable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
