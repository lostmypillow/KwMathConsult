#!/bin/bash

# Exit on error
set -e
APP_DIR="$(pwd)/backend"
SERVICE_NAME="kwmathconsult"
PORT="8001"
echo "SYNC [Syncing version...]"
VERSION=$(python3 sync_version.py)
echo "Done."
echo ""
echo "KwMathConsult API DEPLOY SCRIPT FOR v$VERSION STARTING..."
echo ""

ENV_FILE="$APP_DIR/.env"
ENV_EXAMPLE="$APP_DIR/.env.example"

if [ ! -f "$ENV_FILE" ]; then
    echo "SETUP [Create .env file...]"
    cp "$ENV_EXAMPLE" "$ENV_FILE"

    # Create a temporary file to store user inputs
    TEMP_ENV=$(mktemp)
    
    while IFS= read -r line || [ -n "$line" ]; do
        # Ignore empty lines or comments
        if [[ -z "$line" || "$line" == \#* ]]; then
            echo "$line" >> "$TEMP_ENV"
            continue
        fi

        VAR_NAME=$(echo "$line" | cut -d= -f1)
        read -rp "Enter value for $VAR_NAME: " VAR_VAL
        echo "$VAR_NAME=$VAR_VAL" >> "$TEMP_ENV"
    done < "$ENV_EXAMPLE"

    mv "$TEMP_ENV" "$ENV_FILE"
    echo "Done! .env created at $ENV_FILE"
fi
echo ""



echo "SETUP [Updating system...]"
sudo apt-get update -y >/dev/null
echo "ok"

echo "SETUP [Ensuring necessary packages are installed...]"
sudo apt-get install -y python3-venv python3-pip wget curl gnupg nginx >/dev/null
curl -sSL -O https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb >/dev/null
rm packages-microsoft-prod.deb >/dev/null
sudo apt-get update -y >/dev/null
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18 >/dev/null
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18 >/dev/null
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
sudo apt-get install -y unixodbc-dev >/dev/null
echo "Done."
echo ""

echo "SETUP [Enabling virtual environment...]"
if [ ! -d "$APP_DIR/.venv" ]; then
    python3 -m venv "$APP_DIR/.venv" >/dev/null
fi
source "$APP_DIR/.venv/bin/activate"
echo "Done."
echo ""

echo "SETUP [Installing Python requirements...]"
pip install -r "$APP_DIR/requirements.txt" >/dev/null
# Gunicorn is installed only in deployment. This is becuz gunicorn doesn't work in Windows, where most of the dev work happens
pip install gunicorn >/dev/null
echo "Done."
echo ""

echo "SETUP [Registering as systemd service and starting the service...]"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=KwMathConsult
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/.venv/bin/gunicorn --bind 0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker src.main:app
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL
echo "ok"

echo "RUN [Starting FastAPI systemd service...]"
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME
if [[ "$(sudo systemctl status $SERVICE_NAME --no-pager --quiet)" == *"active (running)"* ]]; then
    echo "Done."
    echo ""
else
    echo "$SERVICE_NAME failed to start."
    echo ""
    exit 1
fi


echo "[DONE] Access KwMathConsult API at http://$(hostname -I | awk '{print $1}'):$PORT"

exit 0