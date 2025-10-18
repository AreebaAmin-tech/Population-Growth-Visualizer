from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QComboBox, QSlider, QWidget
)
from PyQt5.QtCore import Qt

class PopulationGrowthApp(QMainWindow):
    def __init__(self, data_processor, visualizer):
        super().__init__()
        self.data_processor = data_processor
        self.visualizer = visualizer
        self.data = None

        self.setWindowTitle("Population Growth Visualizer")
        self.setGeometry(100, 100, 600, 400)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Heading
        self.heading_label = QLabel("POPULATION GROWTH VISUALIZER")
        self.heading_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.layout.addWidget(self.heading_label)

        # Country selection
        self.country_label = QLabel("Select Country:")
        self.layout.addWidget(self.country_label)
        self.country_dropdown = QComboBox()
        self.layout.addWidget(self.country_dropdown)

        # Year selection
        self.year_label = QLabel("Select Year:")
        self.layout.addWidget(self.year_label)
        self.year_dropdown = QComboBox()
        self.layout.addWidget(self.year_dropdown)

        # Start year slider
        self.start_year_slider = QSlider(Qt.Horizontal)
        self.start_year_slider.setRange(2000, 2023)
        self.start_year_slider.setValue(2000)
        self.start_year_slider.setTickPosition(QSlider.TicksBelow)
        self.start_year_slider.setTickInterval(1)
        self.layout.addWidget(QLabel("Start Year:"))
        self.layout.addWidget(self.start_year_slider)

        # End year slider
        self.end_year_slider = QSlider(Qt.Horizontal)
        self.end_year_slider.setRange(2000, 2023)
        self.end_year_slider.setValue(2023)
        self.end_year_slider.setTickPosition(QSlider.TicksBelow)
        self.end_year_slider.setTickInterval(1)
        self.layout.addWidget(QLabel("End Year:"))
        self.layout.addWidget(self.end_year_slider)

        # Buttons
        self.check_population_button = QPushButton("Check Population")
        self.check_population_button.clicked.connect(self.check_population)
        self.layout.addWidget(self.check_population_button)

        self.generate_chart_button = QPushButton("Generate Chart")
        self.generate_chart_button.clicked.connect(self.generate_charts)
        self.layout.addWidget(self.generate_chart_button)

        # Output label
        self.output_label = QLabel("")
        self.layout.addWidget(self.output_label)

        # Load data automatically
        self.load_data_backend()

    def load_data_backend(self):
        self.data = self.data_processor.load_data()
        if self.data is not None:
            countries = self.data['country'].unique()
            self.country_dropdown.addItems(countries)

            years = [str(year) for year in range(2000, 2024)]
            self.year_dropdown.addItems(years)
        else:
            self.output_label.setText("Failed to load data. Please check the backend.")

    def check_population(self):
        country = self.country_dropdown.currentText()
        year = self.year_dropdown.currentText()
        column_name = f"{year} population"

        if self.data is not None and column_name in self.data.columns:
            population = self.data.loc[self.data['country'] == country, column_name].values
            if population:
                self.output_label.setText(f"Population of {country} in {year}: {int(population[0]):,}")
            else:
                self.output_label.setText(f"No data available for {country} in {year}.")
        else:
            self.output_label.setText("No data available. Please check the backend.")

    def generate_charts(self):
        country = self.country_dropdown.currentText()
        start_year = self.start_year_slider.value()
        end_year = self.end_year_slider.value()

        # Filter the data for selected country and years
        filtered_data = self.data_processor.filter_data(self.data, country, start_year, end_year)

        if filtered_data is not None and not filtered_data.empty:
            filtered_data = self.data_processor.calculate_growth_rate(filtered_data)
            self.visualizer.plot_population_trend(filtered_data, country)
            self.visualizer.plot_growth_rate(filtered_data, country)
        else:
            self.output_label.setText(f"Error: No data for {country} in the selected year range.")
