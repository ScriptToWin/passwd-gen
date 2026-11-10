#!/usr/bin/env bash
set -e

SCRIPT_NAME="passgen.py"
COMMAND_NAME="passgen"
INSTALL_DIR="/usr/local/bin"

# Prüfen, ob passgen.py im aktuellen Verzeichnis liegt
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "Fehler: '$SCRIPT_NAME' wurde im aktuellen Verzeichnis nicht gefunden."
    exit 1
fi

echo "Installiere '$COMMAND_NAME' nach $INSTALL_DIR..."

# Datei ausführbar machen
chmod +x "$SCRIPT_NAME"

# Nach /usr/local/bin kopieren (ohne .py Endung)
sudo cp "$SCRIPT_NAME" "$INSTALL_DIR/$COMMAND_NAME"

echo "Fertig! Du kannst das Programm jetzt überall mit dem Befehl '$COMMAND_NAME' starten."
echo "Beispiel: $COMMAND_NAME --blocks 4"
