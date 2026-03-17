from pathlib import Path
from dataclasses import dataclass
from mutagen import File, MutagenError
import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class Metadata:
    title: str = ""
    author: str = ""
    created: str = ""
    modified: str = ""
    genre: str = ""
    album: str = ""

class AdobeAuditionMetadataReader:
    @staticmethod
    def read(path: Path) -> Metadata:
        """
        Reads metadata from an audio file.

        Args:
            path (Path): The path to the audio file.

        Returns:
            Metadata: A Metadata object containing the audio file's metadata.

        Raises:
            FileNotFoundError: If the file does not exist.
            MutagenError: If there is an error reading the metadata.
        """
        if not path.is_file():
            logging.error(f"File not found: {path}")
            raise FileNotFoundError(f"The file {path} does not exist.")

        try:
            audio = File(str(path))
            if audio is None:
                logging.error(f"Unable to read metadata from: {path}")
                raise MutagenError(f"Unable to read metadata from: {path}")

            metadata = Metadata(
                title=audio.tags.get('TIT2', [""])[0],
                author=audio.tags.get('TPE1', [""])[0],
                created=audio.tags.get('TDRC', [""])[0],
                modified=audio.tags.get('TORY', [""])[0],
                genre=audio.tags.get('TCON', [""])[0],
                album=audio.tags.get('TALB', [""])[0],
            )
            logging.info(f"Metadata read successfully from {path}")
            return metadata
        except MutagenError as e:
            logging.error(f"Error reading metadata: {e}")
            raise

    @staticmethod
    def write(path: Path, metadata: Metadata) -> bool:
        """
        Writes metadata to an audio file.

        Args:
            path (Path): The path to the audio file.
            metadata (Metadata): The Metadata object containing the metadata to write.

        Returns:
            bool: True if the metadata was written successfully, False otherwise.

        Raises:
            FileNotFoundError: If the file does not exist.
            MutagenError: If there is an error writing the metadata.
        """
        if not path.is_file():
            logging.error(f"File not found: {path}")
            raise FileNotFoundError(f"The file {path} does not exist.")

        try:
            audio = File(str(path), easy=True)
            if audio is None:
                logging.error(f"Unable to write metadata to: {path}")
                raise MutagenError(f"Unable to write metadata to: {path}")

            audio['TIT2'] = metadata.title
            audio['TPE1'] = metadata.author
            audio['TDRC'] = metadata.created
            audio['TORY'] = metadata.modified
            audio['TCON'] = metadata.genre
            audio['TALB'] = metadata.album

            audio.save()
            logging.info(f"Metadata written successfully to {path}")
            return True
        except MutagenError as e:
            logging.error(f"Error writing metadata: {e}")
            return False
