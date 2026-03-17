import json
import csv
from typing import List, Dict
from pathlib import Path

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class DataExporter:
    """A class for exporting data to various formats."""

    @staticmethod
    def to_json(data: List[Dict], path: Path) -> Path:
        """Export data to a JSON file.

        Args:
            data (List[Dict]): The data to export.
            path (Path): The path where the JSON file will be saved.

        Returns:
            Path: The path to the saved JSON file.
        """
        try:
            with open(path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            return path
        except IOError as e:
            raise Exception(f"Error writing JSON file: {e}")

    @staticmethod
    def to_csv(data: List[Dict], path: Path) -> Path:
        """Export data to a CSV file.

        Args:
            data (List[Dict]): The data to export.
            path (Path): The path where the CSV file will be saved.

        Returns:
            Path: The path to the saved CSV file.
        """
        try:
            with open(path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return path
        except IOError as e:
            raise Exception(f"Error writing CSV file: {e}")

    @staticmethod
    def to_excel(data: List[Dict], path: Path) -> Path:
        """Export data to an Excel file.

        Args:
            data (List[Dict]): The data to export.
            path (Path): The path where the Excel file will be saved.

        Returns:
            Path: The path to the saved Excel file.
        
        Raises:
            ImportError: If pandas is not installed.
        """
        if not PANDAS_AVAILABLE:
            raise ImportError("Pandas is required for exporting to Excel.")

        try:
            df = pd.DataFrame(data)
            df.to_excel(path, index=False)
            return path
        except Exception as e:
            raise Exception(f"Error writing Excel file: {e}")

    @staticmethod
    def to_txt(data: List[Dict], path: Path) -> Path:
        """Export data to a TXT file.

        Args:
            data (List[Dict]): The data to export.
            path (Path): The path where the TXT file will be saved.

        Returns:
            Path: The path to the saved TXT file.
        """
        try:
            with open(path, 'w', encoding='utf-8') as txt_file:
                for entry in data:
                    txt_file.write(f"{entry}\n")
            return path
        except IOError as e:
            raise Exception(f"Error writing TXT file: {e}")
