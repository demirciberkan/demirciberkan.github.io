#!/usr/bin/env python3
"""
EVSEPARKER Firmware Manifest Auto-Updater

This script automatically scans firmware directories and updates manifest.json
with the latest firmware information based on file naming conventions.

Usage: python3 update-manifest.py [options]

File naming convention:
- EVSE_[version].bin (e.g., EVSE_10_2_0.bin for version 10.2.0)
- EVSE_[version]_custom_[identifier].bin (for MAC-specific firmware)

Directory structure:
firmware/
├── EVSEPARKER_V2_GEN1/
│   ├── EVSE_10_1_43.bin
│   ├── EVSE_10_2_0.bin
│   └── EVSE_10_2_1_custom_ABCDEF123456.bin
└── EVSEPARKER_V2_GEN2/
    ├── EVSE_10_1_43.bin
    └── EVSE_10_2_0.bin
"""

import os
import json
import re
import argparse
from datetime import datetime
from pathlib import Path

class ManifestUpdater:
    def __init__(self, base_url="https://demirciberkan.github.io"):
        self.base_url = base_url
        self.firmware_dir = Path("firmware")
        self.manifest_file = Path("manifest.json")

    def parse_firmware_filename(self, filename):
        """
        Parse firmware filename to extract version and metadata

        Examples:
        - EVSE_10_2_0.bin -> version: 10.2.0, is_custom: False
        - EVSE_10_2_1_custom_ABCDEF123456.bin -> version: 10.2.1, is_custom: True, identifier: ABCDEF123456
        """
        # Remove .bin extension
        name = filename.replace('.bin', '')

        # Check if it's a custom firmware
        if '_custom_' in name:
            # Pattern: EVSE_10_2_1_custom_ABCDEF123456
            match = re.match(r'EVSE_(\d+)_(\d+)_(\d+)_custom_(.+)', name)
            if match:
                major, minor, patch, identifier = match.groups()
                return {
                    'version': f"{major}.{minor}.{patch}",
                    'is_custom': True,
                    'custom_identifier': identifier
                }
        else:
            # Pattern: EVSE_10_2_0
            match = re.match(r'EVSE_(\d+)_(\d+)_(\d+)', name)
            if match:
                major, minor, patch = match.groups()
                return {
                    'version': f"{major}.{minor}.{patch}",
                    'is_custom': False
                }

        return None

    def get_file_info(self, filepath):
        """Get file size and modification date"""
        stat = filepath.stat()
        size_mb = stat.st_size / (1024 * 1024)
        mod_time = datetime.fromtimestamp(stat.st_mtime)

        return {
            'size': f"{size_mb:.2f} MB",
            'modified': mod_time.strftime("%Y-%m-%d")
        }

    def scan_firmware_directory(self, model_name):
        """Scan a specific model directory for firmware files"""
        model_path = self.firmware_dir / model_name

        if not model_path.exists():
            print(f"Warning: Directory {model_path} does not exist")
            return [], []

        firmware_versions = []
        mac_specific = {}

        # Scan all .bin files
        for bin_file in model_path.glob("*.bin"):
            if bin_file.stat().st_size == 0:  # Skip empty files
                print(f"Skipping empty file: {bin_file.name}")
                continue

            parsed = self.parse_firmware_filename(bin_file.name)
            if not parsed:
                print(f"Warning: Could not parse filename {bin_file.name}")
                continue

            file_info = self.get_file_info(bin_file)
            firmware_url = f"{self.base_url}/firmware/{model_name}/{bin_file.name}"

            if parsed['is_custom']:
                # This is MAC-specific firmware
                # Try to extract MAC from identifier (last 12 chars formatted as MAC)
                identifier = parsed['custom_identifier']
                if len(identifier) >= 12:
                    # Convert identifier to MAC format if it looks like hex
                    hex_part = identifier[-12:]
                    if re.match(r'^[A-Fa-f0-9]{12}$', hex_part):
                        mac = ':'.join([hex_part[i:i+2] for i in range(0, 12, 2)]).upper()
                        mac_specific[mac] = {
                            "model": model_name,
                            "version": f"{parsed['version']}-custom",
                            "url": firmware_url,
                            "description": f"Custom firmware for device {identifier}",
                            "release_date": file_info['modified'],
                            "file_size": file_info['size']
                        }
                        print(f"Added MAC-specific firmware for {mac}: v{parsed['version']}")
                    else:
                        print(f"Warning: Custom firmware {bin_file.name} has invalid identifier format")
            else:
                # Regular firmware version
                firmware_versions.append({
                    "version": parsed['version'],
                    "url": firmware_url,
                    "description": f"Firmware version {parsed['version']}",
                    "release_date": file_info['modified'],
                    "file_size": file_info['size']
                })
                print(f"Added firmware version {parsed['version']} for {model_name}")

        # Sort firmware versions by version number (newest first)
        firmware_versions.sort(key=lambda x: [int(v) for v in x['version'].split('.')], reverse=True)

        return firmware_versions, mac_specific

    def update_descriptions(self, firmware_versions):
        """Add meaningful descriptions based on version numbers"""
        version_descriptions = {
            "10.2.0": "Enhanced OTA protocol. Fixed BLE connectivity issues.",
            "10.1.43": "Stable release with improved safety features.",
            "10.1.42": "Bug fixes and performance improvements.",
            "10.0.0": "Initial release version."
        }

        for fw in firmware_versions:
            if fw['version'] in version_descriptions:
                fw['description'] = version_descriptions[fw['version']]

        return firmware_versions

    def get_model_directories(self):
        """Scan firmware directory and return all subdirectories as model names"""
        if not self.firmware_dir.exists():
            print(f"Warning: Firmware directory {self.firmware_dir} does not exist")
            return []

        model_dirs = []
        for item in self.firmware_dir.iterdir():
            if item.is_dir():
                model_dirs.append(item.name)

        return sorted(model_dirs)

    def generate_manifest(self):
        """Generate complete manifest.json from firmware directories"""
        manifest = {
            "hardware_models": {},
            "mac_specific": {},
            "last_updated": datetime.now().isoformat()
        }

        print("Scanning firmware directories...")

        # Get all model directories dynamically
        model_directories = self.get_model_directories()

        if not model_directories:
            print("No model directories found in firmware folder")
            return manifest

        print(f"Found model directories: {', '.join(model_directories)}")

        for model_name in model_directories:
            print(f"\nProcessing {model_name}...")

            firmware_versions, mac_specific = self.scan_firmware_directory(model_name)

            if firmware_versions:
                # Update descriptions with meaningful text
                firmware_versions = self.update_descriptions(firmware_versions)

                manifest["hardware_models"][model_name] = {
                    "name": model_name.replace('_', ' '),  # Convert folder name to display name
                    "description": f"Hardware model {model_name}",
                    "firmware_versions": firmware_versions
                }
                print(f"Added {len(firmware_versions)} firmware versions for {model_name}")
            else:
                print(f"No valid firmware found for {model_name}")

            # Add MAC-specific firmware
            manifest["mac_specific"].update(mac_specific)

        print(f"\nFound {len(manifest['mac_specific'])} MAC-specific firmware entries")
        return manifest

    def load_existing_manifest(self):
        """Load existing manifest to preserve MAC-specific entries"""
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print("Warning: Could not load existing manifest, creating new one")
        return {"mac_specific": {}}

    def merge_mac_specific(self, new_manifest, existing_manifest):
        """Merge MAC-specific entries, keeping manually added ones"""
        existing_mac = existing_manifest.get("mac_specific", {})
        new_mac = new_manifest.get("mac_specific", {})

        # Start with existing MAC entries
        merged_mac = existing_mac.copy()

        # Add new MAC entries from scanned files
        for mac, info in new_mac.items():
            merged_mac[mac] = info

        new_manifest["mac_specific"] = merged_mac
        return new_manifest

    def save_manifest(self, manifest):
        """Save manifest to file with pretty formatting"""
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"\nManifest saved to {self.manifest_file}")

    def update(self, preserve_mac_entries=True):
        """Main update function"""
        print("EVSEPARKER Firmware Manifest Updater")
        print("=" * 50)

        # Load existing manifest if preserving MAC entries
        existing_manifest = {}
        if preserve_mac_entries:
            existing_manifest = self.load_existing_manifest()

        # Generate new manifest
        new_manifest = self.generate_manifest()

        # Merge MAC-specific entries
        if preserve_mac_entries:
            new_manifest = self.merge_mac_specific(new_manifest, existing_manifest)

        # Save updated manifest
        self.save_manifest(new_manifest)

        print("\n" + "=" * 50)
        print("Update completed successfully!")
        print(f"Hardware models: {len(new_manifest['hardware_models'])}")
        print(f"MAC-specific entries: {len(new_manifest['mac_specific'])}")

def main():
    parser = argparse.ArgumentParser(description='Update EVSEPARKER firmware manifest')
    parser.add_argument('--base-url', default='https://demirciberkan.github.io',
                       help='Base URL for firmware downloads')
    parser.add_argument('--reset-mac', action='store_true',
                       help='Reset MAC-specific entries (remove manually added ones)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without writing files')

    args = parser.parse_args()

    updater = ManifestUpdater(args.base_url)

    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")
        manifest = updater.generate_manifest()
        print("\nGenerated manifest preview:")
        print(json.dumps(manifest, indent=2))
    else:
        updater.update(preserve_mac_entries=not args.reset_mac)

if __name__ == "__main__":
    main()