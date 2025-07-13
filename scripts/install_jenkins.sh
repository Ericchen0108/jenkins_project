#!/bin/bash

# Jenkins Installation Script for macOS
# This script installs Jenkins using Homebrew and sets it up for Selenium testing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Jenkins is running
check_jenkins_running() {
    if curl -f -s http://localhost:8080/login >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to install Homebrew if not present
install_homebrew() {
    if ! command_exists brew; then
        print_message $YELLOW "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for the current session
        if [[ "$OSTYPE" == "darwin"* ]]; then
            if [[ -f "/opt/homebrew/bin/brew" ]]; then
                eval "$(/opt/homebrew/bin/brew shellenv)"
            elif [[ -f "/usr/local/bin/brew" ]]; then
                eval "$(/usr/local/bin/brew shellenv)"
            fi
        fi
        
        print_message $GREEN "✅ Homebrew installed successfully"
    else
        print_message $GREEN "✅ Homebrew is already installed"
    fi
}

# Function to install Jenkins
install_jenkins() {
    print_message $BLUE "Installing Jenkins..."
    
    if brew list jenkins >/dev/null 2>&1; then
        print_message $GREEN "✅ Jenkins is already installed"
    else
        brew install jenkins
        print_message $GREEN "✅ Jenkins installed successfully"
    fi
}

# Function to start Jenkins
start_jenkins() {
    print_message $BLUE "Starting Jenkins service..."
    
    if check_jenkins_running; then
        print_message $GREEN "✅ Jenkins is already running"
    else
        brew services start jenkins
        
        # Wait for Jenkins to start
        print_message $YELLOW "Waiting for Jenkins to start..."
        local timeout=60
        local count=0
        
        while [ $count -lt $timeout ]; do
            if check_jenkins_running; then
                print_message $GREEN "✅ Jenkins started successfully"
                return 0
            fi
            sleep 2
            count=$((count + 2))
            echo -n "."
        done
        
        print_message $RED "❌ Jenkins failed to start within $timeout seconds"
        return 1
    fi
}

# Function to get initial admin password
get_admin_password() {
    print_message $BLUE "Retrieving Jenkins initial admin password..."
    
    local password_file
    
    # Try different possible locations
    if [[ -f "/opt/homebrew/var/jenkins_home/secrets/initialAdminPassword" ]]; then
        password_file="/opt/homebrew/var/jenkins_home/secrets/initialAdminPassword"
    elif [[ -f "/usr/local/var/jenkins_home/secrets/initialAdminPassword" ]]; then
        password_file="/usr/local/var/jenkins_home/secrets/initialAdminPassword"
    elif [[ -f "$HOME/.jenkins/secrets/initialAdminPassword" ]]; then
        password_file="$HOME/.jenkins/secrets/initialAdminPassword"
    else
        print_message $YELLOW "⚠️ Could not locate initial admin password file"
        print_message $YELLOW "Please check Jenkins logs for the password"
        return 1
    fi
    
    if [[ -f "$password_file" ]]; then
        local password=$(cat "$password_file")
        print_message $GREEN "✅ Initial admin password found:"
        print_message $YELLOW "================================"
        print_message $YELLOW "$password"
        print_message $YELLOW "================================"
        print_message $BLUE "Save this password - you'll need it for initial setup!"
    else
        print_message $RED "❌ Initial admin password file not found"
        return 1
    fi
}

# Function to install Docker (required for containerized tests)
install_docker() {
    print_message $BLUE "Checking Docker installation..."
    
    if command_exists docker; then
        print_message $GREEN "✅ Docker is already installed"
        
        # Check if Docker is running
        if docker info >/dev/null 2>&1; then
            print_message $GREEN "✅ Docker is running"
        else
            print_message $YELLOW "⚠️ Docker is installed but not running"
            print_message $BLUE "Please start Docker Desktop manually"
        fi
    else
        print_message $YELLOW "⚠️ Docker not found"
        print_message $BLUE "Installing Docker via Homebrew..."
        brew install --cask docker
        print_message $GREEN "✅ Docker installed"
        print_message $YELLOW "Please start Docker Desktop manually after installation"
    fi
}

# Function to verify installation
verify_installation() {
    print_message $BLUE "Verifying installation..."
    
    # Check Jenkins
    if check_jenkins_running; then
        print_message $GREEN "✅ Jenkins is running on http://localhost:8080"
    else
        print_message $RED "❌ Jenkins is not running"
        return 1
    fi
    
    # Check Java (required for Jenkins)
    if command_exists java; then
        java_version=$(java -version 2>&1 | head -n 1)
        print_message $GREEN "✅ Java found: $java_version"
    else
        print_message $YELLOW "⚠️ Java not found - Jenkins may have issues"
    fi
    
    # Check Git
    if command_exists git; then
        git_version=$(git --version)
        print_message $GREEN "✅ Git found: $git_version"
    else
        print_message $YELLOW "⚠️ Git not found - install with: brew install git"
    fi
    
    return 0
}

# Function to show next steps
show_next_steps() {
    print_message $GREEN "🎉 Jenkins installation completed!"
    print_message $BLUE "
Next Steps:
1. Open your browser and go to: http://localhost:8080
2. Use the initial admin password shown above
3. Install suggested plugins
4. Create your admin user
5. Run the Jenkins setup script: ./scripts/jenkins_setup.sh

Setup Guide: Open JENKINS_SETUP.md for detailed instructions

Jenkins Management:
- Start Jenkins: brew services start jenkins
- Stop Jenkins: brew services stop jenkins
- Restart Jenkins: brew services restart jenkins
- View logs: brew services --help jenkins
"
}

# Main installation function
main() {
    print_message $GREEN "🚀 Jenkins Installation Script for Selenium Testing"
    print_message $BLUE "=================================================="
    
    # Check OS
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_message $RED "❌ This script is designed for macOS only"
        print_message $BLUE "For other OS, please refer to JENKINS_SETUP.md"
        exit 1
    fi
    
    # Install Homebrew
    install_homebrew
    
    # Install Jenkins
    install_jenkins
    
    # Install Docker
    install_docker
    
    # Start Jenkins
    if start_jenkins; then
        # Get admin password
        get_admin_password
        
        # Verify installation
        if verify_installation; then
            show_next_steps
        else
            print_message $RED "❌ Installation verification failed"
            exit 1
        fi
    else
        print_message $RED "❌ Failed to start Jenkins"
        exit 1
    fi
}

# Show help if requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    cat << EOF
Jenkins Installation Script for Selenium Testing

Usage: $0 [OPTIONS]

This script will:
1. Install Homebrew (if not present)
2. Install Jenkins via Homebrew
3. Install Docker (for containerized testing)
4. Start Jenkins service
5. Display initial admin password
6. Verify installation

OPTIONS:
    -h, --help      Show this help message

After running this script:
1. Open http://localhost:8080 in your browser
2. Use the displayed admin password
3. Follow the setup wizard
4. Run ./scripts/jenkins_setup.sh for job configuration

For detailed setup instructions, see JENKINS_SETUP.md

EOF
    exit 0
fi

# Run main function
main