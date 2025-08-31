# Main entry point for the Unified Game Automation Tool
# This will be the main file that starts the tabbed interface

import sys
import os
import logging
import traceback

from ui.main_window import MainWindow


def setup_logging():
    """Redirect stdout/stderr and setup logging to file."""
    log_path = os.path.join(os.path.dirname(__file__), "execution.log")

    # Configure logging
    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    # Redirect stdout and stderr to the log file too
    sys.stdout = open(log_path, "a", encoding="utf-8")
    sys.stderr = sys.stdout

    logging.info("==== Application started ====")


def main():
    """Main entry point for the unified game automation tool"""
    print("Starting Unified Game Automation Tool...")
    logging.info("Launching MainWindow...")

    # Create and run the main window
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    setup_logging()
    try:
        main()
    except Exception as e:
        # Log unhandled exceptions
        logging.error("Unhandled exception occurred", exc_info=True)
        # Also print traceback for debugging
        traceback.print_exc()
        # Keep console open if running manually
        input("Press Enter to exit...")
