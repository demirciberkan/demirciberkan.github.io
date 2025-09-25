# EVSEPARKER Firmware Manifest Automation

This directory contains automation scripts for managing firmware distribution in the EVSEPARKER project.

## 🚀 Quick Start

```bash
# Update manifest.json based on firmware folders
./update-all.sh

# Preview changes without modifying files
./update-all.sh --dry-run
```

## 📜 Available Scripts

### 1. `update-manifest.py` - Firmware Manifest Updater

Automatically scans firmware directories and updates `manifest.json` based on folder structure and file naming conventions.

**Features:**
- Dynamically discovers hardware models from folder names in `/firmware` directory
- Scans firmware files and extracts version information from filenames
- Generates URLs for firmware downloads
- Handles MAC-specific firmware targeting
- Preserves manually added MAC entries
- Sorts versions chronologically (newest first)

**File Naming Convention:**
```
# Standard firmware files
EVSE_10_2_0.bin          → version 10.2.0
EVSE_10_1_43.bin         → version 10.1.43

# MAC-specific firmware (optional)
EVSE_10_2_1_custom_ABCDEF123456.bin → custom firmware for MAC AB:CD:EF:12:34:56
```

**Usage:**
```bash
# Update manifest with default settings
python3 update-manifest.py

# Preview changes without writing files
python3 update-manifest.py --dry-run

# Use custom base URL
python3 update-manifest.py --base-url https://yourdomain.com

# Reset all MAC-specific entries (remove manually added ones)
python3 update-manifest.py --reset-mac
```

### 2. `update-all.sh` - Simplified Runner Script

Runs the manifest update with colored output and comprehensive error handling.

**Features:**
- Runs manifest update with single command
- Colored output for better readability
- Dry-run mode for preview
- Comprehensive error handling

**Usage:**
```bash
# Update manifest (recommended)
./update-all.sh

# Preview what would be changed
./update-all.sh --dry-run

# Use custom base URL
./update-all.sh --base-url https://yourdomain.com
```

## 📁 Directory Structure

The scripts expect the following directory structure:

```
demirciberkan.github.io/
├── manifest.json                           # Firmware manifest (auto-generated)
├── firmware/                              # Firmware files directory
│   ├── EVSEPARKER_V2_GEN1/               # GEN1 hardware firmware
│   │   ├── EVSE_10_1_43.bin
│   │   └── EVSE_10_2_0.bin
│   ├── EVSEPARKER_V2_GEN2/               # GEN2 hardware firmware
│   │   ├── EVSE_10_2_0.bin
│   │   ├── EVSE_10_3_0.bin
│   │   └── EVSE_10_2_1_custom_ABCD.bin   # MAC-specific firmware (optional)
│   └── [OTHER_MODEL]/                    # Any other hardware models
│       └── EVSE_x_x_x.bin
├── update-manifest.py                     # Manifest updater script
└── update-all.sh                         # Simplified runner script
```

## 🔄 Workflow Examples

### Adding New Hardware Model

1. **Create new folder** in firmware directory:
   ```bash
   mkdir firmware/EVSEPARKER_V3_GEN1
   ```

2. **Add firmware files**:
   ```bash
   cp EVSE_10_4_0.bin firmware/EVSEPARKER_V3_GEN1/
   ```

3. **Update manifest**:
   ```bash
   ./update-all.sh
   ```

The script will automatically:
- Detect the new `EVSEPARKER_V3_GEN1` folder
- Create a new hardware model entry
- Add the firmware version to the manifest

### Adding New Firmware Version

1. **Upload firmware file** to appropriate model folder:
   ```bash
   cp EVSE_10_5_0.bin firmware/EVSEPARKER_V2_GEN2/
   ```

2. **Update manifest**:
   ```bash
   ./update-all.sh
   ```

3. **Verify the update**:
   ```bash
   cat manifest.json | grep -A 5 "10.5.0"
   ```

### Adding MAC-Specific Firmware

1. **Create custom firmware** with proper naming:
   ```bash
   # For device with MAC AB:CD:EF:12:34:56
   cp EVSE_10_2_1_bugfix.bin firmware/EVSEPARKER_V2_GEN2/EVSE_10_2_1_custom_ABCDEF123456.bin
   ```

2. **Update manifest**:
   ```bash
   python3 update-manifest.py
   ```

3. **Verify MAC targeting**:
   ```bash
   cat manifest.json | grep -A 10 "mac_specific"
   ```

## ⚠️ Important Notes

### Firmware Management
- **File Size**: Empty firmware files (0 bytes) are automatically skipped
- **Naming**: Stick to the naming convention `EVSE_x_x_x.bin` for automatic version detection
- **MAC Format**: MAC addresses must be exactly 12 hex characters for auto-detection
- **Backup**: Always backup your manifest.json before major changes

### Folder Structure
- **Model Names**: Folder names become hardware model IDs in the manifest
- **Display Names**: Folder names are converted to display names (underscores become spaces)
- **Dynamic Discovery**: No need to hardcode model names - script discovers them automatically

### Security
- **File Validation**: Scripts validate file formats before processing
- **Backup Preservation**: Existing MAC-specific entries are preserved unless --reset-mac is used
- **Path Validation**: All file paths are validated before writing

## 🐛 Troubleshooting

### Common Issues

**"No model directories found" error:**
```bash
# Check if firmware directory exists and has subdirectories
ls -la firmware/
```

**"Could not parse filename" warning:**
```bash
# Ensure firmware files follow naming convention
# Correct: EVSE_10_2_0.bin
# Incorrect: firmware_v10.2.0.bin
```

**"JSON parse error":**
```bash
# Validate JSON file
python3 -m json.tool manifest.json
```

### Recovery

**Restore manifest.json from backup:**
```bash
# If you have Git history
git checkout HEAD~1 -- manifest.json

# Or restore from manual backup
cp manifest.json.backup manifest.json
```

## 📊 Script Output Examples

### Successful Manifest Update
```
EVSEPARKER Firmware Manifest Updater
==================================================
Scanning firmware directories...
Found model directories: EVSEPARKER_V2_GEN1, EVSEPARKER_V2_GEN2

Processing EVSEPARKER_V2_GEN1...
Added firmware version 10.1.43 for EVSEPARKER_V2_GEN1
Added 1 firmware versions for EVSEPARKER_V2_GEN1

Processing EVSEPARKER_V2_GEN2...
Added firmware version 10.3.0 for EVSEPARKER_V2_GEN2
Added firmware version 10.2.0 for EVSEPARKER_V2_GEN2
Added 2 firmware versions for EVSEPARKER_V2_GEN2

Found 0 MAC-specific firmware entries

==================================================
Update completed successfully!
Hardware models: 2
MAC-specific entries: 0
```

### Generated Manifest Structure
```json
{
  "hardware_models": {
    "EVSEPARKER_V2_GEN1": {
      "name": "EVSEPARKER V2 GEN1",
      "description": "Hardware model EVSEPARKER_V2_GEN1",
      "firmware_versions": [
        {
          "version": "10.1.43",
          "url": "https://demirciberkan.github.io/firmware/EVSEPARKER_V2_GEN1/EVSE_10_1_43.bin",
          "description": "Stable release with improved safety features.",
          "release_date": "2025-09-26",
          "file_size": "1.15 MB"
        }
      ]
    }
  },
  "mac_specific": {},
  "last_updated": "2025-09-26T00:49:57.484431"
}
```

## 🚀 Deployment

### GitHub Pages Setup
1. Repository must be named `username.github.io`
2. Ensure all paths are relative or absolute GitHub Pages URLs
3. Test all functionality after deployment
4. Monitor for CORS issues with external resources

### Workflow
1. Drop firmware files in appropriate model folders: `firmware/MODEL_NAME/EVSE_x_x_x.bin`
2. Run `./update-all.sh`
3. The script automatically updates `manifest.json`
4. For MAC-specific firmware, use naming: `EVSE_version_custom_MACADDRESS.bin`

The automation system provides a simple, maintainable way to manage firmware releases without manual manifest editing! 🎉