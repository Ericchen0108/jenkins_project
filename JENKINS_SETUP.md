# Jenkins Setup Guide for Selenium Testing

This guide provides step-by-step instructions to install and configure Jenkins for the Selenium YouTube test automation project.

## 🚀 Quick Jenkins Installation

### Option 1: Using Homebrew (macOS - Recommended)

```bash
# Install Jenkins using Homebrew
brew install jenkins

# Start Jenkins service
brew services start jenkins

# Access Jenkins at: http://localhost:8080
```

### Option 2: Using Docker (Cross-platform)

```bash
# Run Jenkins in Docker
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  --name jenkins \
  jenkins/jenkins:lts

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Option 3: Manual Installation (Linux/macOS)

```bash
# Download Jenkins LTS
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

# Add Jenkins repository
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt-get update
sudo apt-get install jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

## 🔧 Initial Jenkins Configuration

### 1. Access Jenkins Web Interface

1. Open your browser and go to: `http://localhost:8080`
2. You'll see the "Unlock Jenkins" page

### 2. Unlock Jenkins

```bash
# Get the initial admin password
# For Homebrew installation:
cat /usr/local/var/jenkins_home/secrets/initialAdminPassword

# For Docker installation:
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# For manual installation:
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### 3. Install Suggested Plugins

1. Select "Install suggested plugins"
2. Wait for plugins to install (takes 5-10 minutes)

### 4. Create Admin User

1. Fill in admin user details:
   - Username: `admin`
   - Password: `your-secure-password`
   - Full name: `Jenkins Admin`
   - Email: `your-email@example.com`

### 5. Configure Jenkins URL

1. Keep default URL: `http://localhost:8080/`
2. Click "Save and Finish"

## 📦 Required Plugins Installation

### Install Additional Plugins

1. Go to **Manage Jenkins** → **Manage Plugins** → **Available**
2. Search and install these plugins:

**Essential Plugins:**
- Pipeline (should be pre-installed)
- Pipeline: Stage View
- HTML Publisher
- Docker Pipeline
- Email Extension
- Build Timeout
- Timestamper
- Workspace Cleanup

**Optional Plugins:**
- Allure Jenkins Plugin
- GitHub Integration
- Slack Notification
- Blue Ocean (modern UI)

### Plugin Installation Commands (via Jenkins CLI)

```bash
# Download Jenkins CLI
wget http://localhost:8080/jnlpJars/jenkins-cli.jar

# Install plugins (replace USER:PASSWORD with your credentials)
java -jar jenkins-cli.jar -s http://localhost:8080 -auth USER:PASSWORD install-plugin \
  workflow-aggregator \
  pipeline-stage-view \
  html-publisher \
  docker-workflow \
  email-ext \
  build-timeout \
  timestamper \
  ws-cleanup
```

## 🛠️ Configure Jenkins for Selenium Testing

### 1. Global Tool Configuration

1. Go to **Manage Jenkins** → **Global Tool Configuration**

2. **Configure Git:**
   - Name: `Default`
   - Path to Git executable: `/usr/bin/git` (or your git path)

3. **Configure Docker:**
   - Name: `Docker`
   - Installation root: `/usr/local/bin/docker`

### 2. System Configuration

1. Go to **Manage Jenkins** → **Configure System**

2. **Configure Email Notification:**
   - SMTP server: `smtp.gmail.com` (or your SMTP server)
   - Default user email suffix: `@yourdomain.com`
   - Use SMTP Authentication: ✅
   - Username/Password: Your email credentials

3. **Configure Extended Email Notification:**
   - SMTP server: `smtp.gmail.com`
   - SMTP Port: `587`
   - Use SMTP Authentication: ✅
   - Use TLS: ✅

### 3. Security Configuration

1. **Manage Jenkins** → **Configure Global Security**
2. **Authorization:** Matrix-based security
3. Add your admin user with all permissions
4. Add anonymous user with Read permission (optional)

## 📋 Create the Selenium Test Job

### Using the Jenkins Setup Script

```bash
# Run our automated setup script
./scripts/jenkins_setup.sh
```

### Manual Job Creation

1. **New Item** → Enter name: `selenium-youtube-tests`
2. Select **Pipeline** → Click **OK**

3. **Configure Job:**
   - **Description:** Selenium YouTube Test Automation Pipeline
   - **Build Triggers:** 
     - ✅ Build periodically: `H 2 * * 1-5` (weekdays at 2 AM)
     - ✅ GitHub hook trigger (if using GitHub)
   
   - **Pipeline:**
     - Definition: **Pipeline script from SCM**
     - SCM: **Git**
     - Repository URL: `https://github.com/your-repo/selenium-youtube-tests.git`
     - Branch Specifier: `*/main`
     - Script Path: `Jenkinsfile`

4. **Save** the configuration

## 🧪 Test the Jenkins Pipeline

### 1. Manual Build Test

1. Go to your job: `selenium-youtube-tests`
2. Click **Build with Parameters**
3. Select parameters:
   - TEST_SUITE: `smoke`
   - BROWSER_TYPE: `chrome`
   - PARALLEL_EXECUTION: `false`
   - PARALLEL_COUNT: `2`
4. Click **Build**

### 2. Monitor Build Progress

1. Check **Build History**
2. Click on build number (e.g., `#1`)
3. View **Console Output** for detailed logs
4. Check **Test Results** and **HTML Reports**

### 3. Pipeline Stages

The pipeline includes these stages:
1. ✅ **Checkout** - Git repository checkout
2. ✅ **Setup Environment** - Create directories, set variables
3. ✅ **Build Docker Image** - Build test container
4. ✅ **Run Tests** - Execute test suites in parallel
5. ✅ **Cross-Browser Testing** - Chrome and Firefox
6. ✅ **Generate Reports** - Create HTML reports
7. ✅ **Archive Artifacts** - Save reports and screenshots

## 📊 Jenkins Dashboard and Reports

### View Test Reports

1. **Build** → **HTML Report** → **Selenium Test Report**
2. Review test results, screenshots, and metrics
3. Check **Artifacts** for downloadable reports

### Email Notifications

Configure in `Jenkinsfile`:
- ✅ Success notifications
- ❌ Failure notifications with logs
- ⚠️ Unstable build warnings

### Build Status

- **Blue ball** 🔵 = Success
- **Red ball** 🔴 = Failure  
- **Yellow ball** 🟡 = Unstable
- **Gray ball** ⚪ = Not built/Disabled

## 🔧 Troubleshooting Common Issues

### Issue 1: "Permission denied" errors

```bash
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Issue 2: Browsers not found in Docker

```bash
# Verify Docker image builds correctly
docker build -t selenium-youtube-tests .
docker run --rm selenium-youtube-tests which google-chrome
```

### Issue 3: Tests timing out

1. Increase timeouts in `config/config.py`
2. Use headless mode: `HEADLESS=true`
3. Add more retry attempts in `Jenkinsfile`

### Issue 4: Email notifications not working

1. Check SMTP settings in **Manage Jenkins** → **Configure System**
2. Test email configuration
3. Verify firewall/network settings

### Issue 5: Git authentication issues

1. Add Git credentials in **Manage Jenkins** → **Manage Credentials**
2. Use SSH keys instead of HTTPS
3. Configure webhook for automatic builds

## 📱 Mobile Testing Setup (Optional)

### Appium Integration

```bash
# Install Appium
npm install -g appium

# Install drivers
appium driver install uiautomator2
appium driver install xcuitest

# Configure in Jenkins
# Add Appium server as build step
```

## 🚀 Production Deployment

### Environment Variables for Production

```bash
# Set in Jenkins job configuration
HEADLESS=true
BROWSER=chrome
PARALLEL_TESTS=4
TEST_ENVIRONMENT=production
SCREENSHOT_ON_FAILURE=true
```

### Monitoring and Alerts

1. **Jenkins Health Check:** Enable in **Manage Jenkins**
2. **Disk Space Monitoring:** Configure thresholds
3. **Build Notifications:** Slack, Microsoft Teams integration
4. **Performance Metrics:** Track test execution times

## 🔒 Security Best Practices

1. **Regular Updates:** Keep Jenkins and plugins updated
2. **Access Control:** Use matrix-based security
3. **Credentials Management:** Store secrets securely
4. **Network Security:** Configure firewall rules
5. **Backup Strategy:** Regular Jenkins home backup

## 📚 Additional Resources

- [Jenkins Official Documentation](https://www.jenkins.io/doc/)
- [Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Docker Plugin Documentation](https://plugins.jenkins.io/docker-workflow/)
- [HTML Publisher Plugin](https://plugins.jenkins.io/htmlpublisher/)

---

## ✅ Quick Verification Checklist

- [ ] Jenkins installed and running on port 8080
- [ ] Initial admin password retrieved and used
- [ ] Required plugins installed
- [ ] Email notifications configured
- [ ] Git repository accessible
- [ ] Docker working (if using containerized tests)
- [ ] First test job created and executed successfully
- [ ] HTML reports accessible
- [ ] Screenshots captured on failures
- [ ] Email notifications working

**Next Steps:** Once Jenkins is configured, proceed with running the automation pipeline! 🎉