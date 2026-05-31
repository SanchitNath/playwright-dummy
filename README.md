# Playwright Python Automation Framework

A scalable, production-ready web automation framework built from scratch using Python, Pytest, and Playwright. This project implements the Page Object Model (POM) design pattern to ensure clean, maintainable, and readable test specifications.

## 🚀 Key Features

*   **Page Object Model (POM):** Clean separation of test logic and page-specific elements/actions.
*   **Modern Configuration:** Uses a unified `pyproject.toml` file to manage metadata, dependencies, and execution flags.
*   **Robust Assertions:** Utilizes Playwright's web-first `expect` library for auto-retrying assertions.
*   **Automated Reporting:** Generates a visually rich HTML test report automatically after every run.

---

## 📂 Project Structure

```text
playwright-python-framework/
├── configs/
│   └── environment.py 
├── logs/
├── pages/
│   └── login_page.py      # Page classes containing locators and actions
├── reports/
│   └── report.html
├── screenshot/
├── tests/
│   └── tests-test-login-py-test-invalid-login-chromium
│       └── trace.zip
├── tests/
│   └── test_login.py      # Test execution suites and specifications
├── .gitignore 
├── conftest.py        # Global setup/teardown fixtures
├── pyproject.toml         # Unified project metadata and configurations
└── README.md              # Project documentation
```

---

## 🛠️ Installation & Setup

Ensure you have [Python 3.8+](https://python.org) installed on your machine. Follow these steps to set up the framework locally:

### 0. Install npm and pnp
```bash
  brew install node
  brew install pnpm
  node --version
  pnpm --version
```

### 1. Navigate to the Project
```bash
  mkdir playwright-python-framework
  cd playwright-python-framework
  pnpm create playwright
```

### 2. Install Project Dependencies After Creating Virtual Envt
Use the explicit `python3 -m pip` command to install the required libraries listed in `pyproject.toml`:
```bash
  python3 -m venv venv_test
  source venv_test/bin/activate
  python3 -m pip install .
  or
  pip install -e .  
  It creates 'playwright_pytest_framework.egg-info' folder
```

### 3. Install Playwright Browser Binaries
Download and initialize the underlying system browsers (Chromium, Firefox, and WebKit) needed for automation execution:
```bash
  python3 -m playwright install
```

---

## Running the Tests

The framework is configured to run tests in **headed** mode (visible browser window) by default and output results 
directly to your terminal.

### Run All Tests
Execute the entire test suite across your `tests/` directory:
```bash
  pytest
```

### Run Specific Test Groups via Markers
Execute only the smoke verification test suite:
```bash
  pytest -m smoke
```

Execute via test name:
```bash
  pytest -k "test_invalid_login"
```

Execute via file name:
```bash
  pytest tests/test_login.py
```

# Rerun failed tests
Rerun failed tests again after completion of current state:
```bash
  pytest
  pytest --lf
```

To run in headed mode:
```bash
  pytest --headed
```

### Debug mode
To debug using playwright inspector:
```bash
  PWDEBUG=1 pytest
  PWDEBUG=1 pytest -m smoke
  PWDEBUG=1 pytest -k "test_invalid_login"
```

### Recording a trace
Trace can be recorded by using:
```bash
  pytest --tracing on
```
It creates test-results folder containing folder of each unique test.
Those folder contains trace.zip

To view the saved traces:
```bash
  playwright show-trace test-results/*/trace.zip
```
Each step has Action, Before, After.
It has Filter actions and a terminal containing - Locator, Call, Log, Errors, Console, Network, Source, Attachments.

Once opened you can click on each action or use the timeline to see the state of the page before and after each action

---

### View packages
To view the installed packages:
```bash
  pip list | grep -E "pytest|playwright"
```

---

## 📊 Test Reports

After executing any test run, a standalone file named `report.html` will be generated automatically in the reports 
folder of the project.

To view the execution results, visual details, and failure logs, simply open the `report.html` file in any 
modern web browser (Chrome, Safari, Firefox).
Or just run 
``` bash
  allure serve reports
```
