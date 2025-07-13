#!/bin/bash

# Cross-Browser Testing Script
# This script runs tests across multiple browsers for compatibility validation

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

# Default configuration
BROWSERS=("chrome" "firefox" "edge")
TEST_SUITE="browser_compatibility"
PARALLEL="false"
HEADLESS="true"
GENERATE_COMPARISON="true"

# Function to show help
show_help() {
    cat << EOF
Cross-Browser Testing Script

Usage: $0 [OPTIONS]

OPTIONS:
    -b, --browsers BROWSERS    Comma-separated list of browsers (chrome,firefox,edge)
    -s, --suite SUITE         Test suite to run (default: browser_compatibility)
    -p, --parallel            Run browsers in parallel
    -h, --headless            Run in headless mode (default: true)
    --no-comparison           Skip generating comparison report
    --help                    Show this help message

EXAMPLES:
    $0 --browsers chrome,firefox --parallel
    $0 --suite smoke --browsers chrome,firefox,edge
    $0 --no-comparison --browsers chrome

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--browsers)
            IFS=',' read -ra BROWSERS <<< "$2"
            shift 2
            ;;
        -s|--suite)
            TEST_SUITE="$2"
            shift 2
            ;;
        -p|--parallel)
            PARALLEL="true"
            shift
            ;;
        -h|--headless)
            HEADLESS="true"
            shift
            ;;
        --no-comparison)
            GENERATE_COMPARISON="false"
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

# Function to validate browser availability
validate_browsers() {
    print_message $BLUE "Validating browser availability..."
    
    for browser in "${BROWSERS[@]}"; do
        case $browser in
            chrome)
                if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
                    print_message $GREEN "✓ Chrome is available"
                else
                    print_message $YELLOW "⚠ Chrome may not be available"
                fi
                ;;
            firefox)
                if command -v firefox &> /dev/null; then
                    print_message $GREEN "✓ Firefox is available"
                else
                    print_message $YELLOW "⚠ Firefox may not be available"
                fi
                ;;
            edge)
                if command -v microsoft-edge &> /dev/null; then
                    print_message $GREEN "✓ Edge is available"
                else
                    print_message $YELLOW "⚠ Edge may not be available (will use chromium-based fallback)"
                fi
                ;;
            *)
                print_message $RED "✗ Unknown browser: $browser"
                exit 1
                ;;
        esac
    done
}

# Function to run tests for a single browser
run_browser_tests() {
    local browser=$1
    local report_name="reports/${browser}_browser_report.html"
    
    print_message $BLUE "Running tests for $browser..."
    
    # Set environment variables
    export BROWSER=$browser
    export HEADLESS=$HEADLESS
    export SCREENSHOT_ON_FAILURE=true
    
    # Create browser-specific report directory
    mkdir -p "reports/screenshots/$browser"
    
    # Run tests
    if pytest -m "$TEST_SUITE" \
        --html="$report_name" \
        --self-contained-html \
        --tb=short \
        -v \
        --browser="$browser"; then
        
        print_message $GREEN "✓ $browser tests completed successfully"
        return 0
    else
        print_message $RED "✗ $browser tests failed"
        return 1
    fi
}

# Function to run tests in parallel
run_parallel_tests() {
    print_message $BLUE "Running cross-browser tests in parallel..."
    
    local pids=()
    local results=()
    
    # Start tests for each browser in background
    for browser in "${BROWSERS[@]}"; do
        print_message $YELLOW "Starting tests for $browser in background..."
        run_browser_tests "$browser" &
        pids+=($!)
    done
    
    # Wait for all background processes to complete
    for i in "${!pids[@]}"; do
        local pid=${pids[$i]}
        local browser=${BROWSERS[$i]}
        
        if wait $pid; then
            results+=("$browser:SUCCESS")
            print_message $GREEN "✓ $browser tests completed"
        else
            results+=("$browser:FAILED")
            print_message $RED "✗ $browser tests failed"
        fi
    done
    
    # Print summary
    print_message $BLUE "Parallel execution summary:"
    for result in "${results[@]}"; do
        IFS=':' read -ra PARTS <<< "$result"
        local browser=${PARTS[0]}
        local status=${PARTS[1]}
        
        if [[ "$status" == "SUCCESS" ]]; then
            print_message $GREEN "  $browser: $status"
        else
            print_message $RED "  $browser: $status"
        fi
    done
}

# Function to run tests sequentially
run_sequential_tests() {
    print_message $BLUE "Running cross-browser tests sequentially..."
    
    local failed_browsers=()
    
    for browser in "${BROWSERS[@]}"; do
        if ! run_browser_tests "$browser"; then
            failed_browsers+=("$browser")
        fi
        
        # Small delay between browsers
        sleep 2
    done
    
    # Report failures
    if [[ ${#failed_browsers[@]} -gt 0 ]]; then
        print_message $RED "Failed browsers: ${failed_browsers[*]}"
        return 1
    else
        print_message $GREEN "All browser tests completed successfully!"
        return 0
    fi
}

# Function to generate comparison report
generate_comparison_report() {
    print_message $BLUE "Generating cross-browser comparison report..."
    
    local comparison_file="reports/cross_browser_comparison.html"
    
    cat > "$comparison_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Cross-Browser Test Comparison</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f4f4f4; padding: 15px; border-radius: 5px; }
        .browser-section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .success { color: green; }
        .failure { color: red; }
        .warning { color: orange; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Cross-Browser Test Comparison Report</h1>
        <p><strong>Generated:</strong> $(date)</p>
        <p><strong>Test Suite:</strong> $TEST_SUITE</p>
        <p><strong>Browsers Tested:</strong> ${BROWSERS[*]}</p>
    </div>

    <h2>Test Results Summary</h2>
    <table>
        <tr>
            <th>Browser</th>
            <th>Report Status</th>
            <th>Report Link</th>
            <th>Screenshots</th>
        </tr>
EOF

    # Add browser results to table
    for browser in "${BROWSERS[@]}"; do
        local report_file="${browser}_browser_report.html"
        local report_status="Unknown"
        local report_link="N/A"
        local screenshot_count=0
        
        if [[ -f "reports/$report_file" ]]; then
            report_status="Generated"
            report_link="<a href='$report_file'>View Report</a>"
        else
            report_status="Missing"
        fi
        
        # Count screenshots
        if [[ -d "reports/screenshots/$browser" ]]; then
            screenshot_count=$(find "reports/screenshots/$browser" -name "*.png" | wc -l)
        fi
        
        cat >> "$comparison_file" << EOF
        <tr>
            <td>$browser</td>
            <td>$report_status</td>
            <td>$report_link</td>
            <td>$screenshot_count</td>
        </tr>
EOF
    done
    
    cat >> "$comparison_file" << EOF
    </table>

    <h2>Individual Browser Reports</h2>
EOF

    # Add browser-specific sections
    for browser in "${BROWSERS[@]}"; do
        local report_file="reports/${browser}_browser_report.html"
        
        cat >> "$comparison_file" << EOF
    <div class="browser-section">
        <h3>$browser Browser Results</h3>
EOF
        
        if [[ -f "$report_file" ]]; then
            cat >> "$comparison_file" << EOF
        <p class="success">✓ Report generated successfully</p>
        <p><a href="${browser}_browser_report.html">View $browser Test Report</a></p>
EOF
        else
            cat >> "$comparison_file" << EOF
        <p class="failure">✗ Report not found</p>
        <p>Tests may have failed or not been executed for this browser.</p>
EOF
        fi
        
        cat >> "$comparison_file" << EOF
    </div>
EOF
    done
    
    cat >> "$comparison_file" << EOF
    
    <h2>Notes</h2>
    <ul>
        <li>All tests were executed with HEADLESS=$HEADLESS</li>
        <li>Screenshots are captured on test failures</li>
        <li>Parallel execution: $PARALLEL</li>
        <li>This report was generated automatically by the cross-browser testing script</li>
    </ul>

</body>
</html>
EOF

    print_message $GREEN "Comparison report generated: $comparison_file"
}

# Function to setup environment
setup_environment() {
    print_message $BLUE "Setting up cross-browser test environment..."
    
    # Create directories
    mkdir -p reports/screenshots
    
    # Clean previous reports
    rm -f reports/*_browser_report.html
    rm -f reports/cross_browser_comparison.html
    
    # Create browser-specific screenshot directories
    for browser in "${BROWSERS[@]}"; do
        mkdir -p "reports/screenshots/$browser"
    done
}

# Main execution function
main() {
    print_message $GREEN "=== Cross-Browser Testing Script ==="
    print_message $BLUE "Configuration:"
    print_message $YELLOW "  Browsers: ${BROWSERS[*]}"
    print_message $YELLOW "  Test Suite: $TEST_SUITE"
    print_message $YELLOW "  Parallel: $PARALLEL"
    print_message $YELLOW "  Headless: $HEADLESS"
    echo
    
    validate_browsers
    setup_environment
    
    local exit_code=0
    
    if [[ "$PARALLEL" == "true" ]]; then
        run_parallel_tests
        exit_code=$?
    else
        run_sequential_tests
        exit_code=$?
    fi
    
    if [[ "$GENERATE_COMPARISON" == "true" ]]; then
        generate_comparison_report
    fi
    
    print_message $GREEN "=== Cross-browser testing completed! ==="
    
    if [[ $exit_code -eq 0 ]]; then
        print_message $GREEN "All tests passed across all browsers! 🎉"
    else
        print_message $RED "Some tests failed. Check the reports for details."
    fi
    
    print_message $BLUE "Reports available in the 'reports' directory:"
    ls -la reports/*.html 2>/dev/null || print_message $YELLOW "No HTML reports found"
    
    exit $exit_code
}

# Run main function
main