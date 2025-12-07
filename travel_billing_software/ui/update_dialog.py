"""
Update notification dialog for Travel Billing Software
Shows update available message with download progress
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


class DownloadThread(QThread):
    """Background thread for downloading updates"""
    progress = pyqtSignal(int, int)  # downloaded, total
    finished = pyqtSignal(str)  # installer_path
    error = pyqtSignal(str)  # error_message
    
    def __init__(self, updater, download_url):
        super().__init__()
        self.updater = updater
        self.download_url = download_url
    
    def run(self):
        """Download the update file"""
        try:
            def progress_callback(downloaded, total):
                self.progress.emit(downloaded, total)
            
            installer_path = self.updater.download_update(
                self.download_url, 
                progress_callback
            )
            
            if installer_path:
                self.finished.emit(installer_path)
            else:
                self.error.emit("Failed to download update")
        except Exception as e:
            self.error.emit(str(e))


class UpdateDialog(QDialog):
    """Dialog showing update information and download progress"""
    
    def __init__(self, updater, latest_version, download_url, parent=None):
        super().__init__(parent)
        self.updater = updater
        self.latest_version = latest_version
        self.download_url = download_url
        self.installer_path = None
        
        self.setWindowTitle("Update Available")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setModal(True)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel("🎉 New Version Available!")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Version info
        current_version = self.updater.get_current_version()
        version_label = QLabel(
            f"Current Version: <b>{current_version}</b><br>"
            f"Latest Version: <b>{self.latest_version}</b>"
        )
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # Release notes
        notes_label = QLabel("What's New:")
        notes_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(notes_label)
        
        self.release_notes = QTextEdit()
        self.release_notes.setReadOnly(True)
        self.release_notes.setMaximumHeight(150)
        release_notes_text = self.updater.get_release_notes()
        self.release_notes.setPlainText(release_notes_text)
        layout.addWidget(self.release_notes)
        
        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #555;")
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.update_button = QPushButton("Download and Install")
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.update_button.clicked.connect(self.start_download)
        button_layout.addWidget(self.update_button)
        
        self.cancel_button = QPushButton("Not Now")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def start_download(self):
        """Start downloading the update"""
        self.update_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Downloading update...")
        
        # Start download thread
        self.download_thread = DownloadThread(self.updater, self.download_url)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.error.connect(self.download_error)
        self.download_thread.start()
    
    def update_progress(self, downloaded, total):
        """Update the progress bar"""
        if total > 0:
            percentage = int((downloaded / total) * 100)
            self.progress_bar.setValue(percentage)
            
            # Convert to MB
            downloaded_mb = downloaded / (1024 * 1024)
            total_mb = total / (1024 * 1024)
            self.status_label.setText(
                f"Downloading: {downloaded_mb:.1f} MB / {total_mb:.1f} MB"
            )
    
    def download_finished(self, installer_path):
        """Handle successful download"""
        self.installer_path = installer_path
        self.progress_bar.setValue(100)
        self.status_label.setText("Download complete! Ready to install.")
        
        # Change button to install
        self.update_button.setText("Install Now")
        self.update_button.setEnabled(True)
        self.update_button.clicked.disconnect()
        self.update_button.clicked.connect(self.install_update)
        self.cancel_button.setEnabled(True)
    
    def download_error(self, error_message):
        """Handle download error"""
        self.status_label.setText(f"Error: {error_message}")
        self.status_label.setStyleSheet("color: red;")
        self.update_button.setText("Retry")
        self.update_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
    
    def install_update(self):
        """Install the downloaded update"""
        if self.installer_path:
            self.status_label.setText("Launching installer...")
            success = self.updater.install_update(self.installer_path)
            
            if success:
                # The app will close when installer starts
                self.accept()
                import sys
                sys.exit(0)
            else:
                self.status_label.setText("Failed to launch installer")
                self.status_label.setStyleSheet("color: red;")


class CheckingUpdateDialog(QDialog):
    """Simple dialog shown while checking for updates"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Checking for Updates")
        self.setMinimumWidth(300)
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
        
        layout = QVBoxLayout()
        
        label = QLabel("Checking for updates...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        progress = QProgressBar()
        progress.setRange(0, 0)  # Indeterminate progress
        layout.addWidget(progress)
        
        self.setLayout(layout)
