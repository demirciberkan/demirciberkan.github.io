#!/bin/bash
#
# EVSEPARKER Update Scripts Runner
#
# This script runs both the manifest updater and language file updater
# Usage: ./update-all.sh [options]
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default paths
TRANSLATIONS_DIR="../App/EVSEPARKER_rn/EVSEPARKER_OTA/translations/"
BASE_URL="https://demirciberkan.github.io"

# Parse command line arguments
DRY_RUN=false
SKIP_MANIFEST=false
SKIP_LANGUAGES=false
GENERATE_REPORT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --skip-manifest)
            SKIP_MANIFEST=true
            shift
            ;;
        --skip-languages)
            SKIP_LANGUAGES=true
            shift
            ;;
        --report)
            GENERATE_REPORT=true
            shift
            ;;
        --base-url)
            BASE_URL="$2"
            shift 2
            ;;
        --translations-dir)
            TRANSLATIONS_DIR="$2"
            shift 2
            ;;
        --help|-h)
            echo "EVSEPARKER Update Scripts Runner"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --dry-run              Show what would be updated without making changes"
            echo "  --skip-manifest        Skip manifest.json update"
            echo "  --skip-languages       Skip language files update"
            echo "  --report               Generate translation report"
            echo "  --base-url URL         Base URL for firmware downloads (default: https://demirciberkan.github.io)"
            echo "  --translations-dir DIR Path to translations directory"
            echo "  --help, -h             Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                     # Update both manifest and languages"
            echo "  $0 --dry-run           # Show what would be updated"
            echo "  $0 --skip-languages    # Update only manifest"
            echo "  $0 --report            # Generate translation report"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Function to print colored status messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "\n${BLUE}================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}================================${NC}\n"
}

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not found"
    exit 1
fi

# Main execution
print_header "EVSEPARKER Automated Update"

if [ "$DRY_RUN" = true ]; then
    print_warning "DRY RUN MODE - No files will be modified"
    echo
fi

# Update manifest.json
if [ "$SKIP_MANIFEST" = false ]; then
    print_header "Updating Firmware Manifest"

    if [ "$DRY_RUN" = true ]; then
        python3 update-manifest.py --base-url "$BASE_URL" --dry-run
    else
        python3 update-manifest.py --base-url "$BASE_URL"
        if [ $? -eq 0 ]; then
            print_success "Manifest updated successfully"
        else
            print_error "Manifest update failed"
            exit 1
        fi
    fi
else
    print_warning "Skipping manifest update (--skip-manifest)"
fi

# Update language files
if [ "$SKIP_LANGUAGES" = false ]; then
    print_header "Validating Language Files"

    # Check if translations directory exists
    if [ ! -d "$TRANSLATIONS_DIR" ]; then
        print_error "Translations directory not found: $TRANSLATIONS_DIR"
        print_status "You can specify a different path with --translations-dir"
        exit 1
    fi

    # Validate language files
    python3 update-languages.py --translations-dir "$TRANSLATIONS_DIR" --validate

    if [ $? -eq 0 ]; then
        print_success "Language validation completed"
    else
        print_error "Language validation failed"
        exit 1
    fi

    # Sync language files if not dry run
    if [ "$DRY_RUN" = false ]; then
        print_status "Syncing language files..."
        python3 update-languages.py --translations-dir "$TRANSLATIONS_DIR" --sync

        if [ $? -eq 0 ]; then
            print_success "Language sync completed"
        else
            print_warning "Language sync had issues (check output above)"
        fi
    fi
else
    print_warning "Skipping language update (--skip-languages)"
fi

# Generate translation report if requested
if [ "$GENERATE_REPORT" = true ]; then
    print_header "Generating Translation Report"

    python3 update-languages.py --translations-dir "$TRANSLATIONS_DIR" --report

    if [ $? -eq 0 ]; then
        print_success "Translation report generated: translation-report.md"
    else
        print_error "Failed to generate translation report"
        exit 1
    fi
fi

# Final summary
print_header "Update Summary"

if [ "$DRY_RUN" = true ]; then
    print_status "Dry run completed - no files were modified"
    print_status "Run without --dry-run to apply changes"
else
    print_success "All updates completed successfully!"

    echo "Files updated:"
    [ "$SKIP_MANIFEST" = false ] && echo "  ✓ manifest.json"
    [ "$SKIP_LANGUAGES" = false ] && echo "  ✓ Language files synchronized"
    [ "$GENERATE_REPORT" = true ] && echo "  ✓ Translation report generated"
fi

print_status "Update process finished"