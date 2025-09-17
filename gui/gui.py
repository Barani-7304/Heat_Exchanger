import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QTabWidget, QMainWindow, QMessageBox
)
from PyQt5.QtCore import Qt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.geometry import heat_exchanger_balance, log_mean_temp_difference


class HeatExchangerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heat Exchanger Calculator")
        self.setGeometry(200, 200, 900, 450)

        # --- Tab widget ---
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # --- Add Tab 1: Mass Flow & Temperature ---
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Mass Flow & Temperature")
        self.setup_tab1()

        # --- Add Tab 2: Tube-Side Calculation ---
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Tube Side Geometry")
        self.setup_tab2()

    # ---------------- TAB 1 ----------------
    def setup_tab1(self):
        main_layout = QHBoxLayout()

        # Left input form
        input_layout = QFormLayout()

        self.m_dot_shell = QLineEdit()
        self.T_in_shell = QLineEdit()
        self.T_out_shell = QLineEdit()

        self.m_dot_tube = QLineEdit()
        self.T_in_tube = QLineEdit()
        self.T_out_tube = QLineEdit()

        input_layout.addRow("Mass Flow (Shell) [kg/s]:", self.m_dot_shell)
        input_layout.addRow("Shell Inlet Temp [°C]:", self.T_in_shell)
        input_layout.addRow("Shell Outlet Temp [°C]:", self.T_out_shell)

        input_layout.addRow("Mass Flow (Tube) [kg/s]:", self.m_dot_tube)
        input_layout.addRow("Tube Inlet Temp [°C]:", self.T_in_tube)
        input_layout.addRow("Tube Outlet Temp [°C]:", self.T_out_tube)

        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate_tab1)
        input_layout.addRow(self.calculate_btn)

        self.result_label = QLabel("Results will appear here")
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setStyleSheet("font-family: monospace; font-size: 14px;")

        main_layout.addLayout(input_layout, stretch=2)
        main_layout.addWidget(self.result_label, stretch=3)

        self.tab1.setLayout(main_layout)

    def calculate_tab1(self):
        try:
            m_dot_shell = float(self.m_dot_shell.text()) if self.m_dot_shell.text() else None
            m_dot_tube = float(self.m_dot_tube.text()) if self.m_dot_tube.text() else None
            T_in_shell = float(self.T_in_shell.text()) if self.T_in_shell.text() else None
            T_out_shell = float(self.T_out_shell.text()) if self.T_out_shell.text() else None
            T_in_tube = float(self.T_in_tube.text()) if self.T_in_tube.text() else None
            T_out_tube = float(self.T_out_tube.text()) if self.T_out_tube.text() else None

            cp_shell = 4180  # J/kg.K
            cp_tube = 4180

            result = heat_exchanger_balance(
                m_hot=m_dot_shell, cp_hot=cp_shell,
                Th_in=T_in_shell, Th_out=T_out_shell,
                m_cold=m_dot_tube, cp_cold=cp_tube,
                Tc_in=T_in_tube, Tc_out=T_out_tube
            )

            LMTD = log_mean_temp_difference(
                result["Th_in"], result["Th_out"],
                result["Tc_in"], result["Tc_out"]
            )

            result_text = f"""
The inputs are:

Mass flow rate in shell side:  {m_dot_shell if m_dot_shell is not None else '-'}
Inlet Temperature in shell side:  {result['Th_in']:.2f} °C
Outlet Temperature in shell side: {result['Th_out']:.2f} °C

Mass flow rate in tube side:   {m_dot_tube if m_dot_tube is not None else '-'}
Inlet Temperature in tube side:   {result['Tc_in']:.2f} °C
Outlet Temperature in tube side:  {result['Tc_out']:.2f} °C

Heat duty: {result['q']:.2f} W
Mean temperature: {LMTD:.2f} °C
"""
            self.result_label.setText(result_text)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Calculation failed:\n{e}")

    # ---------------- TAB 2 ----------------
    def setup_tab2(self):
        main_layout = QHBoxLayout()

        # Left input form
        input_layout = QFormLayout()
        self.num_tubes = QLineEdit()
        self.d_inner = QLineEdit()
        self.d_outer = QLineEdit()

        input_layout.addRow("Number of Tubes:", self.num_tubes)
        input_layout.addRow("Tube Inner Diameter [m]:", self.d_inner)
        input_layout.addRow("Tube Outer Diameter [m]:", self.d_outer)

        self.calculate_tube_btn = QPushButton("Calculate Tube Geometry")
        self.calculate_tube_btn.clicked.connect(self.calculate_tab2)
        input_layout.addRow(self.calculate_tube_btn)

        # Right side: results
        self.result_label_tab2 = QLabel("Tube-side results will appear here")
        self.result_label_tab2.setAlignment(Qt.AlignTop)
        self.result_label_tab2.setStyleSheet("font-family: monospace; font-size: 14px;")

        main_layout.addLayout(input_layout, stretch=2)
        main_layout.addWidget(self.result_label_tab2, stretch=3)

        self.tab2.setLayout(main_layout)

    def calculate_tab2(self):
        try:
            n_tubes = int(self.num_tubes.text()) if self.num_tubes.text() else None
            d_inner = float(self.d_inner.text()) if self.d_inner.text() else None
            d_outer = float(self.d_outer.text()) if self.d_outer.text() else None

            result_text = f"""
Tube-side geometry inputs:

Number of tubes: {n_tubes if n_tubes is not None else '-'}
Inner diameter:  {d_inner if d_inner is not None else '-'} m
Outer diameter:  {d_outer if d_outer is not None else '-'} m
"""
            self.result_label_tab2.setText(result_text)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Tube-side calculation failed:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatExchangerApp()
    window.show()
    sys.exit(app.exec_())
