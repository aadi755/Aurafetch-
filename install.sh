#!/bin/bash

echo "🔧 Installing AuraFetch (User-level install)..."

INSTALL_BIN="$HOME/.local/bin"
INSTALL_DATA="$HOME/.local/share/aurafetch"
SCRIPT_URL="https://raw.githubusercontent.com/aadi755/Aurafetch-/main/aurafetch.py"
SCRIPT_PATH="$INSTALL_DATA/aurafetch.py"
LAUNCHER_PATH="$INSTALL_BIN/aurafetch"

mkdir -p "$INSTALL_BIN" "$INSTALL_DATA"

echo "📥 Downloading aurafetch.py to $SCRIPT_PATH ..."
if ! curl -fsSL "$SCRIPT_URL" -o "$SCRIPT_PATH"; then
  echo "❌ Failed to download aurafetch.py"
  exit 1
fi
chmod +x "$SCRIPT_PATH"

echo "⚙️ Creating launcher at $LAUNCHER_PATH ..."
cat > "$LAUNCHER_PATH" << EOF
#!/bin/bash
python3 "$SCRIPT_PATH" "\$@"
EOF
chmod +x "$LAUNCHER_PATH"

# Add ~/.local/bin to PATH in shell configs if missing
if ! echo "$PATH" | grep -q "$INSTALL_BIN"; then
  echo "Adding $INSTALL_BIN to PATH in shell configs..."
  echo "export PATH=\"\$PATH:$INSTALL_BIN\"" >> "$HOME/.bashrc"
  echo "export PATH=\"\$PATH:$INSTALL_BIN\"" >> "$HOME/.zshrc"
  echo "✅ Added $INSTALL_BIN to PATH. You don't have to source it now to run aurafetch once."
fi

PYTHON_BIN=$(command -v python3)
if [[ -z "$PYTHON_BIN" ]]; then
  echo "❌ python3 not found. Please install python3."
  exit 1
fi

if ! "$PYTHON_BIN" -m pip --version &> /dev/null; then
  echo "❌ pip not found. Please install pip."
  exit 1
fi

echo "📦 Installing Python dependencies (user install)..."
"$PYTHON_BIN" -m pip install --quiet --user psutil netifaces requests distro

# Temporarily update PATH for this session so user can run aurafetch immediately
export PATH="$PATH:$INSTALL_BIN"

echo -e "\n🚀 \033[1mAuraFetch installed successfully!\033[0m"
echo "👉 You can run it now with: \033[1maurafetch\033[0m"
