#!/bin/bash

# Selenium YouTube Tests Runner Script
# This script provides various options to run the test suite

set -e

# Default values
TEST_SUITE="smoke"
BROWSER="chrome"
HEADLESS="true"
PARALLEL="false"
PARALLEL_COUNT="2"
ENVIRONMENT="local"
CLEAN_REPORTS="true"

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

# Function to show help
show_help() {
    cat << EOF
Selenium YouTube Tests Runner

Usage: $0 [OPTIONS]

OPTIONS:
    -s, --suite SUITE       Test suite to run (all, smoke, regression, youtube_search, youtube_video, youtube_navigation)
    -b, --browser BROWSER   Browser to use (chrome, firefox, edge)
    -h, --headless          Run in headless mode (default: true)
    -p, --parallel          Enable parallel execution
    -c, --count COUNT       Number of parallel processes (default: 2)
    -e, --env ENVIRONMENT   Test environment (local, dev, staging, prod, ci)
    --no-clean              Don't clean reports before running
    --docker                Run tests in Docker container
    --grid                  Run tests using Selenium Grid
    --help                  Show this help message

EXAMPLES:
    $0 --suite smoke --browser chrome --headless
    $0 --suite all --parallel --count 4
    $0 --suite regression --browser firefox --env staging
    $0 --docker --suite smoke
    $0 --grid --suite all --parallel --count 8

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--suite)
            TEST_SUITE="$2"
            shift 2
            ;;
        -b|--browser)
            BROWSER="$2"
            shift 2
            ;;
        -h|--headless)
            HEADLESS="true"
            shift
            ;;
        -p|--parallel)
            PARALLEL="true"
            shift
            ;;
        -c|--count)
            PARALLEL_COUNT="$2"
            shift 2
            ;;
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --no-clean)
            CLEAN_REPORTS="false"
            shift
            ;;
        --docker)
            USE_DOCKER="true"
            shift
            ;;
        --grid)
            USE_GRID="true"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_message $RED "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate test suite
valid_suites=("all" "smoke" "regression" "youtube_search" "youtube_video" "youtube_navigation")
if [[ ! " ${valid_suites[@]} " =~ " ${TEST_SUITE} " ]]; then
    print_message $RED "Invalid test suite: ${TEST_SUITE}"
    print_message $YELLOW "Valid suites: ${valid_suites[*]}"
    exit 1
fi

# Validate browser
valid_browsers=("chrome" "firefox" "edge")
if [[ ! " ${valid_browsers[@]} " =~ " ${BROWSER} " ]]; then
    print_message $RED "Invalid browser: ${BROWSER}"
    print_message $YELLOW "Valid browsers: ${valid_browsers[*]}"
    exit 1
fi

# Function to setup environment
setup_environment() {
    print_message $BLUE "Setting up test environment..."
    
    # Export environment variables
    export BROWSER=$BROWSER
    export HEADLESS=$HEADLESS
    export TEST_ENVIRONMENT=$ENVIRONMENT
    export SCREENSHOT_ON_FAILURE=true
    
    # Create reports directory
    if [[ "$CLEAN_REPORTS" == "true" ]]; then
        print_message $YELLOW "Cleaning previous reports..."
        rm -rf reports/*.html reports/screenshots/*.png 2>/dev/null || true
    fi
    
    mkdir -p reports/screenshots
    
    print_message $GREEN "Environment setup complete!"
}

# Function to install dependencies
install_dependencies() {
    if [[ ! -f "requirements.txt" ]]; then
        print_message $RED "requirements.txt not found!"
        exit 1
    fi
    
    print_message $BLUE "Installing Python dependencies..."
    pip install -r requirements.txt
    print_message $GREEN "Dependencies installed!"
}

# Function to run tests locally
run_local_tests() {
    print_message $BLUE "Running tests locally..."
    
    local pytest_args="--html=reports/report.html --self-contained-html --tb=short -v"
    
    # Add marker for test suite
    if [[ "$TEST_SUITE" != "all" ]]; then
        pytest_args="$pytest_args -m $TEST_SUITE"
    fi
    
    # Add parallel execution
    if [[ "$PARALLEL" == "true" ]]; then
        pytest_args="$pytest_args -n $PARALLEL_COUNT"
    fi
    
    # Run tests
    print_message $YELLOW "Executing: pytest $pytest_args"
    pytest $pytest_args
}

# Function to run tests in Docker
run_docker_tests() {
    print_message $BLUE "Running tests in Docker container..."
    
    # Build Docker image
    print_message $YELLOW "Building Docker image..."
    docker build -t selenium-youtube-tests .
    
    local docker_args="-v $(pwd)/reports:/app/reports"
    docker_args="$docker_args -e BROWSER=$BROWSER"
    docker_args="$docker_args -e HEADLESS=$HEADLESS"
    docker_args="$docker_args -e SCREENSHOT_ON_FAILURE=true"
    docker_args="$docker_args -e TEST_ENVIRONMENT=$ENVIRONMENT"
    
    local pytest_args="--html=reports/docker_report.html --self-contained-html --tb=short -v"
    
    if [[ "$TEST_SUITE" != "all" ]]; then
        pytest_args="$pytest_args -m $TEST_SUITE"
    fi
    
    if [[ "$PARALLEL" == "true" ]]; then
        pytest_args="$pytest_args -n $PARALLEL_COUNT"
    fi
    
    # Run Docker container
    print_message $YELLOW "Running Docker container..."
    docker run --rm $docker_args selenium-youtube-tests pytest $pytest_args
}

# Function to run tests using Selenium Grid
run_grid_tests() {
    print_message $BLUE "Running tests using Selenium Grid..."
    
    # Start Selenium Grid using docker-compose
    print_message $YELLOW "Starting Selenium Grid..."
    docker-compose up -d selenium-grid-hub selenium-chrome selenium-firefox
    
    # Wait for grid to be ready
    print_message $YELLOW "Waiting for Selenium Grid to be ready..."
    sleep 10
    
    # Check if grid is ready
    if ! curl -f http://localhost:4444/wd/hub/status > /dev/null 2>&1; then
        print_message $RED "Selenium Grid is not ready!"
        docker-compose down
        exit 1
    fi
    
    # Set grid environment
    export SELENIUM_GRID_URL="http://localhost:4444"
    
    local pytest_args="--html=reports/grid_report.html --self-contained-html --tb=short -v"
    
    if [[ "$TEST_SUITE" != "all" ]]; then
        pytest_args="$pytest_args -m $TEST_SUITE"
    fi
    
    if [[ "$PARALLEL" == "true" ]]; then
        pytest_args="$pytest_args -n $PARALLEL_COUNT"
    fi
    
    # Run tests
    print_message $YELLOW "Executing tests on Selenium Grid..."
    pytest $pytest_args
    
    # Cleanup
    print_message $YELLOW "Stopping Selenium Grid..."
    docker-compose down
}

# Function to generate summary report
generate_summary() {
    print_message $BLUE "Generating test summary..."
    
    local report_file="reports/test_summary.txt"
    
    cat > $report_file << EOF
Selenium YouTube Tests - Execution Summary
==========================================

Test Configuration:
- Suite: $TEST_SUITE
- Browser: $BROWSER
- Headless: $HEADLESS
- Parallel: $PARALLEL
- Parallel Count: $PARALLEL_COUNT
- Environment: $ENVIRONMENT
- Date: $(date)

Reports Generated:
EOF
    
    # List all HTML reports
    find reports -name "*.html" -type f | while read report; do
        echo "- $(basename $report)" >> $report_file
    done
    
    # List screenshots if any
    screenshot_count=$(find reports/screenshots -name "*.png" -type f 2>/dev/null | wc -l)
    echo "- Screenshots: $screenshot_count" >> $report_file
    
    print_message $GREEN "Summary generated: $report_file"
}

# Main execution
main() {
    print_message $GREEN "=== Selenium YouTube Tests Runner ==="
    print_message $BLUE "Configuration:"
    print_message $YELLOW "  Test Suite: $TEST_SUITE"
    print_message $YELLOW "  Browser: $BROWSER"
    print_message $YELLOW "  Headless: $HEADLESS"
    print_message $YELLOW "  Parallel: $PARALLEL"
    print_message $YELLOW "  Environment: $ENVIRONMENT"
    echo
    
    setup_environment
    
    if [[ "$USE_DOCKER" == "true" ]]; then
        run_docker_tests
    elif [[ "$USE_GRID" == "true" ]]; then
        run_grid_tests
    else
        install_dependencies
        run_local_tests
    fi
    
    generate_summary
    
    print_message $GREEN "=== Test execution completed! ==="
    print_message $BLUE "Check the reports directory for detailed results."
}

# Run main function
main