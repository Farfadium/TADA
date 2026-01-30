#!/bin/bash
set -e

echo "🚀 Setup TADA Web"

# Chemins
BACKEND_DIR="/root/TADA/_SYSTEM/runtime/web/backend"
FRONTEND_DIR="/root/TADA/_SYSTEM/runtime/web/frontend"
DEPLOY_DIR="/root/TADA/_SYSTEM/runtime/web/deploy"

# Backend
echo "📦 Installation backend..."
cd "$BACKEND_DIR"

# Créer venv si nécessaire
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Installer dépendances
source venv/bin/activate
pip install -r requirements.txt

# Frontend
echo "📦 Installation frontend..."
cd "$FRONTEND_DIR"

# Installer node si nécessaire
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js non installé. Installation..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi

# Installer dépendances
npm install

# Build production
npm run build

# Systemd service
echo "⚙️  Configuration systemd..."
cp "$DEPLOY_DIR/tada-web.service" /etc/systemd/system/
systemctl daemon-reload

# Générer mot de passe
echo ""
echo "🔐 Génération du hash de mot de passe..."
echo "Entrez le mot de passe pour l'utilisateur 'yvan':"
read -s PASSWORD

cd "$BACKEND_DIR"
HASH=$(python3 -c "from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto'); print(pwd_context.hash('$PASSWORD'))")

echo ""
echo "Hash généré. Ajoutez cette ligne dans /etc/systemd/system/tada-web.service:"
echo "Environment=\"TADA_ADMIN_PASSWORD_HASH=$HASH\""
echo ""
echo "Puis:"
echo "  systemctl daemon-reload"
echo "  systemctl enable tada-web"
echo "  systemctl start tada-web"
echo ""
echo "✅ Setup terminé!"
