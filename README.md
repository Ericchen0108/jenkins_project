# 🚀 Selenium YouTube Test Automation with Jenkins CI/CD

A **production-ready, enterprise-grade** test automation framework for YouTube functionality using Selenium WebDriver, Python, and Jenkins CI/CD pipeline. Built with industry best practices including Page Object Model, parallel execution, cross-browser testing, and comprehensive reporting.

## ✨ Key Features

### 🏗️ **Architecture & Design**
- **Page Object Model (POM)** - Clean, maintainable test architecture with 4 page classes
- **Modular Design** - Separation of concerns with organized directory structure
- **Factory Pattern** - Flexible driver management for multiple browsers
- **Multi-Environment Support** - Local, Dev, Staging, Prod, CI configurations

### 🧪 **Comprehensive Test Coverage**
- **70+ Test Methods** across 4 main test suites
- **Navigation Testing** - Homepage, menu, logo, responsive design (10+ tests)
- **Search Functionality** - Basic search, filters, special characters (8+ tests)
- **Video Testing** - Playback, controls, metadata, interactions (10+ tests)
- **Browser Compatibility** - Cross-browser testing and validation (15+ tests)

### 🚀 **CI/CD Pipeline**
- **Jenkins Integration** - Production-ready pipeline with 8 stages
- **Parallel Execution** - Multiple test suites run concurrently
- **Parameterized Builds** - Configurable test suite, browser, parallel settings
- **Cross-Browser Testing** - Automated Chrome, Firefox, Edge testing
- **Email Notifications** - Success/failure/unstable build alerts
- **HTML Reports** - Comprehensive test reports with screenshots

### 🌐 **Multi-Browser Support**
- **Chrome** - Full support with headless mode and custom options
- **Firefox** - GeckoDriver integration with profile customization
- **Edge** - EdgeChromium driver support
- **Parallel Browser Testing** - Concurrent execution across browsers

### 🐳 **Docker & Containerization**
- **Multi-Architecture Support** - AMD64 and ARM64 compatibility
- **Selenium Grid Setup** - Hub and node configuration
- **Docker Compose** - Multi-service orchestration
- **Volume Mounting** - Persistent reports and screenshots

### 📊 **Advanced Reporting**
- **HTML Reports** - Self-contained reports with embedded assets
- **Screenshot Capture** - Automatic failure screenshots with timestamps
- **Test Metadata** - Execution time, environment details, browser info
- **Jenkins Integration** - HTML Publisher plugin for report viewing

## 🏁 Quick Start

### Prerequisites
- Python 3.9+ 
- Git
- Chrome/Firefox/Edge browsers
- Docker (optional)
- Jenkins (for CI/CD)

### Local Setup
```bash
# Clone the repository
git clone https://github.com/Ericchen0108/jenkins_project.git
cd jenkins_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\\Scripts\\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run smoke tests
pytest -m smoke --html=reports/smoke_report.html --self-contained-html

# Run all tests with parallel execution
pytest -n 2 --html=reports/full_report.html --self-contained-html
```

### Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run specific test suite
docker-compose run selenium-tests pytest -m youtube_search
```

## 🎯 Test Execution Options

### Test Markers
- `smoke` - Quick validation tests (5-10 minutes)
- `regression` - Comprehensive test coverage (20-30 minutes)
- `youtube_search` - Search functionality tests
- `youtube_video` - Video playback tests
- `youtube_navigation` - Navigation and UI tests

### Browser Selection
```bash
# Chrome (default)
pytest --browser=chrome

# Firefox
pytest --browser=firefox

# Edge
pytest --browser=edge

# Headless mode
pytest --browser=chrome --headless=true
```

### Parallel Execution
```bash
# Run with 4 parallel workers
pytest -n 4

# Run specific suite in parallel
pytest -m smoke -n 2
```

## 🔧 Configuration

### Environment Configuration
Edit `config/environments.py` for environment-specific settings:
- **Timeouts** - Page load, element wait, implicit wait
- **Browser Settings** - Window size, headless mode, options
- **Retry Policies** - Test retry count and delay
- **Screenshot Settings** - Capture mode and storage

### Test Data Management
- `config/test_data.json` - Structured test data
- `config/test_data.py` - Dynamic test data generation
- Environment variable overrides supported

## 🚀 Jenkins CI/CD Pipeline

### Pipeline Features
- **Automated Triggers** - Git polling every 2 minutes
- **Parameterized Builds** - Customizable test execution
- **Parallel Stages** - Concurrent test suite execution
- **Cross-Browser Testing** - Automated multi-browser validation
- **Report Publishing** - HTML reports accessible via Jenkins UI
- **Email Notifications** - Build status alerts

### Build Parameters
- **TEST_SUITE** - `all`, `smoke`, `regression`, `youtube_search`, `youtube_video`, `youtube_navigation`
- **BROWSER_TYPE** - `chrome`, `firefox`, `edge`
- **PARALLEL_EXECUTION** - `true`/`false`
- **PARALLEL_COUNT** - Number of parallel workers (default: 2)

### Setting Up Jenkins
1. Install Jenkins and required plugins (Git, HTML Publisher, Email Extension)
2. Create new Pipeline job
3. Configure Git repository: `https://github.com/Ericchen0108/jenkins_project.git`
4. Set branch to `*/main`
5. Configure polling: `H/2 * * * *` (every 2 minutes)
6. Run build with parameters

## 📊 Reporting & Analysis

### HTML Reports
- **Self-contained reports** with embedded CSS/JS
- **Failure screenshots** automatically captured
- **Test execution metrics** and timing data
- **Environment and browser information**

### Screenshot Management
- **Automatic capture** on test failures
- **Timestamped filenames** for easy identification
- **Organized storage** in reports/screenshots/
- **Multiple capture modes** (element, full page)

### Jenkins Integration
- **HTML Publisher** plugin for report viewing
- **Build artifacts** archived automatically
- **Trend analysis** with build history
- **Email notifications** with report links

## 🗂️ Project Structure

```
jenkins_project/
├── 📁 config/              # Configuration management
│   ├── config.py          # Main configuration
│   ├── environments.py    # Environment-specific settings
│   ├── test_data.json     # Structured test data
│   └── test_data.py       # Dynamic test data
├── 📁 pages/               # Page Object Model
│   ├── base_page.py       # Base page with common methods
│   ├── home_page.py       # YouTube homepage
│   ├── search_page.py     # Search functionality
│   └── video_page.py      # Video playback page
├── 📁 tests/               # Test suites
│   ├── conftest.py        # Test fixtures and setup
│   ├── test_youtube_navigation.py   # Navigation tests
│   ├── test_youtube_search.py      # Search tests
│   ├── test_youtube_video.py       # Video tests
│   └── test_browser_compatibility.py  # Cross-browser tests
├── 📁 utils/               # Utility functions
│   ├── driver_manager.py  # Browser driver management
│   ├── screenshot_utils.py # Screenshot capture
│   └── test_helpers.py    # Test helper functions
├── 📁 fixtures/            # Test fixtures and data
├── 📁 scripts/             # Automation scripts
├── 🐳 Dockerfile          # Container configuration
├── 🐳 docker-compose.yml  # Multi-service setup
├── 🚀 Jenkinsfile         # CI/CD pipeline definition
├── 📋 requirements.txt    # Python dependencies
├── ⚙️ pytest.ini          # Pytest configuration
└── 📚 Documentation files
```

## 🔧 Advanced Features

### Selenium Grid Support
- **Hub and Node Configuration** in docker-compose.yml
- **Scalable Test Execution** across multiple containers
- **Load Balancing** with automatic node selection

### Performance Testing
- **Page Load Time Measurement**
- **Search Performance Validation**
- **Memory Usage Monitoring**

### Accessibility Testing
- **Keyboard Navigation Tests**
- **Screen Reader Compatibility**
- **ARIA Attributes Validation**

### Responsive Testing
- **Multiple Screen Resolutions**
- **Mobile Device Simulation**
- **Cross-Device Compatibility**

## 🛠️ Troubleshooting

### Common Issues
1. **Driver Issues** - Automatic driver download via webdriver-manager
2. **Timeout Issues** - Configurable wait times in environments.py
3. **Docker Issues** - Check Docker daemon and permissions
4. **Jenkins Issues** - Verify Git configuration and permissions

### Debug Mode
```bash
# Run with verbose output
pytest -v -s

# Run single test with debugging
pytest tests/test_youtube_navigation.py::TestYouTubeNavigation::test_homepage_load -v -s

# Generate detailed HTML report
pytest --html=reports/debug_report.html --self-contained-html --tb=long
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🚀 Future Enhancements

- [ ] API Testing Integration
- [ ] Visual Regression Testing
- [ ] Mobile App Testing Support
- [ ] Database Testing Integration
- [ ] Performance Benchmarking
- [ ] AI-Powered Test Generation

---

**Built with ❤️ for robust, scalable test automation**