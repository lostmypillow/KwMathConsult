#!/bin/bash

# Exit on error
set -e
APP_DIR="$(pwd)"
SERVICE_NAME="fastapi"

echo "SETUP [Update system]"
sudo apt full-upgrade -qq >/dev/null
echo "ok"

echo "SETUP [Ensure necessary packages are installed]"
sudo apt-get install -y python3-venv python3-pip python3-tk wget p7zip-full >/dev/null
echo "ok"


echo "SETUP [Ensure virtual environment is enabled]"
if [ ! -d "$APP_DIR/.venv" ]; then
    python3 -m venv "$APP_DIR/.venv" >/dev/null
fi
source "$APP_DIR/.venv/bin/activate"
echo "ok"

echo "SETUP [Install Python requirements]"
pip install -r "$APP_DIR/requirements.txt" >/dev/null
echo "ok"

echo "SETUP [Install Microsoft ODBC Driver 18]"
curl https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg >/dev/null
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list >/dev/null
sudo apt-get update -y
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18 >/dev/null
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18 >/dev/null
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
sudo apt-get install -y unixodbc-dev >/dev/null
echo "ok"

echo "SETUP [Register as systemd service and start it]"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=KwConsult API
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$VENV_DIR/bin/gunicorn --bind 0.0.0.0:8001 -k uvicorn.workers.UvicornWorker src.main:app"
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable, and start the service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Print status of the service
sudo systemctl status $SERVICE_NAME
