# Auto-Update System for Travel Billing Software

## Overview
The auto-update system checks for new releases from GitHub and allows users to download and install updates with one click.

## How It Works

### For Users
1. App checks for updates 2 seconds after login (non-blocking)
2. If update is available, a dialog shows:
   - Current version
   - New version available
   - Release notes
   - Download and Install button
3. User clicks "Download and Install"
4. Update downloads with progress bar
5. Installer launches automatically
6. App closes and new version installs

### For Developers (Release Process)

#### Prerequisites
1. **Install Inno Setup**: Download from https://jrsoftware.org/isinfo.php
2. **Ensure Git is installed**: For creating tags

#### Step-by-Step Release Process

**1. Update Version**
```bash
# Edit pyproject.toml
# Change: version = "1.0.0" to version = "1.0.1"
```

**2. Build Installer**
```bash
# Run the automated build script
build_release.bat
```

This script will:
- Read version from `pyproject.toml`
- Clean previous builds
- Run PyInstaller to create `.exe`
- Run Inno Setup to create installer
- Output: `Output\TravelBilling_Setup_v1.0.1.exe`

**3. Create GitHub Release**
```bash
# Commit your changes
git add .
git commit -m "Release v1.0.2"

# Create and push tag
git tag v1.0.2
git push origin v1.0.2
```

**4. Upload to GitHub**
1. Go to: https://github.com/fidha-jazeel/billing-software/releases
2. Click "Draft a new release"
3. Choose tag: `v1.0.1`
4. Release title: `v1.0.1` or `Version 1.0.1`
5. Description: Add release notes (what's new, bug fixes, etc.)
6. Attach file: `Output\TravelBilling_Setup_v1.0.1.exe`
7. Click "Publish release"

**5. Done!**
All users will automatically see the update notification next time they open the app.

## Components

### Files Created

1. **`utils/auto_updater.py`**
   - Checks GitHub API for latest release
   - Compares versions
   - Downloads update file
   - Launches installer

2. **`ui/update_dialog.py`**
   - Update notification dialog
   - Download progress bar
   - Release notes display

3. **`TravelBilling.iss`**
   - Inno Setup script
   - Creates professional Windows installer
   - Supports silent updates

4. **`build_release.bat`**
   - Automated build script
   - Runs PyInstaller + Inno Setup

### Modified Files

1. **`pyproject.toml`**
   - Added version: `1.0.0`
   - Source of truth for version number

2. **`main.py`**
   - Added update check on startup (2 seconds after login)
   - Non-blocking background check

3. **`ui/main_window.py`**
   - Added "Check for Updates" button in sidebar
   - Manual update check functionality

## Configuration

### Change Update Check Behavior

**In `main.py`:**
```python
# Change delay before checking (currently 2000ms = 2 seconds)
QTimer.singleShot(2000, lambda: check_for_updates(main_window))

# To disable automatic checks, comment out this line
# QTimer.singleShot(2000, lambda: check_for_updates(main_window))
```

### Customize Installer

**In `TravelBilling.iss`:**
- Change company name: `#define MyAppPublisher "Your Company Name"`
- Change install location: `DefaultDirName={autopf}\{#MyAppName}`
- Modify desktop icon creation behavior

## Troubleshooting

### Users Can't See Updates
- Check internet connection
- Verify GitHub repository is public
- Check if release has `.exe` file attached

### Update Download Fails
- Firewall might be blocking download
- Check GitHub release file is accessible
- Verify file size isn't too large

### Installer Won't Run
- Requires admin privileges
- Antivirus might block (consider code signing certificate)
- User might need to manually allow through Windows SmartScreen

## Security Considerations

### Code Signing (Recommended for Production)
To avoid Windows SmartScreen warnings:
1. Purchase code signing certificate ($100-300/year)
2. Sign the `.exe` with `signtool.exe`
3. Users won't see "Unknown Publisher" warning

### HTTPS Only
- All downloads are from GitHub (HTTPS)
- GitHub API calls are authenticated
- No man-in-the-middle risk

## Testing the Update System

### Before First Release
1. Build and install v1.0.0
2. Create GitHub release for v1.0.1
3. Open installed app
4. Should see update notification after 2 seconds

### Manual Test
1. Click "🔄 Check for Updates" in sidebar
2. Should immediately check for updates
3. Shows current version if no updates available

## Future Enhancements

Possible improvements:
- **Delta updates**: Only download changed files
- **Automatic rollback**: Restore previous version if update fails
- **Update scheduling**: Install updates at convenient time
- **Forced updates**: Require update for critical security patches
- **Beta channel**: Separate testing release track

## Notes

- Update check does NOT block user from working
- Users can dismiss update and install later
- "Check for Updates" button available anytime
- Failed update checks are silent (don't interrupt user)
- App exits gracefully when installer starts
