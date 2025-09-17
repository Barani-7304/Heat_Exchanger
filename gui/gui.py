import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout, QTabWidget, QTextEdit, QMainWindow
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.geometry import heat_exchanger_balance, log_mean_temp_difference

class HeatExchangerTab(QWidget):
    """First tab: Heat exchanger energy balance inputs & results."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Left side (inputs)
        input_layout = QGridLayout()
        self.m_hot_input = QLineEdit()
        self.Th_in_input = QLineEdit()
        self.Th_out_input = QLineEdit()
        self.m_cold_input = QLineEdit()
        self.Tc_in_input = QLineEdit()
        self.Tc_out_input = QLineEdit()
        self.cp_hot_input = QLineEdit()
        self.cp_cold_input = QLineEdit()

        input_layout.addWidget(QLabel("Mass flow rate (Hot side):"), 0, 0)
        input_layout.addWidget(self.m_hot_input, 0, 1)
        input_layout.addWidget(QLabel("Hot side Cp:"), 1, 0)
        input_layout.addWidget(self.cp_hot_input, 1, 1)
        input_layout.addWidget(QLabel("Hot Inlet Temp:"), 2, 0)
        input_layout.addWidget(self.Th_in_input, 2, 1)
        input_layout.addWidget(QLabel("Hot Outlet Temp:"), 3, 0)
        input_layout.addWidget(self.Th_out_input, 3, 1)

        input_layout.addWidget(QLabel("Mass flow rate (Cold side):"), 4, 0)
        input_layout.addWidget(self.m_cold_input, 4, 1)
        input_layout.addWidget(QLabel("Cold side Cp:"), 5, 0)
        input_layout.addWidget(self.cp_cold_input, 5, 1)
        input_layout.addWidget(QLabel("Cold Inlet Temp:"), 6, 0)
        input_layout.addWidget(self.Tc_in_input, 6, 1)
        input_layout.addWidget(QLabel("Cold Outlet Temp:"), 7, 0)
        input_layout.addWidget(self.Tc_out_input, 7, 1)

        calc_button = QPushButton("Calculate")
        calc_button.clicked.connect(self.calculate)
        input_layout.addWidget(calc_button, 8, 0, 1, 2)

        # Right side (results)
        self.results_box = QTextEdit()
        self.results_box.setReadOnly(True)

        layout.addLayout(input_layout, 1)
        layout.addWidget(self.results_box, 2)

        self.setLayout(layout)

    def calculate(self):
        try:
            m_hot = float(self.m_hot_input.text())
            cp_hot = float(self.cp_hot_input.text())
            Th_in = float(self.Th_in_input.text()) if self.Th_in_input.text() else None
            Th_out = float(self.Th_out_input.text()) if self.Th_out_input.text() else None

            m_cold = float(self.m_cold_input.text())
            cp_cold = float(self.cp_cold_input.text())
            Tc_in = float(self.Tc_in_input.text()) if self.Tc_in_input.text() else None
            Tc_out = float(self.Tc_out_input.text()) if self.Tc_out_input.text() else None

            result = heat_exchanger_balance(m_hot, cp_hot, Th_in, Th_out,
                                            m_cold, cp_cold, Tc_in, Tc_out)

            LMTD = log_mean_temp_difference(result["Th_in"], result["Th_out"],
                                            result["Tc_in"], result["Tc_out"])

            self.results_box.setPlainText(
                f"Inputs:\n"
                f"Mass flow rate (Hot): {m_hot}\n"
                f"Mass flow rate (Cold): {m_cold}\n"
                f"Hot Inlet: {result['Th_in']}\n"
                f"Hot Outlet: {result['Th_out']}\n"
                f"Cold Inlet: {result['Tc_in']}\n"
                f"Cold Outlet: {result['Tc_out']}\n\n"
                f"Results:\n"
                f"Heat Duty (Q): {result['q']}\n"
                f"LMTD: {LMTD}"
            )

        except Exception as e:
            self.results_box.setPlainText(f"Error: {e}")


class TubeSideTab(QWidget):
    """Second tab: Tube side properties calculation inputs & results."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Left side (inputs)
        input_layout = QGridLayout()
        self.d_inner_input = QLineEdit()
        self.d_outer_input = QLineEdit()
        self.k_input = QLineEdit()
        self.rho_input = QLineEdit()
        self.nu_input = QLineEdit()

        input_layout.addWidget(QLabel("Tube Inner Diameter (m):"), 0, 0)
        input_layout.addWidget(self.d_inner_input, 0, 1)
        input_layout.addWidget(QLabel("Tube Outer Diameter (m):"), 1, 0)
        input_layout.addWidget(self.d_outer_input, 1, 1)
        input_layout.addWidget(QLabel("Thermal Conductivity (W/m·K):"), 2, 0)
        input_layout.addWidget(self.k_input, 2, 1)
        input_layout.addWidget(QLabel("Fluid Density (kg/m³):"), 3, 0)
        input_layout.addWidget(self.rho_input, 3, 1)
        input_layout.addWidget(QLabel("Kinematic Viscosity (m²/s):"), 4, 0)
        input_layout.addWidget(self.nu_input, 4, 1)

        calc_button = QPushButton("Calculate Tube Side")
        calc_button.clicked.connect(self.calculate)
        input_layout.addWidget(calc_button, 5, 0, 1, 2)

        # Right side (results)
        self.results_box = QTextEdit()
        self.results_box.setReadOnly(True)

        layout.addLayout(input_layout, 1)
        layout.addWidget(self.results_box, 2)
        self.setLayout(layout)

    def calculate(self):
        try:
            d_inner = float(self.d_inner_input.text())
            d_outer = float(self.d_outer_input.text())
            k = float(self.k_input.text())
            rho = float(self.rho_input.text())
            nu = float(self.nu_input.text())

            # For now, just display the inputs (calculation logic will be in tube.py)
            self.results_box.setPlainText(
                f"Tube Inner Diameter: {d_inner}\n"
                f"Tube Outer Diameter: {d_outer}\n"
                f"Thermal Conductivity: {k}\n"
                f"Fluid Density: {rho}\n"
                f"Kinematic Viscosity: {nu}\n\n"
                f"Results will be shown here after we connect tube.py calculations."
            )

        except Exception as e:
            self.results_box.setPlainText(f"Error: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heat Exchanger Calculator")
        self.setGeometry(100, 100, 800, 600)

        tabs = QTabWidget()
        tabs.addTab(HeatExchangerTab(), "Energy Balance")
        tabs.addTab(TubeSideTab(), "Tube Side Calculation")

        self.setCentralWidget(tabs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
