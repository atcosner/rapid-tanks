from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QHBoxLayout

from src.constants.meteorological import MeteorologicalSite
from src.gui.widgets.util.data_entry_rows import NumericDataRow

from src.gui.widgets.util.labels import SubSectionHeader


class MeteorologicalInfoFrame(QFrame):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.site: MeteorologicalSite | None = None

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Meteorological site name
        name_layout = QHBoxLayout()
        layout.addLayout(name_layout)

        self.site_name = QLabel('')
        self.site_name.setStyleSheet("QLabel { font: bold; }")

        name_layout.addWidget(SubSectionHeader('Site:'))
        name_layout.addWidget(self.site_name)
        name_layout.addStretch()

        # Daily Average Ambient Temperature
        self.daat = NumericDataRow(
            'Daily Average Ambient Temperature',
            'degF',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.daat)

        # Annual Average Maximum Temperature
        self.aat_max = NumericDataRow(
            'Annual Average Maximum Temperature',
            'degF',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.aat_max)

        # Annual Average Minimum Temperature
        self.aat_min = NumericDataRow(
            'Annual Average Minimum Temperature',
            'degF',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.aat_min)

        # Average Wind Speed
        self.aws = NumericDataRow(
            'Average Wind Speed',
            'mph',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.aws)

        # Annual Average Solar Insulation Factor
        self.aasif = NumericDataRow(
            'Annual Average Solar Insulation Factor',
            'dimensionless',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=0,
        )
        layout.addWidget(self.aasif)

        # Atmospheric Pressure
        self.ap = NumericDataRow(
            'Atmospheric Pressure',
            'psia',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.ap)

        layout.addStretch()

    @pyqtSlot(MeteorologicalSite)
    def handle_site_selected(self, site: MeteorologicalSite) -> None:
        self.site = site

        # Load values
        self.site_name.setText(f'{site.name}, {site.state}')
        self.daat.set(site.annual_data.average_daily_max_temp)
        self.aat_max.set(site.annual_data.average_daily_max_temp)
        self.aat_min.set(site.annual_data.average_daily_min_temp)
        self.aws.set(site.annual_data.average_wind_speed)
        self.aasif.set(site.annual_data.average_solar_insolation)
        self.ap.set(site.atmospheric_pressure)

    def get_site(self) -> MeteorologicalSite | None:
        return self.site
