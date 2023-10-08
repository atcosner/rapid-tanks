from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem


class MaterialList(QTreeWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # We only need a column for name
        self.setColumnCount(1)
        self.setHeaderLabels(['Name'])

        self.load()

    def load(self) -> None:
        # Remove all existing tree entries
        self.clear()

        # Load all available materials and populate ourselves
        # TODO
        custom_materials = QTreeWidgetItem()
        custom_materials.setText(0, 'Custom')
        self.addTopLevelItem(custom_materials)

        builtin_materials = QTreeWidgetItem()
        builtin_materials.setText(0, 'Builtin')
        self._load_builtin_materials(builtin_materials)
        self.addTopLevelItem(builtin_materials)

    def _load_builtin_materials(self, parent: QTreeWidgetItem) -> None:
        # TODO: Load from the local DB?
        for material in ['Test1', 'Test2', 'Test3']:
            test = QTreeWidgetItem(parent)
            test.setText(0, material)
            parent.addChild(test)
