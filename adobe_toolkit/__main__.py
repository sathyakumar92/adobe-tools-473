import os
import json
import csv
import argparse
from typing import List, Dict
from pydub import AudioSegment
from mutagen import File as MutagenFile
from concurrent.futures import ThreadPoolExecutor, as_completed

class AudioToolkit:
    def __init__(self, directory: str):
        self.directory = directory

    def scan_directory(self) -> List[str]:
        """Scan the directory for audio files."""
        audio_files = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(('.wav', '.mp3', '.flac')):
                    audio_files.append(os.path.join(root, file))
        return audio_files

    def get_file_info(self, file_path: str) -> Dict[str, str]:
        """Get metadata information from an audio file."""
        try:
            audio = MutagenFile(file_path)
            return {key: str(value) for key, value in audio.items()}
        except Exception as e:
            print(f"Error reading metadata from {file_path}: {e}")
            return {}

    def export_to_json(self, file_info: List[Dict[str, str]], output_file: str) -> None:
        """Export file information to a JSON file."""
        try:
            with open(output_file, 'w') as json_file:
                json.dump(file_info, json_file, indent=4)
            print(f"Exported data to {output_file}")
        except Exception as e:
            print(f"Error exporting to JSON: {e}")

    def export_to_csv(self, file_info: List[Dict[str, str]], output_file: str) -> None:
        """Export file information to a CSV file."""
        try:
            with open(output_file, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=file_info[0].keys())
                writer.writeheader()
                writer.writerows(file_info)
            print(f"Exported data to {output_file}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

    def batch_process(self, files: List[str]) -> List[Dict[str, str]]:
        """Process multiple audio files and return their metadata."""
        results = []
        with ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(self.get_file_info, file): file for file in files}
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    print(f"Error processing {file}: {e}")
        return results


def main():
    parser = argparse.ArgumentParser(description='Audio Toolkit for Adobe Audition on Windows')
    subparsers = parser.add_subparsers(dest='command')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan directory for audio files')
    scan_parser.add_argument('directory', type=str, help='Directory to scan for audio files')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show information about a specific file')
    info_parser.add_argument('file', type=str, help='Path to the audio file')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to JSON/CSV')
    export_parser.add_argument('output_format', choices=['json', 'csv'], help='Output format')
    export_parser.add_argument('files', type=str, nargs='+', help='List of audio files to export metadata from')
    export_parser.add_argument('output_file', type=str, help='Output file path')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process multiple files')
    batch_parser.add_argument('directory', type=str, help='Directory containing audio files')

    args = parser.parse_args()

    toolkit = AudioToolkit(args.directory if args.command in ['scan', 'batch'] else os.path.dirname(args.file))

    if args.command == 'scan':
        audio_files = toolkit.scan_directory()
        print("Found audio files:")
        for file in audio_files:
            print(file)

    elif args.command == 'info':
        info = toolkit.get_file_info(args.file)
        print("File Information:")
        for key, value in info.items():
            print(f"{key}: {value}")

    elif args.command == 'export':
        file_info = []
        for file in args.files:
            info = toolkit.get_file_info(file)
            if info:
                file_info.append(info)
        if args.output_format == 'json':
            toolkit.export_to_json(file_info, args.output_file)
        elif args.output_format == 'csv':
            toolkit.export_to_csv(file_info, args.output_file)

    elif args.command == 'batch':
        audio_files = toolkit.scan_directory()
        results = toolkit.batch_process(audio_files)
        print("Batch processing complete. Processed files:")
        for result in results:
            print(result)

if __name__ == '__main__':
    main()
