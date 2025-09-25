# EVSEPARKER Automation Scripts

This directory contains automation scripts for managing firmware and language files in the EVSEPARKER project.

## 🚀 Quick Start

```bash
# Update both manifest and language files
./update-all.sh

# Preview changes without modifying files
./update-all.sh --dry-run

# Update only manifest.json
./update-all.sh --skip-languages

# Generate translation report
./update-all.sh --report
```

## 📜 Available Scripts

### 1. `update-manifest.py` - Firmware Manifest Updater

Automatically scans firmware directories and updates `manifest.json` based on file naming conventions.

**Features:**
- Scans firmware files and extracts version information
- Generates URLs for firmware downloads
- Handles MAC-specific firmware targeting
- Preserves manually added MAC entries
- Sorts versions chronologically (newest first)

**File Naming Convention:**
```
# Standard firmware
EVSE_10_2_0.bin          → version 10.2.0

# MAC-specific firmware
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

### 2. `update-languages.py` - Language File Manager

Manages translation files for the React Native app, ensuring all languages stay synchronized.

**Features:**
- Validates translation file completeness
- Syncs missing keys between language files
- Adds placeholder translations for missing keys
- Generates detailed translation reports
- Handles nested JSON structure with dot notation

**Usage:**
```bash
# Show validation status
python3 update-languages.py --validate

# Sync all languages with master (English)
python3 update-languages.py --sync

# Generate detailed translation report
python3 update-languages.py --report

# Add new translation key
python3 update-languages.py --add-key "settings.newFeature" --english-text "New Feature" --turkish-text "Yeni Özellik"

# Specify custom translations directory
python3 update-languages.py --translations-dir /path/to/translations --validate
```

### 3. `update-all.sh` - Combined Runner Script

Runs both manifest and language updates in a single command with colored output and comprehensive error handling.

**Features:**
- Runs both updates with single command
- Colored output for better readability
- Dry-run mode for preview
- Comprehensive error handling
- Flexible options for selective updates

**Usage:**
```bash
# Full update (recommended)
./update-all.sh

# Preview what would be changed
./update-all.sh --dry-run

# Update only manifest
./update-all.sh --skip-languages

# Update only languages
./update-all.sh --skip-manifest

# Generate translation report
./update-all.sh --report

# Custom settings
./update-all.sh --base-url https://yourdomain.com --translations-dir /custom/path
```

## 📁 Directory Structure

The scripts expect the following directory structure:

```
demirciberkan.github.io/
├── manifest.json                           # Firmware manifest (auto-updated)
├── firmware/                              # Firmware files directory
│   ├── EVSEPARKER_V2_GEN1/               # GEN1 hardware firmware
│   │   ├── EVSE_10_1_43.bin
│   │   ├── EVSE_10_2_0.bin
│   │   └── EVSE_10_2_1_custom_ABCD.bin   # MAC-specific firmware
│   └── EVSEPARKER_V2_GEN2/               # GEN2 hardware firmware
│       ├── EVSE_10_1_43.bin
│       └── EVSE_10_2_0.bin
├── update-manifest.py                     # Manifest updater script
├── update-languages.py                    # Language updater script
├── update-all.sh                         # Combined runner script
└── ../App/EVSEPARKER_rn/EVSEPARKER_OTA/translations/  # Language files
    ├── en.json                           # English (master language)
    └── tr.json                           # Turkish
```

## 🔄 Workflow Examples

### Adding New Firmware

1. **Upload firmware file** to appropriate model directory:
   ```bash
   cp EVSE_10_2_1.bin firmware/EVSEPARKER_V2_GEN2/
   ```

2. **Update manifest automatically**:
   ```bash
   ./update-all.sh --skip-languages
   ```

3. **Verify the update**:
   ```bash
   # Check that manifest.json was updated with new version
   cat manifest.json | grep -A 5 "10.2.1"
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
   # Check that manifest.json has MAC-specific entry
   cat manifest.json | grep -A 10 "mac_specific"
   ```

### Adding New Translation

1. **Add English text** first:
   ```bash
   python3 update-languages.py --add-key "errors.E_NEW_ERROR" --english-text "New Error Type"
   ```

2. **Add Turkish translation**:
   ```bash
   python3 update-languages.py --add-key "errors.E_NEW_ERROR" --english-text "New Error Type" --turkish-text "Yeni Hata Tipi"
   ```

3. **Validate all languages**:
   ```bash
   python3 update-languages.py --validate
   ```

### Weekly Maintenance

Run the complete update to ensure everything is synchronized:

```bash
# Preview changes
./update-all.sh --dry-run

# Apply updates if everything looks good
./update-all.sh

# Generate translation report for review
./update-all.sh --report
```

## ⚠️ Important Notes

### Firmware Management
- **File Size**: Empty firmware files (0 bytes) are automatically skipped
- **Naming**: Stick to the naming convention for automatic version detection
- **MAC Format**: MAC addresses must be exactly 12 hex characters for auto-detection
- **Backup**: Always backup your manifest.json before major changes

### Language Management
- **Master Language**: English (en.json) is the master - add new keys here first
- **Placeholders**: Missing translations get placeholder text like `[TR] English Text`
- **Structure**: Maintain the nested JSON structure when adding keys
- **Encoding**: All files are saved with UTF-8 encoding

### Security
- **File Validation**: Scripts validate file formats before processing
- **Backup Preservation**: Existing MAC-specific entries are preserved unless --reset-mac is used
- **Path Validation**: All file paths are validated before writing

## 🐛 Troubleshooting

### Common Issues

**"Directory not found" error:**
```bash
# Check if directories exist
ls -la firmware/
ls -la ../App/EVSEPARKER_rn/EVSEPARKER_OTA/translations/
```

**"Could not parse filename" warning:**
```bash
# Ensure firmware files follow naming convention
# Correct: EVSE_10_2_0.bin
# Incorrect: firmware_v10.2.0.bin
```

**"JSON parse error":**
```bash
# Validate JSON files
python3 -m json.tool manifest.json
python3 -m json.tool ../App/EVSEPARKER_rn/EVSEPARKER_OTA/translations/en.json
```

**Language sync issues:**
```bash
# Check file permissions
ls -la ../App/EVSEPARKER_rn/EVSEPARKER_OTA/translations/

# Run validation to see specific issues
python3 update-languages.py --validate
```

### Recovery

**Restore manifest.json from backup:**
```bash
# If you have Git history
git checkout HEAD~1 -- manifest.json

# Or restore from manual backup
cp manifest.json.backup manifest.json
```

**Reset language files:**
```bash
# Restore from Git (if available)
git checkout HEAD -- ../App/EVSEPARKER_rn/EVSEPARKER_OTA/translations/

# Or sync again
python3 update-languages.py --sync
```

## 📊 Script Output Examples

### Successful Manifest Update
```
EVSEPARKER Firmware Manifest Updater
==================================================
Scanning firmware directories...

Processing EVSEPARKER_V2_GEN1...
Added firmware version 10.2.0 for EVSEPARKER_V2_GEN1
Added firmware version 10.1.43 for EVSEPARKER_V2_GEN1
Added 2 firmware versions for EVSEPARKER_V2_GEN1

Processing EVSEPARKER_V2_GEN2...
Added MAC-specific firmware for AB:CD:EF:12:34:56: v10.2.1
Added firmware version 10.2.0 for EVSEPARKER_V2_GEN2
Added 1 firmware versions for EVSEPARKER_V2_GEN2

Found 1 MAC-specific firmware entries

==================================================
Update completed successfully!
Hardware models: 2
MAC-specific entries: 1
```

### Language Validation Output
```
Validating language files...
========================================
en.json:
  Completeness: 100.0%
  Total keys: 189
  Missing: 0
  Extra: 0
  Placeholders: 0

tr.json:
  Completeness: 95.2%
  Total keys: 180
  Missing: 9
  Extra: 0
  Placeholders: 5
```

This automation system will save you significant time when managing firmware releases and translations! 🚀