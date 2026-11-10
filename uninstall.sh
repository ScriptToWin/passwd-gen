#!/usr/bin/env bash
set -e

COMMAND_NAME="passgen"
INSTALL_DIR="/usr/local/bin"
TARGET="$INSTALL_DIR/$COMMAND_NAME"

# Prüfen, ob der Befehl installiert ist
if [ ! -f "$TARGET" ]; then
    echo "Info: '$COMMAND_NAME' ist nicht in $INSTALL_DIR installiert."
    exit 0
fi

echo "Entferne '$COMMAND_NAME' aus $INSTALL_DIR..."

# Datei entfernen (benötigt sudo)
sudo rm "$TARGET"

echo "Fertig! '$COMMAND_NAME' wurde erfolgreich deinstalliert."
