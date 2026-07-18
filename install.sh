#!/bin/bash

echo "Building WordBank architecture..."
mkdir -p ~/WordBank
touch ~/.floppy_ledger

echo "Installing word@ command to system..."
sudo chmod +x word@
sudo cp word@ /usr/local/bin/word@

echo "Installation complete! Type 'word@ ?well' to begin."