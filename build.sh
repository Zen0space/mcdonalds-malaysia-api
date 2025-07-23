#!/bin/bash

# Exit on error
set -e

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers with system dependencies
echo "Installing Playwright browsers..."
playwright install --with-deps chromium

echo "Build completed successfully!"
