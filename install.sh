#!/bin/bash

echo "🌌 Installing AuraFetch..."

INSTALL_DIR="$HOME/.aurafetch"
BIN_PATH="$INSTALL_DIR/aurafetch.py"
REPO_URL="https://github.com/YOUR_USERNAME/aurafetch.git"

# Clone or update repo
if [ -d "$INSTALL_DIR" ]; then
    echo "🔄 Updating existing install..."
    cd "$INSTALL_DIR" && git pull
else
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install --quiet --upgrade pip
python3 -m pip install --quiet psutil distro requests netifaces

# Create alias in shell config
ALIAS_CMD="alias aurafetch='python3 $BIN_PATH'"
SHELL_RC="$HOME/.bashrc"
[[ $SHELL == *zsh ]] && SHELL_RC="$HOME/.zshrc"

if ! grep -Fxq "$ALIAS_CMD" "$SHELL_RC"; then
    echo "$ALIAS_CMD" >> "$SHELL_RC"
    echo "✅ Alias 'aurafetch' added to $SHELL_RC"
fi

echo "✅ Done! Type 'aurafetch' in your terminal."
exec bash
