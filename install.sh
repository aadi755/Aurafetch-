#!/bin/bash

echo "🔧 Installing AuraFetch (User-level install)..."

INSTALL_DIR="$HOME/.local/bin"
PY_SCRIPT_URL="https://raw.githubusercontent.com/aadi755/Aurafetch-/main/aurafetch.py"
PY_SCRIPT_PATH="$INSTALL_DIR/aurafetch.py"
LAUNCHER_PATH="$INSTALL_DIR/aurafetch"

# Create install directory
mkdir -p "$INSTALL_DIR"

# Download aurafetch.py
echo "📥 Downloading aurafetch.py..."
if ! curl -fsSL "$PY_SCRIPT_URL" -o "$PY_SCRIPT_PATH"; then
  echo "❌ Failed to download aurafetch.py"
  exit 1
fi
chmod +x "$PY_SCRIPT_PATH"

# Create launcher script
echo "⚙️ Creating launcher at: $LAUNCHER_PATH"
cat << EOF > "$LAUNCHER_PATH"
#!/bin/bash
python3 "$PY_SCRIPT_PATH" "\$@"
EOF
chmod +x "$LAUNCHER_PATH"

# Install Python dependencies
echo "📦 Installing Python dependencies (user-only)..."
PYTHON_BIN=$(command -v python3)
if [[ -z "$PYTHON_BIN" ]]; then
  echo "❌ python3 not found. Please install Python 3."
  exit 1
fi

if ! "$PYTHON_BIN" -m pip --version &>/dev/null; then
  echo "❌ pip not found. Please install pip for Python 3."
  exit 1
fi

"$PYTHON_BIN" -m pip install --quiet --user psutil netifaces requests distro

# Check if ~/.local/bin is already in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
  echo 'export PATH="$PATH:$HOME/.local/bin"' >> "$HOME/.bashrc"
  echo 'export PATH="$PATH:$HOME/.local/bin"' >> "$HOME/.zshrc"
  echo "✅ Added $INSTALL_DIR to PATH in your shell config files."
  echo "👉 Please restart your terminal or run:"
  echo "   source ~/.bashrc    # for bash users"
  echo "   source ~/.zshrc     # for zsh users"
else
  echo "✅ $INSTALL_DIR is already in your PATH."
fi

echo -e "\n🚀 \033[1mAuraFetch installed successfully!\033[0m"
echo -e "👉 Run it now with: \033[1maurafetch\033[0m"
