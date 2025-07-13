# Selenium YouTube Test Automation with Jenkins CI/CD

A comprehensive test automation framework for YouTube functionality using Selenium WebDriver, Python, and Jenkins CI/CD pipeline.

## 🚀 Features

- **Page Object Model**: Maintainable test architecture
- **Cross-Browser Testing**: Chrome, Firefox, Edge support
- **Parallel Execution**: Speed up test runs with pytest-xdist
- **Docker Integration**: Containerized test execution
- **Jenkins CI/CD**: Automated pipeline with reporting
- **HTML Reports**: Detailed test reports with screenshots
- **Screenshot Capture**: Automatic screenshots on test failures
- **Environment Configuration**: Multiple environment support

## 📋 Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Jenkins (for CI/CD)
- Git

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd selenium-youtube-tests
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
BROWSER=chrome
HEADLESS=false
SCREENSHOT_ON_FAILURE=true
PARALLEL_TESTS=1
TEST_ENVIRONMENT=local
```

## 🏃 Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test suite
pytest -m smoke
pytest -m regression
pytest -m youtube_search

# Run with specific browser
BROWSER=firefox pytest

# Run in headless mode
HEADLESS=true pytest
```

### Using the Test Runner Script

```bash
# Basic smoke tests
./scripts/run_tests.sh --suite smoke --browser chrome

# Parallel execution
./scripts/run_tests.sh --suite all --parallel --count 4

# Different environment
./scripts/run_tests.sh --suite regression --env staging --headless

# Using Docker
./scripts/run_tests.sh --docker --suite smoke

# Using Selenium Grid
./scripts/run_tests.sh --grid --suite all --parallel --count 8
```

### Docker Execution

```bash
# Build and run tests in Docker
docker build -t selenium-youtube-tests .
docker run --rm -v $(pwd)/reports:/app/reports selenium-youtube-tests

# Using Docker Compose
docker-compose up selenium-tests

# Cross-browser testing with Docker Compose
docker-compose up selenium-tests-chrome selenium-tests-firefox
```

### Selenium Grid

```bash
# Start Selenium Grid
docker-compose up -d selenium-grid-hub selenium-chrome selenium-firefox

# Run tests on grid
docker-compose up selenium-tests-grid

# Stop grid
docker-compose down
```

## 📊 Test Reporting

### HTML Reports

Tests generate HTML reports with:
- Test execution summary
- Pass/fail status for each test
- Screenshots on failures
- Execution time and environment details

Reports are saved in the `reports/` directory:
- `reports/report.html` - Main test report
- `reports/screenshots/` - Screenshot directory

### Viewing Reports

```bash
# Open report in browser (macOS)
open reports/report.html

# Open report in browser (Linux)
xdg-open reports/report.html

# Open report in browser (Windows)
start reports/report.html
```

## 🔧 Jenkins Setup

### 1. Install Required Plugins

In Jenkins, install these plugins:
- Pipeline
- HTML Publisher
- Docker Pipeline
- Email Extension
- Allure (optional)

### 2. Create Jenkins Job

```bash
# Run the Jenkins setup script
./scripts/jenkins_setup.sh
```

Follow the instructions to:
1. Create a new Pipeline job
2. Configure parameters
3. Set up SCM (Git)
4. Configure build triggers

### 3. Pipeline Configuration

The `Jenkinsfile` includes:
- Multi-stage pipeline
- Parallel test execution
- Cross-browser testing
- Docker integration
- Report generation
- Email notifications

### 4. Manual Job Creation

1. Open Jenkins → New Item
2. Enter job name: `selenium-youtube-tests`
3. Select "Pipeline"
4. Configure:
   - **Description**: Selenium YouTube Test Automation
   - **Parameters**: Defined in Jenkinsfile
   - **Pipeline**: Pipeline script from SCM
   - **Repository URL**: Your Git repository
   - **Branch**: `main`
   - **Script Path**: `Jenkinsfile`

## 🧪 Test Structure

```
selenium-youtube-tests/
├── tests/                     # Test files
│   ├── test_youtube_search.py
│   ├── test_youtube_navigation.py
│   ├── test_youtube_video.py
│   └── conftest.py
├── pages/                     # Page Object Models
│   ├── base_page.py
│   ├── home_page.py
│   ├── search_page.py
│   └── video_page.py
├── utils/                     # Utility functions
│   ├── driver_manager.py
│   ├── test_helpers.py
│   └── screenshot_utils.py
├── config/                    # Configuration files
│   ├── config.py
│   ├── environments.py
│   ├── test_data.py
│   └── test_data.json
├── fixtures/                  # Test fixtures
│   └── test_fixtures.py
├── scripts/                   # Helper scripts
│   ├── run_tests.sh
│   └── jenkins_setup.sh
├── reports/                   # Test reports
└── jenkins/                   # Jenkins configuration
    └── job-config.xml
```

## 🎯 Test Categories

### Smoke Tests
Quick validation of core functionality:
```bash
pytest -m smoke
```

### Regression Tests
Comprehensive test suite:
```bash
pytest -m regression
```

### Feature-Specific Tests
```bash
pytest -m youtube_search      # Search functionality
pytest -m youtube_video       # Video playback
pytest -m youtube_navigation  # Navigation features
```

## 🔧 Configuration

### Browser Configuration

```python
# config/config.py
BROWSER = "chrome"  # chrome, firefox, edge
HEADLESS = True     # Run in headless mode
```

### Environment Configuration

```python
# config/environments.py
environment_config = {
    "local": {...},
    "staging": {...},
    "production": {...}
}
```

### Test Data Configuration

```json
// config/test_data.json
{
  "search_terms": {
    "valid": ["Python programming", "Web development"],
    "invalid": ["", "   ", "nonexistent"]
  },
  "video_categories": ["Education", "Technology", "Music"]
}
```

## 🚀 Advanced Features

### Parallel Execution

```bash
# Run 4 tests in parallel
pytest -n 4

# Using the runner script
./scripts/run_tests.sh --parallel --count 4
```

### Cross-Browser Testing

```bash
# Test across multiple browsers
BROWSER=chrome pytest -m smoke
BROWSER=firefox pytest -m smoke
BROWSER=edge pytest -m smoke
```

### Performance Testing

```bash
# Run with performance monitoring
pytest --tb=short -v --durations=10
```

### Screenshot Management

Screenshots are automatically captured:
- On test failures
- In parallel execution (worker-specific directories)
- With configurable retention policies

## 📧 Email Notifications

Configure in Jenkins:
1. Manage Jenkins → Configure System
2. E-mail Notification
3. Extended E-mail Notification

The pipeline will send notifications on:
- ✅ Success
- ❌ Failure
- ⚠️ Unstable builds

## 🐛 Troubleshooting

### Common Issues

1. **Browser Driver Issues**
   ```bash
   # Update WebDriver Manager
   pip install --upgrade webdriver-manager
   ```

2. **Docker Permission Issues**
   ```bash
   # Add user to docker group
   sudo usermod -aG docker $USER
   ```

3. **Port Conflicts**
   ```bash
   # Check if ports are in use
   lsof -i :4444  # Selenium Grid
   lsof -i :8080  # Jenkins
   ```

4. **Memory Issues in Docker**
   ```bash
   # Increase shared memory
   docker run --shm-size=2g selenium-youtube-tests
   ```

### Debug Mode

```bash
# Run with verbose output
pytest -v -s

# Run single test for debugging
pytest tests/test_youtube_search.py::TestYouTubeSearch::test_search_basic_functionality -v -s
```

### Log Files

Check logs in:
- `reports/` - Test execution logs
- Jenkins console output
- Docker container logs: `docker logs <container-id>`

## 🔒 Security Considerations

- Never commit sensitive data to repository
- Use environment variables for credentials
- Secure Jenkins with authentication
- Regular security updates for dependencies

## 📈 Performance Optimization

1. **Parallel Execution**: Use `-n auto` for optimal worker count
2. **Headless Mode**: Faster execution in CI/CD
3. **Docker Resources**: Allocate sufficient memory and CPU
4. **Test Data**: Use parameterized tests efficiently

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support:
1. Check the troubleshooting section
2. Review Jenkins build logs
3. Check Docker container logs
4. Open an issue in the repository

---

## Quick Start Commands

```bash
# Setup
git clone <repo> && cd selenium-youtube-tests
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Run Tests
./scripts/run_tests.sh --suite smoke --browser chrome
./scripts/run_tests.sh --docker --suite all
./scripts/run_tests.sh --grid --parallel --count 4

# Jenkins
./scripts/jenkins_setup.sh
# Then create job manually in Jenkins UI

# View Reports
open reports/report.html
```

Happy Testing! 🎉