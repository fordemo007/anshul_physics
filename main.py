import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
import sys


class FirstPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("page1.ui", self)
        self.lineEdit_2.textChanged.connect(self.update_d_text)
        self.lineEdit_5.textChanged.connect(self.update_d_text)
        self.lineEdit_3.textChanged.connect(self.update_t_text)
        self.lineEdit_6.textChanged.connect(self.update_t_text)
        self.pushButton.clicked.connect(self.solve)

    def update_d_text(self, text):
        self.lineEdit_2.setText(text)
        self.lineEdit_5.setText(text)

    def update_t_text(self, text):
        self.lineEdit_3.setText(text)
        self.lineEdit_6.setText(text)

    def solve(self):
        if self.lineEdit_3.text() != "0":
            try:
                v = f"{float(self.lineEdit_2.text()) / float(self.lineEdit_3.text()):.3f}"
                d = f"{float(self.lineEdit_2.text()):.3f}"
                t = f"{float(self.lineEdit_3.text()):.3f}"
                call_window = SecondPage(v, d, t)
                widget.addWidget(call_window)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"{e}")
        else:
            QMessageBox.critical(self, "Error", "Can't process as t=0")


class SecondPage(QMainWindow):
    def __init__(self, v, d, t):
        super().__init__()
        loadUi("page2.ui", self)
        self.v = v
        self.d = d
        self.t = t
        self.label_9.setText(v)
        self.label_10.setText(d)
        self.label_11.setText(t)
        self.pushButton.clicked.connect(self.call_graph)

    def call_graph(self):
        call_window = ThirdPage(self.v, self.d, self.t)
        widget.addWidget(call_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ThirdPage(QMainWindow):
    def __init__(self, v, d, t):
        super().__init__()
        loadUi("page3.ui", self)
        self.v = float(v)
        self.d = float(d)
        self.t = float(t)
        self.plot_graph()
        self.pushButton.clicked.connect(self.home)

    def home(self):
        call_window = FirstPage()
        widget.addWidget(call_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def plot_graph(self):
        t_vals = np.linspace(0, self.t, 100)
        d_vals = self.v * t_vals

        plt.figure(figsize=(6, 4))
        plt.plot(t_vals, d_vals, label="Displacement vs Time", color="red")
        plt.axhline(0, color="black", linewidth=1)
        plt.axvline(0, color="black", linewidth=1)
        plt.xlabel("Time (s)")
        plt.ylabel("Displacement (m)")
        plt.title("Displacement-Time Graph")
        plt.grid(True)
        plt.legend()
        plt.xlim(0, self.t)
        plt.ylim(0, self.d)
        plt.savefig("displacement_time_graph.png", dpi=140, transparent=True)
        plt.close()

        pixmap = QPixmap("displacement_time_graph.png")
        self.label_3.setPixmap(pixmap)
        self.label_3.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    main_wind = FirstPage()
    widget.addWidget(main_wind)
    widget.setFixedSize(main_wind.size())
    widget.show()
    sys.exit(app.exec())
