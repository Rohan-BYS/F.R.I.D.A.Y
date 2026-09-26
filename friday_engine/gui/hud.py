import sys
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush

from friday_engine.senses.audio_monitor import AudioMonitor

class OrbVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)
        self.volume = 0.0
        self.base_radius = 50

    def set_volume(self, vol):
        # Smooth interpolation
        self.volume = self.volume * 0.7 + vol * 0.3
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        center = QPointF(width / 2, height / 2)

        # Draw outer glowing rings
        ring_count = 3
        for i in range(ring_count):
            radius = self.base_radius + (self.volume * 1.5) + (i * 20 * (self.volume / 20.0 + 1))
            alpha = max(0, 150 - (i * 40) - int(self.volume))
            
            pen = QPen(QColor(0, 200, 255, alpha))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(center, radius, radius)

        # Draw central orb
        core_radius = self.base_radius + (self.volume * 0.5)
        core_color = QColor(0, 255, 255, min(255, 100 + int(self.volume * 2)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(core_color))
        painter.drawEllipse(center, core_radius, core_radius)

class FridayHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        # Make the window frameless and transparent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.init_ui()
        
        # Audio Monitor
        self.audio_monitor = AudioMonitor()
        self.audio_monitor.start()

        # Update Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_visuals)
        self.timer.start(30) # ~30 FPS

        # Dragging variables
        self._drag_pos = None

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Left Panel - Widgets
        widget_panel = QVBoxLayout()
        
        title = QLabel("F.R.I.D.A.Y. HUD")
        title.setStyleSheet("color: #00ffff; font-size: 18px; font-weight: bold; font-family: Courier;")
        widget_panel.addWidget(title)

        self.lbl_status = QLabel("Status: LISTENING")
        self.lbl_status.setStyleSheet("color: #aaffff; font-family: Courier;")
        widget_panel.addWidget(self.lbl_status)

        self.lbl_agent = QLabel("Sub-agent: IDLE")
        self.lbl_agent.setStyleSheet("color: #aaffff; font-family: Courier;")
        widget_panel.addWidget(self.lbl_agent)
        
        widget_panel.addStretch()

        # Right Panel - Visualizer
        self.orb = OrbVisualizer()

        main_layout.addLayout(widget_panel)
        main_layout.addWidget(self.orb)

        # Style the main widget background
        central_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(10, 15, 20, 220);
                border-radius: 15px;
                border: 1px solid rgba(0, 255, 255, 50);
            }
        """)

    def update_visuals(self):
        vol = self.audio_monitor.get_volume()
        self.orb.set_volume(vol)
        if vol > 10:
            self.lbl_status.setText("Status: PROCESSING AUDIO...")
        else:
            self.lbl_status.setText("Status: LISTENING")

    # Draggable Window Logic
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def closeEvent(self, event):
        self.audio_monitor.stop()
        super().closeEvent(event)

def launch_hud():
    app = QApplication(sys.argv)
    window = FridayHUD()
    window.resize(600, 350)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launch_hud()
