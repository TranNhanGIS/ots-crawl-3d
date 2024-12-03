"""
DataCleaner Class

This module defines the DataCleaner class, which is used to clean and normalize the data crawled from various sources. 
It processes the data by removing duplicates, normalizing model names, and converting specific columns to JSON and back to string format. 
The cleaned data is then saved to both CSV and JSON files.

Key Features:
- Removes duplicate entries based on the "id" column.
- Normalizes model names, removing image extensions and ensuring the ".obj" extension is present.
- Converts relevant columns to JSON and normalizes them.
- Outputs cleaned data to both CSV and JSON formats.

Usage:
    cleaner = DataCleaner(input_crawler_file="input.csv", output_cleaner_csv_file="output.csv", output_cleaner_json_file="output.json")
    cleaner.run()

Dependencies:
- pandas
- re
- src.app.utils.data_utils (str_to_json, json_to_str)
"""

import pandas as pd
import re
from src.app.utils.data_utils import str_to_json, json_to_str


class DataCleaner:
    """
    A class for cleaning and normalizing crawled data.

    Attributes:
        input_crawler_file (str): Path to the input CSV file containing crawled data.
        output_cleaner_csv_file (str): Path to the output CSV file where cleaned data will be saved.
        output_cleaner_json_file (str): Path to the output JSON file where cleaned data will be saved.
        df (pd.DataFrame): DataFrame holding the loaded data from the input file.
    """

    def __init__(
        self, input_crawler_file: str, output_cleaner_csv_file: str, output_cleaner_json_file: str
    ):
        """
        Initializes the DataCleaner with input and output file paths.

        Args:
            input_crawler_file (str): Path to the input CSV file containing crawled data.
            output_cleaner_csv_file (str): Path to the output CSV file for cleaned data.
            output_cleaner_json_file (str): Path to the output JSON file for cleaned data.
        """
        self.input_crawler_file = input_crawler_file
        self.output_cleaner_csv_file = output_cleaner_csv_file
        self.output_cleaner_json_file = output_cleaner_json_file
        self.df = pd.read_csv(self.input_crawler_file)

    @staticmethod
    def normalize_model(model: dict) -> str:
        """
        Normalizes the model by removing image file extensions and ensuring the ".obj" extension is added.

        Args:
            model (dict): A dictionary containing the model's properties, including the "objName".

        Returns:
            str: The normalized model name.
        """
        model["objName"] = re.sub(r"\b(.jpg|.JPG|.png|.PNG)\b", "", model["objName"])
        if ".obj" not in model["objName"]:
            model["objName"] += ".obj"
        return model

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes duplicate rows from the DataFrame based on the "id" column, keeping only the first occurrence.

        Args:
            df (pd.DataFrame): The DataFrame to clean.

        Returns:
            pd.DataFrame: The cleaned DataFrame with duplicates removed.
        """
        return df.drop_duplicates(subset=["id"], keep="first", ignore_index=True)

    def run(self):
        """
        Runs the data cleaning process: removes duplicates, normalizes model names, converts relevant columns to JSON,
        and saves the cleaned data to CSV and JSON files.
        """
        self.df = self.clean_data(self.df)
        self.df["model"] = self.df["model"].apply(str_to_json)
        self.df["model"] = self.df["model"].apply(self.normalize_model)
        self.df["camera"] = self.df["camera"].apply(str_to_json)
        self.df["location"] = self.df["location"].apply(str_to_json)
        self.df["types"] = self.df["types"].apply(str_to_json)
        self.df.to_json(
            self.output_cleaner_json_file, orient="records", lines=False, force_ascii=False
        )

        self.df["model"] = self.df["model"].apply(json_to_str)
        self.df["camera"] = self.df["camera"].apply(json_to_str)
        self.df["location"] = self.df["location"].apply(json_to_str)
        self.df["types"] = self.df["types"].apply(json_to_str)
        self.df.to_csv(self.output_cleaner_csv_file, index=False)
