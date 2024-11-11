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

    # Verify installation
    sudo docker run hello-world
}

# Function to set up Docker group and user permissions
setup_docker_group() {
    echo "Setting up Docker group and adding user..."

    # Create the docker group if it doesn't exist
    sudo groupadd docker

    # Add the current user to the docker group
    sudo usermod -aG docker $USER

    # Inform the user to log out or restart for the changes to take effect
    echo "You need to log out and log back in for the group membership to be re-evaluated."
    echo "Alternatively, you can run 'newgrp docker' to apply the changes immediately."
}

# Main logic
if command -v docker &> /dev/null; then
    # Docker is installed
    echo "Docker is already installed."

    # Check if Docker needs sudo to run
    if sudo docker run hello-world &> /dev/null; then
        echo "Docker requires sudo to run. Setting up Docker to run without sudo..."

        # Set up Docker group
        setup_docker_group

        # Verify that Docker works without sudo
        echo "Verifying Docker installation..."
        docker run hello-world

    else
        # Docker doesn't need sudo, so just run the docker compose command
        echo "Docker setup is complete, running docker-compose..."
        docker compose up -d
    fi
else
    # Docker is not installed, so proceed with installation
    echo "Docker is not installed. Installing Docker..."

    # Remove conflicting packages
    uninstall_conflicting_packages

    # Install Docker
    install_docker

    # Set up Docker group
    setup_docker_group

    # Verify installation and run docker-compose
    docker run hello-world
    echo "Docker setup is complete, running docker-compose..."
    docker compose up -d
fi
