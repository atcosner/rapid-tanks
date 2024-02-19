import sys

from PyQt5.QtWidgets import QApplication

from src.gui.main_window import MainWindow
from src.util.logging import configure_root_logger


def main() -> int:
    qt_app = QApplication([])

    # from src.gui.modals.mixture_browser import MixtureBrowser
    # browser = MixtureBrowser(None, select_mode=False)
    # browser.show()

    tanks_main_window = MainWindow()
    tanks_main_window.show()

    return qt_app.exec()


if __name__ == '__main__':
    configure_root_logger()
    sys.exit(main())
