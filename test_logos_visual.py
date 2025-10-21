#!/usr/bin/env python3
"""
Test visual de los logos circulares de Jaime System Care
Muestra todos los tamaños de logos en una ventana para verificación visual
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QFrame)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class LogoTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Visual de Logos - Jaime System Care")
        self.setGeometry(100, 100, 900, 600)

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Título
        title = QLabel("🎨 Test Visual de Logos Circulares")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Obtener directorio base
        base_dir = os.path.dirname(__file__)

        # Definir logos a probar
        logos = [
            ("logo-Jaime-circular-512.png", "Alta Resolución", "512x512px"),
            ("logo-Jaime-circular-256.png", "Resolución Media", "256x256px"),
            ("logo-Jaime-circular-128.png", "Icono Aplicación", "128x128px"),
            ("logo-Jaime-circular-80.png", "UI Principal", "80x80px"),
            ("logo-Jaime-circular-60.png", "UI Secundaria", "60x60px"),
        ]

        # Crear filas de logos
        for filename, description, size_text in logos:
            logo_path = os.path.join(base_dir, filename)

            # Frame contenedor
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                stop:0 #2c3e50, stop:1 #34495e);
                    border-radius: 15px;
                    padding: 15px;
                }
            """)

            row_layout = QHBoxLayout()
            row_layout.setSpacing(20)

            # Imagen del logo
            if os.path.exists(logo_path):
                pixmap = QPixmap(logo_path)
                logo_label = QLabel()
                logo_label.setPixmap(pixmap)
                logo_label.setAlignment(Qt.AlignCenter)
                row_layout.addWidget(logo_label)

                # Información
                info_layout = QVBoxLayout()

                name_label = QLabel(f"📁 {filename}")
                name_label.setFont(QFont("Arial", 12, QFont.Bold))
                name_label.setStyleSheet("color: white;")
                info_layout.addWidget(name_label)

                desc_label = QLabel(f"📋 {description}")
                desc_label.setFont(QFont("Arial", 10))
                desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
                info_layout.addWidget(desc_label)

                size_label = QLabel(f"📐 {size_text}")
                size_label.setFont(QFont("Arial", 10))
                size_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
                info_layout.addWidget(size_label)

                # Tamaño del archivo
                file_size = os.path.getsize(logo_path) / 1024
                file_label = QLabel(f"💾 {file_size:.1f} KB")
                file_label.setFont(QFont("Arial", 10))
                file_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
                info_layout.addWidget(file_label)

                status_label = QLabel("✅ OK")
                status_label.setFont(QFont("Arial", 12, QFont.Bold))
                status_label.setStyleSheet("color: #4CAF50;")
                info_layout.addWidget(status_label)

                row_layout.addLayout(info_layout)
            else:
                error_label = QLabel(f"❌ No encontrado: {filename}")
                error_label.setFont(QFont("Arial", 12))
                error_label.setStyleSheet("color: #F44336;")
                row_layout.addWidget(error_label)

            row_layout.addStretch()
            frame.setLayout(row_layout)
            layout.addWidget(frame)

        layout.addStretch()
        central.setLayout(layout)

        # Estilo general
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #1e3c72, stop:1 #2a5298);
            }
            QLabel {
                color: white;
            }
        """)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = LogoTestWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
