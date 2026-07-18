#!/bin/bash

echo "Building WordBank architecture..."
# Using $HOME ensures this goes to /home/pi/ (or your user), NOT the root directory
mkdir -p "$HOME/WordBank"
touch "$HOME/.floppy_ledger"

echo "Installing word@ command to system..."
# The script asks for sudo ONLY for the two lines that require system access
sudo chmod +x word@
sudo cp word@ /usr/local/bin/word@

echo "Installation complete! Type 'word@ ?well' to begin."
