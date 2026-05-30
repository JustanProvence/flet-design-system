"""
Playwright-based integration and rendering tests for Flet applications.

Verifies that both the Design System documentation app and the responsive_app_example
can start, run, and successfully render in a headless browser environment,
while ensuring that the Python backend does not crash and remains healthy.
"""

import subprocess
import time
import socket
import pytest
from playwright.sync_api import sync_playwright

def wait_for_port(port: int, timeout: float = 15.0):
    """Wait for a port to start accepting TCP connections."""
    start_time = time.time()
    while True:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1.0):
                return True
        except (ConnectionRefusedError, socket.timeout):
            if time.time() - start_time > timeout:
                raise RuntimeError(f"Timeout waiting for port {port} to be ready")
            time.sleep(0.5)

@pytest.fixture(scope="function")
def design_system_app():
    # Start the design system documentation app on port 8550
    # Use DEVNULL for stdout and stderr to prevent OS pipe buffer block deadlock
    proc = subprocess.Popen(
        ["poetry", "run", "python3", "src/design_system/main.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_for_port(8550)
        yield "http://localhost:8550", proc
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3.0)
        except subprocess.TimeoutExpired:
            proc.kill()

@pytest.fixture(scope="function")
def responsive_app():
    # Start the responsive application on port 8551
    # Use DEVNULL for stdout and stderr to prevent OS pipe buffer block deadlock
    proc = subprocess.Popen(
        ["poetry", "run", "python3", "responsive_app_example/main_flet.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_for_port(8551)
        yield "http://localhost:8551", proc
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3.0)
        except subprocess.TimeoutExpired:
            proc.kill()

def test_design_system_renders(design_system_app):
    url, proc = design_system_app
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            
            # Listen to browser console to detect any unhandled exceptions
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            
            page.goto(url)
            
            # Wait for Flet to load and set the correct document title
            page.wait_for_function("document.title === 'Flet Token-Driven Design System'", timeout=15000)
            assert "Flet Token-Driven Design System" in page.title()
            
            # Verify that the Flutter canvas or glass pane is loaded to confirm UI rendering
            page.wait_for_selector("flt-glass-pane, flutter-view, canvas", timeout=15000)
            
            # Allow a moment for session handshake, then assert python backend is still running successfully
            time.sleep(2.0)
            assert proc.poll() is None, "Backend process crashed!"
            
            # Ensure no websocket or connection errors in browser console
            for error in console_errors:
                assert "failed" not in error.lower() and "exception" not in error.lower()
        finally:
            browser.close()

def test_responsive_app_renders(responsive_app):
    url, proc = responsive_app
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            
            # Listen to browser console to detect any unhandled exceptions
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            
            page.goto(url)
            
            # Wait for Flet to load and set the correct document title
            page.wait_for_function("document.title === 'Responsive Flet App with Design System'", timeout=15000)
            assert "Responsive Flet App with Design System" in page.title()
            
            # Verify that the Flutter canvas or glass pane is loaded to confirm UI rendering
            page.wait_for_selector("flt-glass-pane, flutter-view, canvas", timeout=15000)
            
            # Allow a moment for session handshake, then assert python backend is still running successfully
            time.sleep(2.0)
            assert proc.poll() is None, "Backend process crashed!"
            
            # Ensure no websocket or connection errors in browser console
            for error in console_errors:
                assert "failed" not in error.lower() and "exception" not in error.lower()
        finally:
            browser.close()
