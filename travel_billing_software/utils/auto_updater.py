"""
Auto-updater module for Travel Billing Software
Checks GitHub releases for updates and handles download/installation
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Dict, Tuple
from urllib import request
from urllib.error import URLError
import tomllib


class AutoUpdater:
    """Handles checking for updates and downloading new versions"""
    
    GITHUB_OWNER = "fidha-jazeel"
    GITHUB_REPO = "billing-software"
    GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    
    def __init__(self):
        self.current_version = self._get_current_version()
        self.latest_release_info: Optional[Dict] = None
    
    def _get_current_version(self) -> str:
        """Get current version from pyproject.toml"""
        try:
            # Get the project root directory
            if getattr(sys, 'frozen', False):
                # Running as compiled executable - use _MEIPASS for bundled resources
                app_path = Path(sys._MEIPASS)
            else:
                # Running as script
                app_path = Path(__file__).parent.parent.parent
            
            pyproject_path = app_path / "pyproject.toml"
            
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    version = data.get("project", {}).get("version", "1.0.0")
                    print(f"Current version from pyproject.toml: {version}")
                    return version
            else:
                print(f"pyproject.toml not found at {pyproject_path}")
                return "1.0.0"
        except Exception as e:
            print(f"Error reading version: {e}")
            return "1.0.0"
    
    def check_for_updates(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check if a new version is available
        
        Returns:
            Tuple of (update_available, latest_version, download_url)
        """
        try:
            # Create request with timeout
            req = request.Request(
                self.GITHUB_API_URL,
                headers={'Accept': 'application/vnd.github.v3+json'}
            )
            
            with request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                self.latest_release_info = data
                latest_version = data.get("tag_name", "").lstrip("v")
                
                # Find the .exe asset
                download_url = None
                for asset in data.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        break
                
                if not download_url:
                    return False, None, None
                
                # Compare versions
                print(f"Comparing versions - Current: {self.current_version}, Latest: {latest_version}")
                if self._is_newer_version(latest_version, self.current_version):
                    print(f"Update available: {latest_version} > {self.current_version}")
                    return True, latest_version, download_url
                else:
                    print(f"No update needed: {latest_version} <= {self.current_version}")
                    return False, latest_version, None
                    
        except URLError as e:
            print(f"Network error checking for updates: {e}")
            return False, None, None
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return False, None, None
    
    def _is_newer_version(self, latest: str, current: str) -> bool:
        """
        Compare version strings (e.g., "1.0.1" vs "1.0.0")
        
        Returns:
            True if latest is newer than current
        """
        try:
            latest_parts = [int(x) for x in latest.split(".")]
            current_parts = [int(x) for x in current.split(".")]
            
            # Pad with zeros if needed
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts += [0] * (max_len - len(latest_parts))
            current_parts += [0] * (max_len - len(current_parts))
            
            return latest_parts > current_parts
        except Exception:
            return False
    
    def download_update(self, download_url: str, progress_callback=None) -> Optional[str]:
        """
        Download the update file
        
        Args:
            download_url: URL to download from
            progress_callback: Optional callback function(downloaded_bytes, total_bytes)
        
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            # Create temp directory
            temp_dir = tempfile.gettempdir()
            filename = download_url.split("/")[-1]
            temp_file = os.path.join(temp_dir, filename)
            
            # Download with progress tracking
            def report_progress(block_num, block_size, total_size):
                if progress_callback:
                    downloaded = block_num * block_size
                    progress_callback(downloaded, total_size)
            
            request.urlretrieve(download_url, temp_file, reporthook=report_progress)
            
            return temp_file
            
        except Exception as e:
            print(f"Error downloading update: {e}")
            return None
    
    def install_update(self, installer_path: str) -> bool:
        """
        Launch the installer and exit current application
        
        Args:
            installer_path: Path to the installer executable
        
        Returns:
            True if installer launched successfully
        """
        try:
            if not os.path.exists(installer_path):
                return False
            
            # Launch installer with elevated privileges (will prompt UAC if needed)
            # /CLOSEAPPLICATIONS asks installer to close running instances
            # /RESTARTAPPLICATIONS restarts the app after installation
            subprocess.Popen(
                [installer_path, "/SILENT", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS"],
                shell=True
            )
            
            # Exit current application to allow update
            # Give a small delay for the process to start
            import time
            time.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"Error installing update: {e}")
            return False
    
    def get_release_notes(self) -> str:
        """Get release notes from latest release"""
        if self.latest_release_info:
            return self.latest_release_info.get("body", "No release notes available.")
        return "No release notes available."
    
    def get_current_version(self) -> str:
        """Get the current application version"""
        return self.current_version
