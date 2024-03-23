import argparse
import logging
import sys

from PyQt5.QtWidgets import QApplication

from src.gui.main_window import MainWindow
from src.util.logging import configure_root_logger


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true', help='Report debug info to stdout/stderr')
    args = parser.parse_args()

    configure_root_logger(logging.DEBUG if args.verbose else logging.INFO)

    qt_app = QApplication([])

    # from src.gui.modals.mixture_browser import MixtureBrowser
    # test1 = MixtureBrowser(None, False)
    # test1.show()

    tanks_main_window = MainWindow()
    tanks_main_window.show()

    return qt_app.exec()


if __name__ == '__main__':
    sys.exit(main())
