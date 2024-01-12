import logging
import sys

from PyQt5.QtWidgets import QApplication

from src.gui.main_window import MainWindow


def main() -> int:
    qt_app = QApplication([])

    tanks_main_window = MainWindow()
    tanks_main_window.show()

    return qt_app.exec()


if __name__ == '__main__':
    logging.basicConfig()
    sys.exit(main())
