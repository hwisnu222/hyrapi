#!/bin/bash

set -e

REPO="hwisnu222/hyrapi"
BINARY_NAME="hyr"
INSTALL_PATH="/usr/local/bin"

echo "Fetching latest release for $REPO..."

DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" |
  grep "browser_download_url" |
  grep "$BINARY_NAME"\" |
  cut -d '"' -f 4)

if [ -z "$DOWNLOAD_URL" ]; then
  echo "Failed to find download URL."
  exit 1
fi

echo "Downloading $BINARY_NAME from $DOWNLOAD_URL ..."
curl -L "$DOWNLOAD_URL" -o "$BINARY_NAME"

chmod +x "$BINARY_NAME"

echo "Moving $BINARY_NAME to $INSTALL_PATH ..."
sudo mv "$BINARY_NAME" "$INSTALL_PATH/"

echo "Installed $BINARY_NAME to $INSTALL_PATH/$BINARY_NAME"
