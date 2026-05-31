import os
import shutil

import allure
import pytest
from playwright.sync_api import Page

from configs.environment import App
from pages.login_page import LoginPage


def pytest_sessionstart(session):
    print("\nIn conftest > pytest_sessionstart")

    # Check if this is a sub-worker in parallel execution (pytest-xdist)
    # Worker names are typically worker1, worker2, etc. Master process has no worker id.
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    if worker_id is not None:
        print(f"Skipping folder cleanup on parallel worker: {worker_id}")
        return
    folders_to_clean = ['reports', 'screenshot', 'logs']
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

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """
    The 'page' argument is built-in from the pytest-playwright plugin.
    It manages browser context setup and teardown automatically.
    """
    login_page_obj = LoginPage(page)
    page.set_default_timeout(App.DEFAULT_TIMEOUT)
    # Navigate using the base URL from your config folder
    page.goto(App.BASE_URL)
    login_page_obj.assert_navigation()
    yield login_page_obj
    # Playwright closes the page automatically after yield finishes
    print("\n[Teardown] Cleaning up application state...")
    try:
        # Example: Clear storage or cookies so tests don't leak state
        page.context.clear_cookies()
    except Exception as e:
        print(f"Cleanup warning: {e}")
