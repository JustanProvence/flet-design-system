
# Responsive Flet Application Example

This directory contains an example of a responsive Flet application.

## How to Run

To run this application, follow these steps:

1.  **Navigate to the application directory:**
    ```bash
    cd responsive_app_example
    ```

2.  **Ensure Flet is installed:**
    If you haven't already, install Flet in your environment. This project's `pyproject.toml` specifies `flet = "0.85.2"`. You can install it using Poetry (from the project root) or pip:
    ```bash
    # From the project root directory (one level up from this directory)
    poetry install

    # Alternatively, using pip if you prefer (ensure it's in your active environment)
    pip install flet
    ```

3.  **Run the application:**
    ```bash
    flet run main_flet.py
    ```

    This command will launch the Flet application in a new window.
