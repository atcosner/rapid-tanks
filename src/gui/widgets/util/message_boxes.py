from PyQt5.QtWidgets import QMessageBox, QWidget


def confirm_dirty_cancel(parent: QWidget) -> bool:
    return QMessageBox.warning(
        parent,
        'Unsaved Changes',
        'You have unsaved changes, are you sure you want to cancel editing?',
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.Yes,
    ) == QMessageBox.Yes


def warn_mandatory_fields(parent: QWidget) -> None:
    return QMessageBox.warning(
        parent,
        'Form Error',
        'Please fill out mandatory fields (*) before saving changes',
    )
