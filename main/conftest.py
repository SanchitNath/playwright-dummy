import os
import shutil
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from configs.environment import App
from pages.login_page import LoginPage
from utils.logger import LogGen


def pytest_sessionstart(session):
    print("\nIn conftest > pytest_sessionstart")

    # Check if this is a sub-worker in parallel execution (pytest-xdist)
    # Worker names are typically worker1, worker2, etc. Master process has no worker id.
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    if worker_id is not None:
        print(f"Skipping folder cleanup on parallel worker: {worker_id}")
        return
    folders_to_clean = ['logs', 'reports', 'screenshots', 'test-results']
    for folder in folders_to_clean:
        folder_path = os.path.join(os.getcwd(), folder)
        if os.path.exists(folder_path):
            try:
                # shutil.rmtree deletes the folder and all its contents
                shutil.rmtree(folder_path)
                print(f"Deleted: {folder}")
            except Exception as e:
                print(f"Error deleting {folder}: {e}")
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created fresh: {folder}")
    print("Cleaning up python bytecode cache...")
    try:
        # rglob finds all instances of "__pycache__" anywhere in your project root
        for cache_dir in Path(os.getcwd()).rglob("__pycache__"):
            shutil.rmtree(cache_dir)
            print(f"Deleted cache: {cache_dir.relative_to(os.getcwd())}")
    except Exception as e:
        print(f"Error during __pycache__ cleanup: {e}")

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Handles native shell maximizing flags for Windows and Linux runners."""
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"]
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, browser_name):
    """
    Removes Playwright's default 1280x720 window restrictions.
    Forces the webpage canvas to fluidly fill 100% of the screen on macOS, Windows, and Linux.
    """
    if "chromium" in browser_name.lower():
        return {
        **browser_context_args,
        "viewport": None,        # Bypasses the fixed 1280x720 layout ceiling
        "no_viewport": True      # Instructs the page to stretch to the actual browser size
    }
    return {
            **browser_context_args,
            "viewport": {"width": 1920, "height": 1080},
            "no_viewport": False # Must be False to respect the dimensions
        }

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This executes your test and catches the final result status
    outcome = yield
    report = outcome.get_result()
    # We only attach video or trace logs if the test block actually failed/finished
    if report.when == "call" and report.failed:
        # Access the built-in playwright page instance from your test fixtures
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            # Attach a direct screenshot to Allure dashboard
            allure.attach(
                page.screenshot(full_page=True),
                name="Failure-Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

@pytest.fixture(scope="class", autouse=True)
def setup_logger(request):
    test_file_full_path = str(request.node.fspath)
    print(test_file_full_path)
    print(os.path.basename(test_file_full_path))
    file_name = os.path.splitext(os.path.basename(test_file_full_path))[0]
    print(f"File name is {file_name}")
    # Create the logger using your existing LogGen
    logger = LogGen.loggen()
    # Attach the logger to the class instance (self)
    if request.cls is not None:
        request.cls.logger = logger
    yield logger

@pytest.fixture(scope="function")
def login_page(request, page: Page) -> LoginPage:
    """
    The 'page' argument is built-in from the pytest-playwright plugin.
    It manages browser context setup and teardown automatically.
    """
    test_instance = request.instance
    login_page_obj = LoginPage(test_instance, page)
    page.set_default_timeout(App.DEFAULT_TIMEOUT)
    # Navigate using the base URL from your config folder
    page.goto(App.BASE_URL)
    login_page_obj.assert_navigation()
    yield login_page_obj
    # Playwright closes the page automatically after yield finishes
    print("\n[Teardown] Cleaning up application state...")
    try:
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)
        # Extract the safe test name (removes invalid filename characters)
        test_name = request.node.name.replace("[", "_").replace("]", "")
        screenshot_path = screenshot_dir / f"{test_name}.png"
        # Capture the screenshot
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"[Teardown] Screenshot saved successfully at: {screenshot_path}")
        # Attach to allure
        allure.attach(
            body=page.screenshot(full_page=True),
            name=f"Teardown - {test_name}",
            attachment_type=allure.attachment_type.PNG
        )
        print(f"[Teardown] Screenshot attached to Allure for: {test_name}")
        # Example: Clear storage or cookies so tests don't leak state
        page.context.clear_cookies()
    except Exception as e:
        print(f"Cleanup warning: {e}")
