from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel

from src.constants.meteorological import MeteorologicalSite
from src.gui.widgets.data_row import DataRow


class MeteorologicalInfoFrame(QFrame):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Daily Average Ambient Temperature
        self.daat = DataRow('Daily Average Ambient Temperature (F)', 'degF')
        layout.addLayout(self.daat)

        # Annual Average Maximum Temperature
        self.aat_max = DataRow('Annual Average Maximum Temperature (F)', 'degF')
        layout.addLayout(self.aat_max)

        # Annual Average Minimum Temperature
        self.aat_min = DataRow('Annual Average Minimum Temperature (F)', 'degF')
        layout.addLayout(self.aat_min)

        # Average Wind Speed
        self.aws = DataRow('Average Wind Speed (mph)', 'mph')
        layout.addLayout(self.aws)

        # Annual Average Solar Insulation Factor
        self.aasif = DataRow('Annual Average Solar Insulation Factor', 'dimensionless')
        layout.addLayout(self.aasif)

        # Atmospheric Pressure
        self.ap = DataRow('Atmospheric Pressure', 'psia')
        layout.addLayout(self.ap)

    @pyqtSlot(MeteorologicalSite)
    def handle_site_selected(self, site: MeteorologicalSite) -> None:
        # Update our line edits with the new data
        self.daat.set_text(site.annual_data.average_daily_max_temp)
        self.aat_max.set_text(site.annual_data.average_daily_max_temp)
        self.aat_min.set_text(site.annual_data.average_daily_min_temp)
        self.aws.set_text(site.annual_data.average_wind_speed)
        self.aasif.set_text(site.annual_data.average_solar_insolation)
        self.ap.set_text(site.atmospheric_pressure)
