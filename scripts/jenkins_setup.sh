#!/bin/bash

# Jenkins Setup Script for Selenium YouTube Tests
# This script helps set up Jenkins with the required plugins and configurations

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

# Jenkins configuration
JENKINS_URL=${JENKINS_URL:-"http://localhost:8080"}
JENKINS_USER=${JENKINS_USER:-"admin"}
JENKINS_PASSWORD=${JENKINS_PASSWORD:-""}
JOB_NAME="selenium-youtube-tests"

# Function to check if Jenkins is running
check_jenkins() {
    print_message $BLUE "Checking Jenkins availability..."
    
    if curl -f -s "${JENKINS_URL}/login" > /dev/null; then
        print_message $GREEN "Jenkins is running at ${JENKINS_URL}"
        return 0
    else
        print_message $RED "Jenkins is not accessible at ${JENKINS_URL}"
        return 1
    fi
}

# Function to install required Jenkins plugins
install_plugins() {
    print_message $BLUE "Installing required Jenkins plugins..."
    
    local plugins=(
        "workflow-aggregator"
        "pipeline-stage-view"
        "build-pipeline-plugin"
        "docker-workflow"
        "html-publisher"
        "email-ext"
        "build-timeout"
        "timestamper"
        "ws-cleanup"
        "ant"
        "gradle"
        "git"
        "github"
        "junit"
        "xvfb"
        "parameterized-trigger"
        "conditional-buildstep"
        "run-condition"
        "matrix-auth"
        "role-strategy"
        "build-user-vars-plugin"
        "allure-jenkins-plugin"
    )
    
    for plugin in "${plugins[@]}"; do
        print_message $YELLOW "Installing plugin: $plugin"
        # Note: This requires Jenkins CLI or REST API authentication
        # curl -X POST "${JENKINS_URL}/pluginManager/installNecessaryPlugins" \
        #      -d "<jenkins><install plugin=\"${plugin}@latest\" /></jenkins>" \
        #      --user "${JENKINS_USER}:${JENKINS_PASSWORD}"
    done
    
    print_message $GREEN "Plugin installation commands prepared (manual installation required)"
}

# Function to create Jenkins job
create_jenkins_job() {
    print_message $BLUE "Creating Jenkins job: ${JOB_NAME}"
    
    local job_config="jenkins/job-config.xml"
    
    if [[ ! -f "$job_config" ]]; then
        print_message $RED "Job configuration file not found: $job_config"
        return 1
    fi
    
    print_message $YELLOW "Job configuration file: $job_config"
    print_message $YELLOW "Manual job creation required in Jenkins UI"
    
    cat << EOF

Jenkins Job Creation Instructions:
=================================

1. Open Jenkins at: ${JENKINS_URL}
2. Click "New Item"
3. Enter job name: ${JOB_NAME}
4. Select "Pipeline" project type
5. Configure the following settings:

   General:
   - Description: Selenium YouTube Test Automation Pipeline
   - Discard old builds: Keep 50 builds, 30 days
   
   Build Triggers:
   - Build periodically: H 2 * * 1-5 (weekdays at 2 AM)
   - GitHub hook trigger (if using GitHub)
   
   Pipeline:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: [Your Git Repository URL]
   - Branch: */main
   - Script Path: Jenkinsfile
   
   Parameters (will be auto-configured from Jenkinsfile):
   - TEST_SUITE (Choice): all, smoke, regression, youtube_search, youtube_video, youtube_navigation
   - BROWSER_TYPE (Choice): chrome, firefox, edge
   - PARALLEL_EXECUTION (Boolean): false
   - PARALLEL_COUNT (String): 2

6. Save the job configuration

EOF
}

# Function to setup Jenkins environment
setup_jenkins_environment() {
    print_message $BLUE "Setting up Jenkins environment..."
    
    cat << EOF

Jenkins Environment Setup:
=========================

1. System Configuration:
   - Manage Jenkins > Configure System
   - Set up Global Tool Configuration for:
     * Git
     * Docker
     * Python (if using Python installations)
   
2. Security Configuration:
   - Enable security if not already enabled
   - Configure authentication (LDAP, GitHub, etc.)
   - Set up authorization strategy
   
3. Node Configuration:
   - Ensure Jenkins has Docker access
   - Install required tools on Jenkins nodes:
     * Docker
     * Docker Compose
     * Git
   
4. Credential Management:
   - Add GitHub credentials (if using private repositories)
   - Add Docker registry credentials (if using private registries)
   - Add email server credentials for notifications
   
5. Plugin Configuration:
   - Configure Email Extension Plugin
   - Configure HTML Publisher Plugin
   - Configure Allure Plugin (if using Allure reports)

EOF
}

# Function to setup Docker for Jenkins
setup_docker_integration() {
    print_message $BLUE "Setting up Docker integration..."
    
    cat << EOF

Docker Integration Setup:
========================

1. Ensure Jenkins user has Docker permissions:
   sudo usermod -aG docker jenkins
   sudo systemctl restart jenkins

2. Install Docker Pipeline Plugin in Jenkins

3. Configure Docker in Jenkins:
   - Manage Jenkins > Configure System
   - Add Docker installation
   - Test Docker connectivity

4. For Docker-in-Docker scenarios:
   - Mount Docker socket: -v /var/run/docker.sock:/var/run/docker.sock
   - Or use Docker-in-Docker (DinD) container

5. Selenium Grid Setup (Optional):
   - Use docker-compose.yml provided in the project
   - Configure network access between Jenkins and Selenium Grid

EOF
}

# Function to setup email notifications
setup_email_notifications() {
    print_message $BLUE "Setting up email notifications..."
    
    cat << EOF

Email Notification Setup:
========================

1. Configure SMTP Server:
   - Manage Jenkins > Configure System
   - E-mail Notification section
   - Set SMTP server, port, authentication
   - Test configuration

2. Extended E-mail Notification:
   - Configure Extended E-mail Notification plugin
   - Set default recipients, subject, content
   - Configure triggers (failure, success, unstable)

3. Environment Variables (optional):
   - DEFAULT_EMAIL: Default email for notifications
   - SMTP_SERVER: SMTP server address
   - SMTP_PORT: SMTP server port

EOF
}

# Function to create sample Jenkins configuration files
create_config_files() {
    print_message $BLUE "Creating Jenkins configuration templates..."
    
    # Create Jenkins directory structure
    mkdir -p jenkins/templates
    
    # Create email template
    cat > jenkins/templates/email-template.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background-color: #f4f4f4; padding: 10px; }
        .content { padding: 20px; }
        .success { color: green; }
        .failure { color: red; }
        .unstable { color: orange; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Selenium Test Results - ${BUILD_STATUS}</h2>
    </div>
    <div class="content">
        <p><strong>Project:</strong> ${PROJECT_NAME}</p>
        <p><strong>Build Number:</strong> ${BUILD_NUMBER}</p>
        <p><strong>Build Status:</strong> <span class="${BUILD_STATUS_CSS}">${BUILD_STATUS}</span></p>
        <p><strong>Test Suite:</strong> ${TEST_SUITE}</p>
        <p><strong>Browser:</strong> ${BROWSER_TYPE}</p>
        <p><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
        <p><strong>Test Reports:</strong> <a href="${BUILD_URL}Selenium_Test_Report/">View Reports</a></p>
        
        <h3>Build Information</h3>
        <p><strong>Started by:</strong> ${BUILD_USER}</p>
        <p><strong>Duration:</strong> ${BUILD_DURATION}</p>
        <p><strong>Node:</strong> ${NODE_NAME}</p>
        
        ${TEST_RESULTS_SUMMARY}
    </div>
</body>
</html>
EOF

    # Create Jenkins job template
    cat > jenkins/templates/job-template.groovy << 'EOF'
pipelineJob('selenium-youtube-tests') {
    description('Selenium YouTube Test Automation Pipeline')
    
    parameters {
        choiceParam('TEST_SUITE', ['all', 'smoke', 'regression', 'youtube_search', 'youtube_video', 'youtube_navigation'], 'Select test suite to run')
        choiceParam('BROWSER_TYPE', ['chrome', 'firefox', 'edge'], 'Select browser for testing')
        booleanParam('PARALLEL_EXECUTION', false, 'Run tests in parallel')
        stringParam('PARALLEL_COUNT', '2', 'Number of parallel processes')
    }
    
    triggers {
        cron('H 2 * * 1-5')
    }
    
    logRotator {
        numToKeep(50)
        daysToKeep(30)
        artifactNumToKeep(10)
        artifactDaysToKeep(7)
    }
    
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/your-repo/selenium-youtube-tests.git')
                        credentials('github-credentials')
                    }
                    branch('main')
                }
            }
            scriptPath('Jenkinsfile')
        }
    }
}
EOF

    print_message $GREEN "Jenkins configuration templates created in jenkins/templates/"
}

# Function to show Jenkins CLI commands
show_jenkins_cli_commands() {
    print_message $BLUE "Jenkins CLI Commands Reference..."
    
    cat << EOF

Jenkins CLI Commands:
====================

1. Download Jenkins CLI:
   wget ${JENKINS_URL}/jnlpJars/jenkins-cli.jar

2. Install Plugins:
   java -jar jenkins-cli.jar -s ${JENKINS_URL} install-plugin workflow-aggregator pipeline-stage-view

3. Create Job:
   java -jar jenkins-cli.jar -s ${JENKINS_URL} create-job ${JOB_NAME} < jenkins/job-config.xml

4. Build Job:
   java -jar jenkins-cli.jar -s ${JENKINS_URL} build ${JOB_NAME}

5. Get Job Status:
   java -jar jenkins-cli.jar -s ${JENKINS_URL} get-job ${JOB_NAME}

6. List Jobs:
   java -jar jenkins-cli.jar -s ${JENKINS_URL} list-jobs

Note: Authentication may be required. Use -auth username:password or API token.

EOF
}

# Main function
main() {
    print_message $GREEN "=== Jenkins Setup for Selenium YouTube Tests ==="
    echo
    
    print_message $BLUE "This script will help you set up Jenkins for the Selenium test project."
    print_message $YELLOW "Some steps require manual configuration in Jenkins UI."
    echo
    
    # Check if Jenkins is accessible
    if check_jenkins; then
        echo
        install_plugins
        echo
        create_jenkins_job
        echo
        setup_jenkins_environment
        echo
        setup_docker_integration
        echo
        setup_email_notifications
        echo
        create_config_files
        echo
        show_jenkins_cli_commands
        echo
        print_message $GREEN "=== Jenkins setup instructions completed! ==="
        print_message $BLUE "Follow the manual configuration steps shown above."
    else
        print_message $RED "Please ensure Jenkins is running and accessible."
        print_message $YELLOW "Start Jenkins and re-run this script."
    fi
}

# Show help if requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    cat << EOF
Jenkins Setup Script for Selenium YouTube Tests

Usage: $0 [OPTIONS]

ENVIRONMENT VARIABLES:
    JENKINS_URL      Jenkins server URL (default: http://localhost:8080)
    JENKINS_USER     Jenkins username (default: admin)
    JENKINS_PASSWORD Jenkins password or API token

OPTIONS:
    -h, --help      Show this help message

This script provides setup instructions and templates for configuring
Jenkins to run the Selenium YouTube test automation pipeline.

EOF
    exit 0
fi

# Run main function
main