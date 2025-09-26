# EVSEPARKER Firmware File Locations

This document tracks the locations of firmware files in the project structure.

## Current Structure

### Web Distribution Firmware
**Location**: `/home/berkan/Documents/KiCad/8.0/projects/evse_s_v5/demirciberkan.github.io/firmware/`
```
firmware/
├── EVSEPARKER_V2_GEN1/
│   └── EVSE_x_x_x.bin
├── EVSEPARKER_V2_GEN2/
│   └── EVSE_x_x_x.bin
└── [OTHER_MODELS]/
    └── EVSE_x_x_x.bin
```
**Purpose**: Files served via GitHub Pages for OTA downloads
**Managed by**: `update-manifest.py` script
**URL Format**: `https://demirciberkan.github.io/firmware/MODEL/EVSE_x_x_x.bin`

### ESP32 Source Firmware
**Location**: `/home/berkan/Documents/KiCad/8.0/projects/evse_s_v5/Firmware/EVSE_10.2.0/`
```
Firmware/
└── EVSE_10.2.0/
    ├── EVSE_10_2_0.ino          # Main firmware source
    ├── *.h                      # Header files
    ├── *.cpp                    # Source files
    └── build/                   # Compiled binaries
```
**Purpose**: Arduino/ESP32 source code and build artifacts
**Contains**:
- Source code files (.ino, .h, .cpp)
- Build configurations
- Compiled .bin files for deployment

## Workflow

1. **Development**:
   - Edit source code in `/Firmware/EVSE_10.2.0/`
   - Compile using Arduino IDE or CLI

2. **Build**:
   - Generate .bin files in build directory
   - Test firmware locally

3. **Distribution**:
   - Copy compiled .bin files to appropriate `/firmware/MODEL/` directory
   - Run `./update-all.sh` to update manifest.json
   - Commit and push to GitHub Pages

## File Naming Convention

**Source Files**:
- `EVSE_10_2_0.ino` (Arduino sketch)
- Version format: `MAJOR_MINOR_PATCH`

**Binary Files**:
- `EVSE_10_2_0.bin` (compiled firmware)
- `EVSE_10_2_1_custom_MACADDR.bin` (MAC-specific versions)

## Notes

- **Updated**: 2025-09-26
- **Previous Location**: Firmware was previously in different directory structure
- **Migration**: ESP32 source files consolidated to `/Firmware/EVSE_10.2.0/`
- **Version**: Currently working with firmware version 10.2.0