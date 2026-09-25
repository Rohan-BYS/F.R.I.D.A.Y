import sys
import os
import sqlite3
import json
import random
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QPen
from PyQt6.QtCore import Qt, QTimer

class FridayOrb(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(300, 300)
        
        # Initial state
        self.state = "idle"
        self.radius = 100
        self.pulse = 0
        self.pulse_dir = 1
        
        # Layout for status text
        layout = QVBoxLayout()
        self.status_label = QLabel("F.R.I.D.A.Y. Idle")
        self.status_label.setStyleSheet("color: cyan; font-family: Consolas; font-size: 14px; background: transparent;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.setLayout(layout)

        # Pulse timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_orb)
        self.timer.start(50)
        
        # State checker (IPC placeholder)
        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.check_state)
        self.state_timer.start(1000)
        
        # State file path
        self.state_file = os.path.join(os.path.dirname(__file__), ".friday_state.json")
        self.write_state("idle", "F.R.I.D.A.Y. Online")

    def write_state(self, status, message):
        with open(self.state_file, "w") as f:
            json.dump({"status": status, "message": message}, f)

    def check_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    self.state = data.get("status", "idle")
                    self.status_label.setText(data.get("message", "F.R.I.D.A.Y. Online"))
            except:
                pass

    def update_orb(self):
        # Calculate pulse
        if self.state == "listening":
            self.pulse += 10 * self.pulse_dir
            if self.pulse > 40: self.pulse_dir = -1
            if self.pulse < -10: self.pulse_dir = 1
        elif self.state == "speaking":
            self.pulse += 15 * self.pulse_dir
            if self.pulse > 60: self.pulse_dir = -1
            if self.pulse < 0: self.pulse_dir = 1
        elif self.state == "thinking":
            self.pulse += 5 * self.pulse_dir
            if self.pulse > 20: self.pulse_dir = -1
            if self.pulse < 0: self.pulse_dir = 1
        else:
            self.pulse += 2 * self.pulse_dir
            if self.pulse > 10: self.pulse_dir = -1
            if self.pulse < 0: self.pulse_dir = 1
            
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = self.width() / 2, self.height() / 2 - 20
        r = self.radius + self.pulse
        
        # Set colors based on state
        if self.state == "listening":
            c1, c2 = QColor(0, 255, 255, 200), QColor(0, 100, 255, 50)
        elif self.state == "thinking":
            c1, c2 = QColor(255, 0, 255, 200), QColor(100, 0, 255, 50)
        elif self.state == "speaking":
            c1, c2 = QColor(0, 255, 100, 200), QColor(0, 150, 50, 50)
        else:
            c1, c2 = QColor(0, 200, 255, 150), QColor(0, 50, 150, 30)

        gradient = QRadialGradient(cx, cy, r)
        gradient.setColorAt(0, c1)
        gradient.setColorAt(1, c2)
        
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(cx - r), int(cy - r), int(r * 2), int(r * 2))

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FridayOrb()
    window.show()
    sys.exit(app.exec())
