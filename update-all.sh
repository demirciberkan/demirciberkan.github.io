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
BASE_URL="https://demirciberkan.github.io"

# Parse command line arguments
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --base-url)
            BASE_URL="$2"
            shift 2
            ;;
        --help|-h)
            echo "EVSEPARKER Manifest Updater"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --dry-run              Show what would be updated without making changes"
            echo "  --base-url URL         Base URL for firmware downloads (default: https://demirciberkan.github.io)"
            echo "  --help, -h             Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                     # Update manifest.json"
            echo "  $0 --dry-run           # Show what would be updated"
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
print_header "EVSEPARKER Manifest Update"

if [ "$DRY_RUN" = true ]; then
    print_warning "DRY RUN MODE - No files will be modified"
    echo
fi

# Update manifest.json
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

# Final summary
print_header "Update Summary"

if [ "$DRY_RUN" = true ]; then
    print_status "Dry run completed - no files were modified"
    print_status "Run without --dry-run to apply changes"
else
    print_success "Manifest update completed successfully!"
    echo "Files updated:"
    echo "  ✓ manifest.json"
fi

print_status "Update process finished"