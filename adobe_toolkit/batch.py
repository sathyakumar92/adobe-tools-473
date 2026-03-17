from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import List, Callable, Any
import glob
import os

@dataclass
class Result:
    path: Path
    success: bool
    data: Any = None
    error: str = ""

class BatchProcessor:
    def __init__(self, max_workers: int = 4):
        """
        Initialize the BatchProcessor with a specified number of worker threads.

        :param max_workers: Maximum number of worker threads to use for processing.
        """
        self.max_workers = max_workers

    def process_directory(self, path: Path, pattern: str = "*") -> List[Result]:
        """
        Process all files in a directory that match a specified pattern.

        :param path: The directory path to process.
        :param pattern: The glob pattern to match files.
        :return: A list of Result objects containing the outcome of each file processing.
        """
        results = []
        file_paths = list(Path(path).glob(pattern))

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {executor.submit(self.process_file, file_path): file_path for file_path in file_paths}

            for future in as_completed(future_to_path):
                file_path = future_to_path[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(Result(path=file_path, success=False, error=str(e)))

        return results

    def process_files(self, paths: List[Path], callback: Callable = None) -> List[Result]:
        """
        Process a list of files and optionally call a callback function for each file.

        :param paths: A list of file paths to process.
        :param callback: An optional callback function to call with each file's result.
        :return: A list of Result objects containing the outcome of each file processing.
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {executor.submit(self.process_file, file_path): file_path for file_path in paths}

            for future in as_completed(future_to_path):
                file_path = future_to_path[future]
                try:
                    result = future.result()
                    if callback:
                        callback(result)
                    results.append(result)
                except Exception as e:
                    results.append(Result(path=file_path, success=False, error=str(e)))

        return results

    def process_file(self, file_path: Path) -> Result:
        """
        Process a single audio file. This is a placeholder for actual audio processing logic.

        :param file_path: The path of the audio file to process.
        :return: A Result object indicating the success or failure of the processing.
        """
        try:
            # Placeholder for actual audio processing logic
            # For example, read the file, perform analysis, etc.
            # Here we just simulate a successful processing
            data = f"Processed {file_path.name}"
            return Result(path=file_path, success=True, data=data)
        except Exception as e:
            return Result(path=file_path, success=False, error=str(e))
