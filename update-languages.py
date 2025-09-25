#!/usr/bin/env python3
"""
EVSEPARKER Language File Updater

This script helps manage language files for the React Native app.
It can:
1. Sync missing keys between language files
2. Add new translation keys
3. Validate translation file structure
4. Generate translation reports

Usage: python3 update-languages.py [options]

Directory structure:
../App/EVSEPARKER_rn/EVSEPARKER_OTA/translations/
├── en.json (English - master language)
├── tr.json (Turkish)
└── [other language files]
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
import difflib

class LanguageUpdater:
    def __init__(self, translations_dir=None):
        if translations_dir:
            self.translations_dir = Path(translations_dir)
        else:
            # Default path relative to current script
            self.translations_dir = Path("../App/EVSEPARKER_rn/EVSEPARKER_OTA/translations/")

        self.master_language = "en"  # English is the master language
        self.supported_languages = ["en", "tr"]  # Add more as needed

    def load_language_file(self, language_code):
        """Load a language JSON file"""
        file_path = self.translations_dir / f"{language_code}.json"

        if not file_path.exists():
            print(f"Warning: Language file {file_path} does not exist")
            return {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error loading {file_path}: {e}")
            return {}

    def save_language_file(self, language_code, data):
        """Save a language JSON file with proper formatting"""
        file_path = self.translations_dir / f"{language_code}.json"

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
            print(f"Saved {file_path}")
            return True
        except Exception as e:
            print(f"Error saving {file_path}: {e}")
            return False

    def get_all_keys(self, data, prefix=""):
        """Recursively get all translation keys from nested JSON"""
        keys = []

        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                keys.extend(self.get_all_keys(value, full_key))
            else:
                keys.append(full_key)

        return keys

    def set_nested_value(self, data, key_path, value):
        """Set a value in nested dictionary using dot notation"""
        keys = key_path.split('.')
        current = data

        # Navigate to the parent
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # Set the final value
        current[keys[-1]] = value

    def get_nested_value(self, data, key_path, default=""):
        """Get a value from nested dictionary using dot notation"""
        keys = key_path.split('.')
        current = data

        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default

    def find_missing_keys(self, master_data, target_data):
        """Find keys that exist in master but missing in target"""
        master_keys = set(self.get_all_keys(master_data))
        target_keys = set(self.get_all_keys(target_data))

        return master_keys - target_keys

    def find_extra_keys(self, master_data, target_data):
        """Find keys that exist in target but not in master"""
        master_keys = set(self.get_all_keys(master_data))
        target_keys = set(self.get_all_keys(target_data))

        return target_keys - master_keys

    def sync_language_files(self, dry_run=False):
        """Sync all language files with the master language"""
        print(f"Syncing language files with master ({self.master_language})")
        print("=" * 60)

        # Load master language
        master_data = self.load_language_file(self.master_language)
        if not master_data:
            print(f"Error: Could not load master language file ({self.master_language}.json)")
            return False

        master_keys = self.get_all_keys(master_data)
        print(f"Master language ({self.master_language}) has {len(master_keys)} keys")

        # Process each supported language
        for lang_code in self.supported_languages:
            if lang_code == self.master_language:
                continue  # Skip master language

            print(f"\n--- Processing {lang_code}.json ---")

            # Load target language
            target_data = self.load_language_file(lang_code)

            # Find missing and extra keys
            missing_keys = self.find_missing_keys(master_data, target_data)
            extra_keys = self.find_extra_keys(master_data, target_data)

            print(f"Missing keys: {len(missing_keys)}")
            print(f"Extra keys: {len(extra_keys)}")

            if missing_keys:
                print("Missing keys:")
                for key in sorted(missing_keys):
                    master_value = self.get_nested_value(master_data, key)
                    print(f"  {key}: '{master_value}'")

                    if not dry_run:
                        # Add missing key with master language value as placeholder
                        placeholder = f"[{lang_code.upper()}] {master_value}"
                        self.set_nested_value(target_data, key, placeholder)

            if extra_keys:
                print("Extra keys (consider removing):")
                for key in sorted(extra_keys):
                    extra_value = self.get_nested_value(target_data, key)
                    print(f"  {key}: '{extra_value}'")

            # Save updated file
            if not dry_run and missing_keys:
                self.save_language_file(lang_code, target_data)
                print(f"Updated {lang_code}.json with {len(missing_keys)} new keys")
            elif missing_keys:
                print(f"DRY RUN: Would add {len(missing_keys)} keys to {lang_code}.json")

        return True

    def add_translation_key(self, key_path, english_text, translations=None):
        """Add a new translation key to all language files"""
        print(f"Adding new translation key: {key_path}")
        print(f"English text: {english_text}")

        if translations is None:
            translations = {}

        # Load and update master language
        master_data = self.load_language_file(self.master_language)
        self.set_nested_value(master_data, key_path, english_text)
        self.save_language_file(self.master_language, master_data)

        # Update other languages
        for lang_code in self.supported_languages:
            if lang_code == self.master_language:
                continue

            lang_data = self.load_language_file(lang_code)

            if lang_code in translations:
                translation_text = translations[lang_code]
            else:
                # Use placeholder with English text
                translation_text = f"[{lang_code.upper()}] {english_text}"

            self.set_nested_value(lang_data, key_path, translation_text)
            self.save_language_file(lang_code, lang_data)

            print(f"Added to {lang_code}.json: {translation_text}")

    def validate_language_files(self):
        """Validate all language files for structure and completeness"""
        print("Validating language files...")
        print("=" * 40)

        master_data = self.load_language_file(self.master_language)
        if not master_data:
            print("Error: Cannot validate without master language file")
            return False

        master_keys = set(self.get_all_keys(master_data))
        validation_results = {}

        for lang_code in self.supported_languages:
            lang_data = self.load_language_file(lang_code)
            lang_keys = set(self.get_all_keys(lang_data))

            # Calculate completeness
            missing = master_keys - lang_keys
            extra = lang_keys - master_keys
            completeness = (len(lang_keys & master_keys) / len(master_keys)) * 100

            # Check for placeholder texts
            placeholders = []
            for key in lang_keys:
                value = self.get_nested_value(lang_data, key)
                if isinstance(value, str) and value.startswith(f"[{lang_code.upper()}]"):
                    placeholders.append(key)

            validation_results[lang_code] = {
                'completeness': completeness,
                'missing_keys': len(missing),
                'extra_keys': len(extra),
                'placeholders': len(placeholders),
                'total_keys': len(lang_keys)
            }

            print(f"{lang_code}.json:")
            print(f"  Completeness: {completeness:.1f}%")
            print(f"  Total keys: {len(lang_keys)}")
            print(f"  Missing: {len(missing)}")
            print(f"  Extra: {len(extra)}")
            print(f"  Placeholders: {len(placeholders)}")
            print()

        return validation_results

    def generate_translation_report(self, output_file="translation-report.md"):
        """Generate a markdown report of translation status"""
        print(f"Generating translation report: {output_file}")

        master_data = self.load_language_file(self.master_language)
        master_keys = self.get_all_keys(master_data)

        report_lines = [
            "# EVSEPARKER Translation Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"## Summary",
            f"Total translation keys: {len(master_keys)}",
            f"Supported languages: {', '.join(self.supported_languages)}",
            ""
        ]

        # Language-specific sections
        for lang_code in self.supported_languages:
            lang_data = self.load_language_file(lang_code)
            lang_keys = set(self.get_all_keys(lang_data))

            missing = self.find_missing_keys(master_data, lang_data)
            extra = self.find_extra_keys(master_data, lang_data)
            completeness = (len(lang_keys & set(master_keys)) / len(master_keys)) * 100

            # Count placeholders
            placeholders = []
            for key in lang_keys:
                value = self.get_nested_value(lang_data, key)
                if isinstance(value, str) and value.startswith(f"[{lang_code.upper()}]"):
                    placeholders.append(key)

            report_lines.extend([
                f"## {lang_code.upper()} Language",
                f"- **Completeness**: {completeness:.1f}%",
                f"- **Total keys**: {len(lang_keys)}",
                f"- **Missing keys**: {len(missing)}",
                f"- **Extra keys**: {len(extra)}",
                f"- **Untranslated (placeholders)**: {len(placeholders)}",
                ""
            ])

            if missing:
                report_lines.extend([
                    "### Missing Keys:",
                    "```"
                ])
                for key in sorted(missing):
                    report_lines.append(f"{key}")
                report_lines.extend(["```", ""])

            if placeholders:
                report_lines.extend([
                    "### Untranslated Keys:",
                    "```"
                ])
                for key in sorted(placeholders):
                    report_lines.append(f"{key}")
                report_lines.extend(["```", ""])

        # Write report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))

        print(f"Report saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Update EVSEPARKER language files')
    parser.add_argument('--translations-dir',
                       help='Path to translations directory')
    parser.add_argument('--sync', action='store_true',
                       help='Sync all language files with master language')
    parser.add_argument('--validate', action='store_true',
                       help='Validate language files')
    parser.add_argument('--report', action='store_true',
                       help='Generate translation report')
    parser.add_argument('--add-key',
                       help='Add new translation key (format: section.key)')
    parser.add_argument('--english-text',
                       help='English text for new key (use with --add-key)')
    parser.add_argument('--turkish-text',
                       help='Turkish text for new key (use with --add-key)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without modifying files')

    args = parser.parse_args()

    updater = LanguageUpdater(args.translations_dir)

    # Verify translations directory exists
    if not updater.translations_dir.exists():
        print(f"Error: Translations directory not found: {updater.translations_dir}")
        print("Please specify the correct path with --translations-dir")
        return 1

    if args.add_key:
        if not args.english_text:
            print("Error: --english-text is required when adding a key")
            return 1

        translations = {}
        if args.turkish_text:
            translations['tr'] = args.turkish_text

        updater.add_translation_key(args.add_key, args.english_text, translations)

    elif args.sync:
        updater.sync_language_files(dry_run=args.dry_run)

    elif args.validate:
        updater.validate_language_files()

    elif args.report:
        updater.generate_translation_report()

    else:
        # Default: show status
        print("EVSEPARKER Language File Manager")
        print("=" * 40)
        updater.validate_language_files()
        print("\nUse --help to see available options")

    return 0

if __name__ == "__main__":
    exit(main())