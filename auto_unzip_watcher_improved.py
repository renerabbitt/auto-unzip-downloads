#!/usr/bin/env python3
"""
Auto Unzip Watcher - Improved Version
Automatically monitors the Downloads folder and processes zip files as they appear.
Uses Windows file system notifications for minimal performance impact.
"""

import os
import time
import zipfile
import threading
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_unzip_watcher.log'),
        logging.StreamHandler()
    ]
)

class ZipFileHandler(FileSystemEventHandler):
    """Handles zip file events in the Downloads directory."""
    
    def __init__(self, downloads_dir):
        self.downloads_dir = Path(downloads_dir)
        self.processing_files = set()  # Track files being processed to avoid duplicates
        
    def on_created(self, event):
        """Called when a new file is created."""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if file_path.suffix.lower() == '.zip':
            # Wait a moment to ensure the file is fully written
            time.sleep(2)
            self.process_zip_file(file_path)
    
    def on_moved(self, event):
        """Called when a file is moved/renamed."""
        if event.is_directory:
            return
            
        file_path = Path(event.dest_path)
        if file_path.suffix.lower() == '.zip':
            # Wait a moment to ensure the file is fully written
            time.sleep(2)
            self.process_zip_file(file_path)
    
    def process_zip_file(self, zip_path):
        """Process a single zip file."""
        # Avoid processing the same file multiple times
        if zip_path in self.processing_files:
            return
            
        self.processing_files.add(zip_path)
        
        try:
            logging.info(f"Detected new zip file: {zip_path.name}")
            
            # Check if file is still being downloaded (file size changing)
            initial_size = zip_path.stat().st_size
            time.sleep(1)
            current_size = zip_path.stat().st_size
            
            if initial_size != current_size:
                logging.info(f"File {zip_path.name} is still being downloaded, waiting...")
                # Wait for download to complete
                while True:
                    time.sleep(2)
                    new_size = zip_path.stat().st_size
                    if new_size == current_size:
                        break
                    current_size = new_size
                logging.info(f"Download completed for {zip_path.name}")
            
            # Process the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                logging.info(f"Contains {len(file_list)} file(s)")
                
                # Create subfolder with zip file name (without .zip extension)
                zip_name = zip_path.stem  # Gets filename without extension
                extract_dir = self.downloads_dir / zip_name
                
                # Create the subfolder if it doesn't exist
                extract_dir.mkdir(exist_ok=True)
                logging.info(f"Created extraction directory: {extract_dir}")
                
                # Extract all files to the subfolder
                zip_ref.extractall(extract_dir)
                logging.info(f"Successfully extracted to: {extract_dir}")
                
                # Force close the zip file to release any handles
                zip_ref.close()
                
                # Wait a moment to ensure file handles are released
                time.sleep(1)
                
                # Delete the original zip file with retry logic
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        zip_path.unlink()
                        logging.info(f"Deleted original zip file: {zip_path.name}")
                        break
                    except PermissionError as e:
                        if attempt < max_retries - 1:
                            logging.warning(f"Permission error deleting {zip_path.name}, retrying in 2 seconds... (attempt {attempt + 1}/{max_retries})")
                            time.sleep(2)
                        else:
                            logging.error(f"Failed to delete {zip_path.name} after {max_retries} attempts: {e}")
                    except Exception as e:
                        logging.error(f"Error deleting {zip_path.name}: {e}")
                        break
                
                logging.info(f"Completed processing {zip_path.name}")
                
        except zipfile.BadZipFile:
            logging.error(f"{zip_path.name} is not a valid zip file")
        except PermissionError as e:
            logging.error(f"Permission denied when processing {zip_path.name}: {e}")
        except Exception as e:
            logging.error(f"Error processing {zip_path.name}: {str(e)}")
        finally:
            # Remove from processing set
            self.processing_files.discard(zip_path)

def main():
    """Main function to start the folder watcher."""
    downloads_dir = Path(r"C:\Users\rener\Dropbox\Assets\Downloads")
    
    # Check if Downloads directory exists
    if not downloads_dir.exists():
        logging.error(f"Downloads directory not found at {downloads_dir}")
        return
    
    logging.info("Auto Unzip Watcher Starting")
    logging.info("=" * 50)
    logging.info(f"Monitoring directory: {downloads_dir}")
    logging.info("=" * 50)
    
    # Create event handler and observer
    event_handler = ZipFileHandler(downloads_dir)
    observer = Observer()
    observer.schedule(event_handler, str(downloads_dir), recursive=False)
    
    try:
        # Start watching
        observer.start()
        logging.info("Watcher started. Monitoring for new zip files...")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logging.info("Stopping watcher...")
        observer.stop()
        observer.join()
        logging.info("Watcher stopped.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main() 