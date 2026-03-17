import logging
import os
from pathlib import Path
from typing import Optional
import win32com.client

class AdobeAuditionClient:
    """A client interface for interacting with Adobe Audition via COM on Windows."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initializes the AdobeAuditionClient.

        Args:
            config_path (Optional[Path]): Path to the configuration file.
        """
        self.config_path = config_path
        self.audition_app = None
        self.connected = False
        self.logger = self.setup_logging()

    def setup_logging(self) -> logging.Logger:
        """Sets up logging for the client.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger("AdobeAuditionClient")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def connect(self) -> bool:
        """Connects to the Adobe Audition application via COM.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            self.logger.debug("Attempting to connect to Adobe Audition.")
            self.audition_app = win32com.client.Dispatch("Audition.Application")
            self.connected = True
            self.logger.info("Successfully connected to Adobe Audition.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Adobe Audition: {e}")
            return False

    def disconnect(self):
        """Disconnects from the Adobe Audition application."""
        if self.connected:
            self.logger.debug("Disconnecting from Adobe Audition.")
            self.audition_app = None
            self.connected = False
            self.logger.info("Disconnected from Adobe Audition.")

    def get_version(self) -> str:
        """Retrieves the version of Adobe Audition.

        Returns:
            str: Version of the Adobe Audition application.

        Raises:
            RuntimeError: If not connected to Adobe Audition.
        """
        if not self.connected:
            raise RuntimeError("Not connected to Adobe Audition.")
        version = self.audition_app.Version
        self.logger.debug(f"Retrieved Adobe Audition version: {version}")
        return version

    def is_installed(self) -> bool:
        """Checks if Adobe Audition is installed on the system.

        Returns:
            bool: True if Adobe Audition is installed, False otherwise.
        """
        installed = False
        try:
            self.logger.debug("Checking if Adobe Audition is installed.")
            audition_path = r"C:\Program Files\Adobe\Adobe Audition <version>\Adobe Audition.exe"
            installed = os.path.exists(audition_path)
            self.logger.info(f"Adobe Audition installed: {installed}")
        except Exception as e:
            self.logger.error(f"Error checking installation: {e}")
        return installed
