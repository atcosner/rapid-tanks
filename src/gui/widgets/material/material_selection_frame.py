from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QTabWidget, QHBoxLayout

from src.gui.widgets.material.petrochemical_info_frame import PetrochemicalInfoFrame
from src.gui.widgets.material.petrochemical_list import PetrochemicalList
from src.gui.widgets.material.petroleum_liquid_info_frame import PetroleumLiquidInfoFrame
from src.gui.widgets.material.petroleum_liquid_list import PetroleumLiquidList
from src.gui.widgets.util.search_bar import SearchBar


class MaterialSelectionFrame(QFrame):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.material_tabs = QTabWidget(self)
        self.search_bar = SearchBar(self)
        self.petrochemical_list = PetrochemicalList(self)
        self.petrochemical_info = PetrochemicalInfoFrame(self)
        self.petroleum_liquid_list = PetroleumLiquidList(self)
        self.petroleum_liquid_info = PetroleumLiquidInfoFrame(self)

        self.petrochemical_list.materialSelected.connect(self.petrochemical_info.handle_material_selected)
        self.petroleum_liquid_list.materialSelected.connect(self.petroleum_liquid_info.handle_material_selected)

        self.search_bar.textChanged.connect(self.petrochemical_list.handle_search)
        self.search_bar.textChanged.connect(self.petroleum_liquid_list.handle_search)

        self.material_tabs.currentChanged.connect(self.handle_tab_change)

        # Set up the tab widget for each type of material
        self.material_tabs.addTab(self.petrochemical_list, 'Petrochemical')
        self.material_tabs.addTab(self.petroleum_liquid_list, 'Petroleum Liquid')

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.petroleum_liquid_list.hide()

        layout = QHBoxLayout()
        self.setLayout(layout)

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.search_bar)
        list_layout.addWidget(self.material_tabs)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.petrochemical_info)
        info_layout.addWidget(self.petroleum_liquid_info)

        layout.addLayout(list_layout)
        layout.addLayout(info_layout)

    @pyqtSlot(int)
    def handle_tab_change(self, index: int) -> None:
        if index == 0:
            self.petrochemical_info.show()
            self.petroleum_liquid_info.hide()
        else:
            self.petrochemical_info.hide()
            self.petroleum_liquid_info.show()
