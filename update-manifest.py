#!/usr/bin/env python3
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
        self.manifest = self._load_existing_manifest()

    def _load_existing_manifest(self):
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _get_firmware_description(self, model, version):
        try:
            for fw in self.manifest.get("hardware_models", {}).get(model, {}).get("firmware_versions", []):
                if fw.get("version") == version:
                    return fw.get("description", f"Firmware version {version}")
        except (AttributeError, TypeError):
            pass
        return f"Firmware version {version}"

    def _parse_firmware_filename(self, filename):
        name, _ = os.path.splitext(filename)
        # EVSE_10_2_1_custom_ABCDEF123456
        custom_match = re.match(r'EVSE_(\d+)\.(\d+)\.(\d+)_custom_(.+)', name)
        if custom_match:
            major, minor, patch, identifier = custom_match.groups()
            version = f"{major}.{minor}.{patch}"
            return {
                'version': version,
                'is_custom': True,
                'custom_identifier': identifier
            }
        # EVSE_10.2.0
        regular_match = re.match(r'EVSE_(\d+)\.(\d+)\.(\d+)', name)
        if regular_match:
            major, minor, patch = regular_match.groups()
            version = f"{major}.{minor}.{patch}"
            return {
                'version': version,
                'is_custom': False
            }
        return None

    def _get_file_info(self, filepath):
        stat = filepath.stat()
        size_mb = stat.st_size / (1024 * 1024)
        mod_time = datetime.fromtimestamp(stat.st_mtime)
        return {
            'size': f"{size_mb:.2f} MB",
            'modified': mod_time.strftime("%Y-%m-%d")
        }

    def generate_manifest(self):
        new_manifest = {
            "hardware_models": {},
            "mac_specific": {},
            "last_updated": datetime.now().isoformat()
        }

        if not self.firmware_dir.exists():
            print(f"Warning: Firmware directory '{self.firmware_dir}' does not exist.")
            return new_manifest

        for model_dir in self.firmware_dir.iterdir():
            if not model_dir.is_dir():
                continue

            model_name = model_dir.name
            new_manifest["hardware_models"][model_name] = {
                "name": model_name.replace('_', ' '),
                "description": f"Hardware model {model_name}",
                "firmware_versions": []
            }

            for firmware_file in model_dir.glob("*.bin"):
                if firmware_file.stat().st_size == 0:
                    print(f"Skipping empty file: {firmware_file.name}")
                    continue

                parsed_info = self._parse_firmware_filename(firmware_file.name)
                if not parsed_info:
                    print(f"Warning: Could not parse filename {firmware_file.name}")
                    continue

                file_info = self._get_file_info(firmware_file)
                firmware_url = f"{self.base_url}/firmware/{model_name}/{firmware_file.name}"

                if parsed_info['is_custom']:
                    identifier = parsed_info['custom_identifier']
                    if len(identifier) >= 12:
                        hex_part = identifier[-12:]
                        if re.match(r'^[A-Fa-f0-9]{12}$', hex_part):
                            mac = ':'.join([hex_part[i:i+2] for i in range(0, 12, 2)]).upper()
                            new_manifest["mac_specific"][mac] = {
                                "model": model_name,
                                "version": f"{parsed_info['version']}-custom",
                                "url": firmware_url,
                                "description": f"Custom firmware for device {identifier}",
                                "release_date": file_info['modified'],
                                "file_size": file_info['size']
                            }
                else:
                    description = self._get_firmware_description(model_name, parsed_info['version'])
                    new_manifest["hardware_models"][model_name]["firmware_versions"].append({
                        "version": parsed_info['version'],
                        "url": firmware_url,
                        "description": description,
                        "release_date": file_info['modified'],
                        "file_size": file_info['size']
                    })

            # Sort firmware versions
            new_manifest["hardware_models"][model_name]["firmware_versions"].sort(
                key=lambda x: [int(v) for v in x['version'].split('.')], reverse=True
            )

        return new_manifest

    def save_manifest(self, manifest):
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"Manifest saved to {self.manifest_file}")

def main():
    parser = argparse.ArgumentParser(description='Update EVSEPARKER firmware manifest')
    parser.add_argument('--base-url', default='https://demirciberkan.github.io',
                       help='Base URL for firmware downloads')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without writing files')
    args = parser.parse_args()

    updater = ManifestUpdater(args.base_url)
    new_manifest = updater.generate_manifest()

    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")
        print("\nGenerated manifest preview:")
        print(json.dumps(new_manifest, indent=2))
    else:
        updater.save_manifest(new_manifest)
        print("Manifest update completed successfully!")

if __name__ == "__main__":
    main()
