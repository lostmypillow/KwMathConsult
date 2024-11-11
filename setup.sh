#!/bin/bash

# Function to uninstall conflicting packages
uninstall_conflicting_packages() {
    echo "Removing conflicting packages..."
    for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
        sudo apt-get remove -y $pkg
    done
}

# Function to install Docker
install_docker() {
    echo "Installing Docker..."

    # Install dependencies
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl

    # Add Docker's official GPG key
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add Docker repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update

    # Install Docker packages
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Set up Docker group and add the user
    sudo groupadd docker
    sudo usermod -aG docker $USER

    # Inform the user to log out or restart for the changes to take effect
    echo "Docker installed. You need to log out and log back in for the group membership to be re-evaluated."
    echo "Alternatively, you can run 'newgrp docker' to apply the changes immediately."

    # Verify installation by running the hello-world container
    sudo docker run hello-world
}

# Main logic
if command -v docker &> /dev/null; then
    # Docker is already installed, so just run docker-compose
    echo "Docker is already installed, running docker-compose..."
    docker compose up -d
else
    # Docker is not installed, proceed with installation
    echo "Docker is not installed. Installing Docker..."

    # Remove conflicting packages
    uninstall_conflicting_packages

    # Install Docker
    install_docker

    # Run docker-compose
    echo "Docker setup is complete, running docker-compose..."
    docker compose up -d
fi
