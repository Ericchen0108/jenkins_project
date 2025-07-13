pipeline {
    agent any
    
    environment {
        REPORTS_DIR = 'reports'
        SCREENSHOTS_DIR = 'reports/screenshots'
        HEADLESS = 'true'
    }
    
    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'smoke', 'regression', 'youtube_search', 'youtube_video', 'youtube_navigation'],
            description: 'Select test suite to run'
        )
        choice(
            name: 'BROWSER_TYPE',
            choices: ['chrome', 'firefox', 'edge'],
            description: 'Select browser for testing'
        )
        booleanParam(
            name: 'PARALLEL_EXECUTION',
            defaultValue: false,
            description: 'Run tests in parallel'
        )
        string(
            name: 'PARALLEL_COUNT',
            defaultValue: '2',
            description: 'Number of parallel processes (if parallel execution is enabled)'
        )
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out source code..."
                    // Git checkout is handled automatically by Jenkins
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    echo "Setting up test environment..."
                    sh '''
                        # Create reports directory
                        mkdir -p ${REPORTS_DIR}
                        mkdir -p ${SCREENSHOTS_DIR}
                        
                        # Clean previous reports
                        rm -f ${REPORTS_DIR}/*.html
                        rm -f ${SCREENSHOTS_DIR}/*.png
                        
                        # Set environment variables
                        export HEADLESS=true
                        export SCREENSHOT_ON_FAILURE=true
                    '''
                }
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    echo "Setting up Python virtual environment..."
                    sh '''
                        # Create virtual environment if it doesn't exist
                        if [ ! -d "venv" ]; then
                            python3 -m venv venv
                        fi
                        
                        # Activate virtual environment and install dependencies
                        source venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            parallel {
                stage('Smoke Tests') {
                    when {
                        expression { params.TEST_SUITE == 'all' || params.TEST_SUITE == 'smoke' }
                    }
                    steps {
                        script {
                            echo "Running Smoke Tests..."
                            runTests('smoke', 'smoke_report.html')
                        }
                    }
                }
                
                stage('Search Tests') {
                    when {
                        expression { params.TEST_SUITE == 'all' || params.TEST_SUITE == 'youtube_search' }
                    }
                    steps {
                        script {
                            echo "Running YouTube Search Tests..."
                            runTests('youtube_search', 'search_report.html')
                        }
                    }
                }
                
                stage('Video Tests') {
                    when {
                        expression { params.TEST_SUITE == 'all' || params.TEST_SUITE == 'youtube_video' }
                    }
                    steps {
                        script {
                            echo "Running YouTube Video Tests..."
                            runTests('youtube_video', 'video_report.html')
                        }
                    }
                }
                
                stage('Navigation Tests') {
                    when {
                        expression { params.TEST_SUITE == 'all' || params.TEST_SUITE == 'youtube_navigation' }
                    }
                    steps {
                        script {
                            echo "Running YouTube Navigation Tests..."
                            runTests('youtube_navigation', 'navigation_report.html')
                        }
                    }
                }
                
                stage('Regression Tests') {
                    when {
                        expression { params.TEST_SUITE == 'regression' }
                    }
                    steps {
                        script {
                            echo "Running Regression Tests..."
                            runTests('regression', 'regression_report.html')
                        }
                    }
                }
            }
        }
        
        stage('Cross-Browser Testing') {
            when {
                expression { params.TEST_SUITE == 'all' }
            }
            parallel {
                stage('Chrome Browser') {
                    steps {
                        script {
                            echo "Running tests on Chrome..."
                            runBrowserTests('chrome', 'chrome_browser_report.html')
                        }
                    }
                }
                
                stage('Firefox Browser') {
                    steps {
                        script {
                            echo "Running tests on Firefox..."
                            runBrowserTests('firefox', 'firefox_browser_report.html')
                        }
                    }
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                script {
                    echo "Generating test reports..."
                    sh '''
                        # List all generated reports
                        echo "Generated Reports:"
                        ls -la ${REPORTS_DIR}/*.html || true
                        
                        # List screenshots if any
                        echo "Screenshots:"
                        ls -la ${SCREENSHOTS_DIR}/*.png || true
                        
                        # Generate combined report if multiple reports exist
                        if [ $(ls ${REPORTS_DIR}/*.html 2>/dev/null | wc -l) -gt 1 ]; then
                            echo "Multiple reports found. Consider combining them."
                        fi
                    '''
                }
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                script {
                    echo "Archiving test artifacts..."
                    // Archive HTML reports
                    archiveArtifacts artifacts: 'reports/*.html', fingerprint: true, allowEmptyArchive: true
                    
                    // Archive screenshots
                    archiveArtifacts artifacts: 'reports/screenshots/*.png', fingerprint: true, allowEmptyArchive: true
                    
                    // Publish HTML reports
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: '*.html',
                        reportName: 'Selenium Test Report',
                        reportTitles: 'YouTube Selenium Tests'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "Pipeline completed. Cleaning up..."
                
                // Clean up temporary files
                sh "rm -rf .pytest_cache || true"
                
                // Note: We generate HTML reports, not XML
                echo "Test results are in HTML format in reports/ directory"
                
                // Clean old artifacts (keep last 10 builds)
                cleanWs(cleanWhenAborted: true, cleanWhenFailure: false, cleanWhenNotBuilt: true, cleanWhenSuccess: true)
            }
        }
        
        success {
            script {
                echo "✅ All tests passed successfully!"
                
                // Send success notification
                emailext (
                    subject: "✅ Selenium Tests PASSED - Build #${BUILD_NUMBER}",
                    body: """
                    <h2>Selenium Test Results - SUCCESS</h2>
                    <p><strong>Build:</strong> #${BUILD_NUMBER}</p>
                    <p><strong>Test Suite:</strong> ${params.TEST_SUITE}</p>
                    <p><strong>Browser:</strong> ${params.BROWSER_TYPE}</p>
                    <p><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p><strong>Test Reports:</strong> <a href="${BUILD_URL}Selenium_Test_Report/">View Reports</a></p>
                    
                    <p>All tests completed successfully! 🎉</p>
                    """,
                    mimeType: 'text/html',
                    to: "admin@localhost",
                    attachLog: false
                )
            }
        }
        
        failure {
            script {
                echo "❌ Some tests failed!"
                
                // Send failure notification
                emailext (
                    subject: "❌ Selenium Tests FAILED - Build #${BUILD_NUMBER}",
                    body: """
                    <h2>Selenium Test Results - FAILURE</h2>
                    <p><strong>Build:</strong> #${BUILD_NUMBER}</p>
                    <p><strong>Test Suite:</strong> ${params.TEST_SUITE}</p>
                    <p><strong>Browser:</strong> ${params.BROWSER_TYPE}</p>
                    <p><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p><strong>Test Reports:</strong> <a href="${BUILD_URL}Selenium_Test_Report/">View Reports</a></p>
                    <p><strong>Console Log:</strong> <a href="${BUILD_URL}console">View Console</a></p>
                    
                    <p>Some tests failed. Please check the reports and console log for details.</p>
                    """,
                    mimeType: 'text/html',
                    to: "admin@localhost",
                    attachLog: true
                )
            }
        }
        
        unstable {
            script {
                echo "⚠️ Tests completed with warnings!"
                
                // Send unstable notification
                emailext (
                    subject: "⚠️ Selenium Tests UNSTABLE - Build #${BUILD_NUMBER}",
                    body: """
                    <h2>Selenium Test Results - UNSTABLE</h2>
                    <p><strong>Build:</strong> #${BUILD_NUMBER}</p>
                    <p><strong>Test Suite:</strong> ${params.TEST_SUITE}</p>
                    <p><strong>Browser:</strong> ${params.BROWSER_TYPE}</p>
                    <p><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p><strong>Test Reports:</strong> <a href="${BUILD_URL}Selenium_Test_Report/">View Reports</a></p>
                    
                    <p>Tests completed with some issues. Please review the results.</p>
                    """,
                    mimeType: 'text/html',
                    to: "admin@localhost",
                    attachLog: false
                )
            }
        }
    }
}

// Helper function to run tests with specific markers
def runTests(marker, reportName) {
    def parallelArgs = params.PARALLEL_EXECUTION ? "-n ${params.PARALLEL_COUNT}" : ""
    
    sh """
        # Run tests locally without Docker for now
        export BROWSER='${params.BROWSER_TYPE}'
        export HEADLESS=true
        export SCREENSHOT_ON_FAILURE=true
        
        # Activate virtual environment and run tests
        source venv/bin/activate
        pytest -m "${marker}" ${parallelArgs} \
            --html=reports/${reportName} \
            --self-contained-html \
            --tb=short \
            -v
    """
}

// Helper function to run browser-specific tests
def runBrowserTests(browser, reportName) {
    sh """
        # Run tests locally without Docker for now
        export BROWSER='${browser}'
        export HEADLESS=true
        export SCREENSHOT_ON_FAILURE=true
        
        # Activate virtual environment and run tests
        source venv/bin/activate
        pytest -m "smoke" \
            --html=reports/${reportName} \
            --self-contained-html \
            --tb=short \
            -v
    """
}