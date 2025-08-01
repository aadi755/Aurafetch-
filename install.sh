#!/bin/bash

echo "🔧 Installing AuraFetch..."

# Set variables
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_URL="https://raw.githubusercontent.com/aadi755/Aurafetch-/main/aurafetch.py"
PY_SCRIPT_PATH="$INSTALL_DIR/aurafetch.py"
LAUNCHER_PATH="$INSTALL_DIR/aurafetch"

# Ensure bin directory exists
mkdir -p "$INSTALL_DIR"

# Download the Python script
echo "📥 Downloading AuraFetch script..."
if ! curl -fsSL "$SCRIPT_URL" -o "$PY_SCRIPT_PATH"; then
  echo "❌ Failed to download AuraFetch script from $SCRIPT_URL"
  exit 1
fi
chmod +x "$PY_SCRIPT_PATH"

# Create launcher wrapper script
echo "⚙️ Creating 'aurafetch' launcher command..."
cat << EOF > "$LAUNCHER_PATH"
#!/bin/bash
PYTHON_BIN=\$(command -v python3 || command -v python)
if [[ -z "\$PYTHON_BIN" ]]; then
  echo "❌ Python is not installed."
  exit 1
fi
exec "\$PYTHON_BIN" "$PY_SCRIPT_PATH" "\$@"
EOF
chmod +x "$LAUNCHER_PATH"

# Add ~/.local/bin to PATH in shell profiles if missing
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
  echo 'export PATH="$PATH:$HOME/.local/bin"' >> "$HOME/.bashrc"
  echo 'export PATH="$PATH:$HOME/.local/bin"' >> "$HOME/.zshrc"
  echo "✅ Added $INSTALL_DIR to PATH. Restart your terminal or run:"
  echo "    source ~/.bashrc  OR  source ~/.zshrc"
else
  echo "✅ AuraFetch launcher installed at: $LAUNCHER_PATH"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
PYTHON_BIN=$(command -v python3 || command -v python)

if [[ -z "$PYTHON_BIN" ]]; then
  echo "❌ Python is not installed!"
  exit 1
fi

if ! "$PYTHON_BIN" -m pip --version &> /dev/null; then
  echo "❌ pip is not available. Please install pip with:"
  echo "    sudo apt install python3-pip  # or equivalent"
  exit 1
fi

"$PYTHON_BIN" -m pip install --quiet --user psutil netifaces requests distro

echo "🚀 Done! AuraFetch is ready."
echo "💻 Run it from anywhere using: aurafetch"
