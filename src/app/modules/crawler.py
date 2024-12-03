"""
BuildingCrawler Class

This module defines the BuildingCrawler class, which is used to scrape building-related data from a set of grid coordinates. 
The crawler generates URLs based on the grid data, processes web pages to extract relevant information, and saves the results in a CSV file.

Key Features:
- Initializes with grid data from a JSON file and outputs crawled data to a CSV.
- Crawls pages concurrently (using Playwright and asyncio).
- Automatically aborts non-relevant requests (images, fonts, media).
- Extracts and saves relevant data (like location, camera, elevation, etc.) from 3D mode responses.

Usage:
    crawler = BuildingCrawler(input_grid_file="grid_data.json", output_crawler_file="output.csv", num_pages=5)
    asyncio.run(crawler.run())

Dependencies:
- asyncio
- csv
- json
- loguru
- playwright.async_api

"""

import asyncio
import csv
import json
from loguru import logger
from playwright.async_api import (
    async_playwright,
    Response,
    Request,
    Route,
    BrowserContext,
)
from src.app.config import settings


class BuildingCrawler:
    """
    A crawler that processes grid data, generates URLs, and scrapes relevant information from web pages.

    Attributes:
        input_grid_file (str): Path to the input grid file in JSON format.
        output_crawler_file (str): Path to the output CSV file.
        num_pages (int): Number of pages to process concurrently (default is 3).
        fieldnames (list): List of CSV fieldnames for the output file.
        grid_file (file object): File handler for reading the grid data.
        grid_data (dict): Loaded grid data from the input file.
        crawler_file (file object): File handler for writing crawled data.
        writer (csv.DictWriter): CSV writer to save crawled data.
    """

    def __init__(self, input_grid_file, output_crawler_file, num_pages=3):
        """
        Initializes the BuildingCrawler with input and output file paths and the number of pages to process in parallel.

        Args:
            input_grid_file (str): Path to the input grid file in JSON format.
            output_crawler_file (str): Path to the output CSV file.
            num_pages (int, optional): Number of pages to process concurrently. Default is 3.
        """
        self.input_grid_file = input_grid_file
        self.output_crawler_file = output_crawler_file
        self.num_pages = num_pages
        self.fieldnames = [
            "bearing",
            "camera",
            "elevation",
            "endDate",
            "id",
            "location",
            "maxZoom",
            "minZoom",
            "model",
            "name",
            "scale",
            "startDate",
            "types",
        ]

        self.grid_file = open(self.input_grid_file, "r", encoding="utf-8")
        self.grid_data = json.load(self.grid_file)

        self.crawler_file = open(self.output_crawler_file, mode="w", encoding="utf-8", newline="")
        self.writer = csv.DictWriter(self.crawler_file, self.fieldnames)
        self.writer.writeheader()

    @staticmethod
    def generate_url(feature: dict) -> str:
        """
        Generates a URL for crawling based on the feature's geographical properties.

        Args:
            feature (dict): A feature from the grid data containing geographical properties (lat, lng).

        Returns:
            str: The generated URL.
        """
        lat = feature.get("properties").get("lat")
        lng = feature.get("properties").get("lng")
        zoom = "19.00"
        return f"{settings.crawler_url}?camera={lat},{lng},{zoom},0.0,0.0,d"

    @staticmethod
    def is_abort_url(request: Request) -> bool:
        """
        Determines if a request should be aborted based on its resource type or URL extension.

        Args:
            request (Request): The request to check.

        Returns:
            bool: True if the request should be aborted, False otherwise.
        """
        return (
            request.resource_type in ["image", "font", "media"]
            or any(ext in request.url for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"])
            or any(ext in request.url for ext in [".mp3", ".mp4", ".avi", ".mov", ".mkv", ".webm"])
            or any(ext in request.url for ext in [".woff", ".woff2", ".ttf", ".eot", ".otf"])
        )

    async def abort_url(self, route: Route) -> None:
        """
        Aborts a request if it matches certain criteria (image, font, media, etc.), otherwise allows the request to continue.

        Args:
            route (Route): The route for the request.
        """
        if self.is_abort_url(route.request):
            await route.abort()
        else:
            await route.continue_()

    async def response_url(self, response: Response) -> None:
        """
        Processes a response by extracting data if it contains relevant information and writing it to the CSV file.

        Args:
            response (Response): The response to process.
        """
        if "mode=3d" in response.url:
            try:
                res_json = await response.json()
                objects = res_json.get("result", {}).get("objects", [])
                if objects:
                    self.writer.writerows(objects)
                logger.success(f"Crawled: {response.url}; Data: {objects}")
            except Exception as e:
                logger.error(f"Failed to process response: {response.url}; Exception: {e}")

    async def process_page(self, context: BrowserContext, url: str) -> None:
        """
        Crawls a single page by opening it in the browser and processing its responses.

        Args:
            context (BrowserContext): The Playwright browser context.
            url (str): The URL to visit and scrape.
        """
        page = await context.new_page()
        try:
            page.on("response", self.response_url)
            await page.route("**/*", self.abort_url)
            await page.goto(url)
            await page.wait_for_load_state("networkidle")
        except Exception as e:
            logger.error(f"Failed to crawl: {url}; Exception: {e}")
        finally:
            await page.close()

    async def run(self):
        """
        Starts the crawling process by launching the browser and processing URLs in parallel.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            urls = [self.generate_url(feature) for feature in self.grid_data.get("features")]

            for i in range(0, len(urls), self.num_pages):
                tasks = [
                    self.process_page(context, urls[i + j])
                    for j in range(min(self.num_pages, len(urls) - i))
                ]
                await asyncio.gather(*tasks)

            await browser.close()

        self.crawler_file.close()
