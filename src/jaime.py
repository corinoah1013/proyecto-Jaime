#!/usr/bin/env python3
"""
Jaime System Care - Mantenimiento y optimización para Linux
Versión 1.3.0
"""

import sys
import subprocess
import platform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QFrame, QScrollArea, QCheckBox, QTextEdit, QProgressBar,
                             QMessageBox, QGroupBox, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
import psutil
import os

# Importar sistema de traducciones
from translations import TranslationManager

# Instancia global del gestor de traducciones
t = TranslationManager()

# Estilos globales con glassmorphism
GLOBAL_STYLES = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #1e3c72, stop:1 #2a5298);
    }

    QWidget {
        color: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    QPushButton {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
        padding: 12px 24px;
        font-size: 13px;
        font-weight: 500;
    }

    QPushButton:hover {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    QPushButton:pressed {
        background: rgba(255, 255, 255, 0.15);
    }

    QGroupBox {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-top: 15px;
        padding: 20px;
        font-weight: bold;
        font-size: 14px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 15px;
        padding: 0 5px;
    }

    QCheckBox {
        color: white;
        spacing: 8px;
        padding: 5px;
    }

    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border-radius: 6px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.1);
    }

    QCheckBox::indicator:checked {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #4CAF50, stop:1 #45a049);
        border: 2px solid #4CAF50;
    }

    QTextEdit {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        padding: 10px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 12px;
    }

    QProgressBar {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        height: 20px;
        text-align: center;
        color: white;
    }

    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #4CAF50, stop:1 #45a049);
        border-radius: 9px;
    }

    QLabel {
        color: white;
    }
"""

class SystemInfo:
    """Clase para obtener información del sistema con caché"""
    _cache = {}

    @classmethod
    def get_cpu(cls):
        if 'cpu' not in cls._cache:
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line:
                            cls._cache['cpu'] = line.split(':')[1].strip()
                            break
                    else:
                        cls._cache['cpu'] = platform.processor() or "CPU Desconocida"
            except (IOError, OSError, Exception):
                cls._cache['cpu'] = platform.processor() or "CPU Desconocida"
        return cls._cache['cpu']

    @classmethod
    def get_ram(cls):
        if 'ram' not in cls._cache:
            ram = psutil.virtual_memory()
            total_gb = ram.total / (1024**3)
            cls._cache['ram'] = f"{total_gb:.1f} GB"
        return cls._cache['ram']

    @classmethod
    def get_gpu(cls):
        if 'gpu' not in cls._cache:
            try:
                result = subprocess.run(['lspci'], capture_output=True, text=True, timeout=5)
                for line in result.stdout.split('\n'):
                    if 'VGA' in line or '3D' in line or 'Display' in line:
                        gpu_info = line.split(':')[-1].strip()
                        cls._cache['gpu'] = gpu_info
                        break
                else:
                    cls._cache['gpu'] = "No detectada"
            except (subprocess.SubprocessError, subprocess.TimeoutExpired, Exception):
                cls._cache['gpu'] = "No detectada"
        return cls._cache['gpu']

    @classmethod
    def get_os(cls):
        if 'os' not in cls._cache:
            try:
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME'):
                            cls._cache['os'] = line.split('=')[1].strip().strip('"')
                            break
                    else:
                        cls._cache['os'] = platform.system() + " " + platform.release()
            except (IOError, OSError, Exception):
                cls._cache['os'] = platform.system() + " " + platform.release()
        return cls._cache['os']


class WorkerThread(QThread):
    """Thread para ejecutar tareas de limpieza sin bloquear la UI"""
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, task_type, tasks):
        super().__init__()
        self.task_type = task_type
        self.tasks = tasks

    def run(self):
        results = []

        for task in self.tasks:
            self.progress.emit(f"Ejecutando: {task['name']}")

            try:
                if task['type'] == 'command':
                    result = subprocess.run(task['command'], shell=True, check=False,
                                 capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        results.append(f"✓ {task['name']}")
                    else:
                        results.append(f"⚠ {task['name']} (con advertencias)")
                elif task['type'] == 'remove_cache':
                    path = os.path.expanduser(task['path'])
                    if os.path.exists(path):
                        # Usar subprocess para eliminar de forma más segura
                        result = subprocess.run(['rm', '-rf', path],
                                              capture_output=True, text=True, timeout=30)
                        if result.returncode == 0:
                            results.append(f"✓ {task['name']} eliminado")
                        else:
                            results.append(f"⚠ {task['name']} (error al eliminar)")
                    else:
                        results.append(f"○ {task['name']} no existe")
            except subprocess.TimeoutExpired:
                results.append(f"⏱ {task['name']}: operación tardó mucho tiempo")
            except Exception as e:
                results.append(f"✗ {task['name']}: {str(e)}")

        self.finished.emit('\n'.join(results))


class UpdateWorkerThread(QThread):
    """Thread específico para actualizaciones del sistema"""
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, action):
        super().__init__()
        self.action = action

    def run(self):
        try:
            if self.action == 'check':
                self.progress.emit("Actualizando lista de paquetes...")
                result = subprocess.run(['pkexec', 'apt', 'update'],
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    result2 = subprocess.run(['apt', 'list', '--upgradable'],
                                           capture_output=True, text=True)
                    self.finished.emit(result2.stdout if result2.stdout else "No hay actualizaciones disponibles")
                else:
                    self.finished.emit(f"Error al actualizar: {result.stderr}")

            elif self.action == 'install':
                self.progress.emit("Instalando actualizaciones...")
                result = subprocess.run(['pkexec', 'apt', 'upgrade', '-y'],
                                      capture_output=True, text=True, timeout=600)
                if result.returncode == 0:
                    self.finished.emit("✅ Actualizaciones instaladas correctamente")
                else:
                    self.finished.emit(f"Error: {result.stderr}")

        except subprocess.TimeoutExpired:
            self.finished.emit("⚠️ La operación tardó demasiado tiempo")
        except Exception as e:
            self.finished.emit(f"Error: {str(e)}")


def add_shadow(widget):
    """Añade sombra suave a un widget"""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(0, 0, 0, 80))
    widget.setGraphicsEffect(shadow)


class HealthCheckPanel(QWidget):
    """Panel de Health Check"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel(t.get('health_title'))
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(self.title)

        # Opciones de chequeo
        self.options_group = QGroupBox(t.get('health_select'))
        options_layout = QVBoxLayout()
        options_layout.setSpacing(12)

        self.check_disk = QCheckBox(t.get('health_disk'))
        self.check_disk.setChecked(True)
        self.check_memory = QCheckBox(t.get('health_memory'))
        self.check_memory.setChecked(True)
        self.check_cpu = QCheckBox(t.get('health_cpu'))
        self.check_cpu.setChecked(True)
        self.check_services = QCheckBox(t.get('health_services'))
        self.check_services.setChecked(True)
        self.check_errors = QCheckBox(t.get('health_errors'))
        self.check_errors.setChecked(True)

        for checkbox in [self.check_disk, self.check_memory, self.check_cpu,
                        self.check_services, self.check_errors]:
            checkbox.setFont(QFont("Segoe UI", 11))
            options_layout.addWidget(checkbox)

        self.options_group.setLayout(options_layout)
        add_shadow(self.options_group)
        layout.addWidget(self.options_group)

        # Botón de análisis
        self.analyze_btn = QPushButton(t.get('health_start'))
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #4CAF50, stop:1 #45a049);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 15px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #45a049, stop:1 #3d8b40);
            }
        """)
        self.analyze_btn.clicked.connect(self.run_health_check)
        add_shadow(self.analyze_btn)
        layout.addWidget(self.analyze_btn)

        # Área de resultados
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setMinimumHeight(250)
        add_shadow(self.results)
        layout.addWidget(self.results)

        layout.addStretch()
        self.setLayout(layout)

    def run_health_check(self):
        self.results.clear()
        self.results.append(t.get('health_starting'))

        if self.check_disk.isChecked():
            self.results.append(t.get('health_disk_label'))
            disk = psutil.disk_usage('/')
            self.results.append(t.get('health_disk_total', total=f"{disk.total / (1024**3):.1f}"))
            self.results.append(t.get('health_disk_used', used=f"{disk.used / (1024**3):.1f}", percent=disk.percent))
            self.results.append(t.get('health_disk_free', free=f"{disk.free / (1024**3):.1f}"))

        if self.check_memory.isChecked():
            self.results.append(t.get('health_memory_label'))
            mem = psutil.virtual_memory()
            self.results.append(t.get('health_memory_total', total=f"{mem.total / (1024**3):.1f}"))
            self.results.append(t.get('health_memory_used', used=f"{mem.used / (1024**3):.1f}", percent=mem.percent))
            self.results.append(t.get('health_memory_available', available=f"{mem.available / (1024**3):.1f}"))

        if self.check_cpu.isChecked():
            self.results.append(t.get('health_cpu_label'))
            self.results.append(t.get('health_cpu_usage', usage=psutil.cpu_percent(interval=1)))
            self.results.append(t.get('health_cpu_cores', cores=psutil.cpu_count()))

        if self.check_services.isChecked():
            self.results.append(t.get('health_services_label'))

        if self.check_errors.isChecked():
            self.results.append(t.get('health_errors_label'))
            try:
                # Intentar con dmesg primero
                result = subprocess.run(['dmesg'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and result.stdout:
                    # Buscar errores en las últimas líneas
                    errors = [line for line in result.stdout.split('\n')[-50:]
                             if 'error' in line.lower() or 'fail' in line.lower()]
                    if errors:
                        self.results.append(t.get('health_errors_found'))
                        for error in errors[-5:]:  # Mostrar solo los 5 más recientes
                            self.results.append(f"  • {error[:100]}")
                    else:
                        self.results.append(t.get('health_errors_none'))
                else:
                    # Si dmesg no funciona, intentar con journalctl
                    result = subprocess.run(['journalctl', '-p', 'err', '-n', '5', '--no-pager'],
                                          capture_output=True, text=True, timeout=5)
                    if result.stdout:
                        self.results.append(f"  {result.stdout}")
                    else:
                        self.results.append(t.get('health_errors_none'))
            except subprocess.TimeoutExpired:
                self.results.append(t.get('health_errors_timeout'))
            except Exception as e:
                self.results.append(t.get('health_errors_noaccess'))

        self.results.append(t.get('health_complete'))


class CustomCleanPanel(QWidget):
    """Panel de limpieza personalizada"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel(t.get('clean_title'))
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(self.title)

        # Opciones de limpieza
        self.options_group = QGroupBox(t.get('clean_select'))
        options_layout = QVBoxLayout()
        options_layout.setSpacing(12)

        self.clean_apt = QCheckBox(t.get('clean_apt'))
        self.clean_apt.setChecked(True)
        self.clean_thumbnails = QCheckBox(t.get('clean_thumbnails'))
        self.clean_thumbnails.setChecked(True)
        self.clean_trash = QCheckBox(t.get('clean_trash'))
        self.clean_trash.setChecked(True)
        self.clean_logs = QCheckBox(t.get('clean_logs'))
        self.clean_logs.setChecked(False)
        self.clean_cache = QCheckBox(t.get('clean_cache'))
        self.clean_cache.setChecked(True)
        self.clean_temp = QCheckBox(t.get('clean_temp'))
        self.clean_temp.setChecked(True)

        for checkbox in [self.clean_apt, self.clean_thumbnails, self.clean_trash,
                        self.clean_logs, self.clean_cache, self.clean_temp]:
            checkbox.setFont(QFont("Segoe UI", 11))
            options_layout.addWidget(checkbox)

        self.options_group.setLayout(options_layout)
        add_shadow(self.options_group)
        layout.addWidget(self.options_group)

        # Botón de limpieza
        self.clean_btn = QPushButton(t.get('clean_start'))
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #2196F3, stop:1 #1976D2);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 15px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #1976D2, stop:1 #1565C0);
            }
        """)
        self.clean_btn.clicked.connect(self.run_cleaning)
        add_shadow(self.clean_btn)
        layout.addWidget(self.clean_btn)

        # Área de resultados
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setMinimumHeight(180)
        add_shadow(self.results)
        layout.addWidget(self.results)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                height: 25px;
                border-radius: 12px;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        add_shadow(self.progress_bar)
        layout.addWidget(self.progress_bar)

        layout.addStretch()
        self.setLayout(layout)

    def run_cleaning(self):
        tasks = []

        if self.clean_apt.isChecked():
            tasks.append({'name': 'Limpieza de caché APT', 'type': 'command',
                         'command': 'pkexec apt-get clean'})

        if self.clean_thumbnails.isChecked():
            tasks.append({'name': 'Miniaturas', 'type': 'remove_cache',
                         'path': '~/.cache/thumbnails'})

        if self.clean_trash.isChecked():
            tasks.append({'name': 'Papelera', 'type': 'remove_cache',
                         'path': '~/.local/share/Trash'})

        if self.clean_cache.isChecked():
            # Limpiar solo cachés específicas conocidas, no todo ~/.cache
            cache_dirs = [
                '~/.cache/mozilla',
                '~/.cache/chromium',
                '~/.cache/google-chrome',
                '~/.cache/pip',
                '~/.cache/yarn'
            ]
            for cache_dir in cache_dirs:
                tasks.append({'name': f'Caché {cache_dir.split("/")[-1]}', 'type': 'remove_cache',
                             'path': cache_dir})

        if self.clean_temp.isChecked():
            tasks.append({'name': 'Archivos temporales', 'type': 'command',
                         'command': 'pkexec sh -c "find /tmp -type f -atime +7 -delete 2>/dev/null || true"'})

        if self.clean_logs.isChecked():
            tasks.append({'name': 'Logs antiguos', 'type': 'command',
                         'command': 'pkexec journalctl --vacuum-time=7d'})

        if not tasks:
            QMessageBox.warning(self, t.get('clean_warning_title'), t.get('clean_warning_msg'))
            return

        self.results.clear()
        self.results.append(t.get('clean_starting'))
        self.progress_bar.setValue(0)

        self.worker = WorkerThread('clean', tasks)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.cleaning_finished)
        self.worker.start()

        self.clean_btn.setEnabled(False)

    def update_progress(self, message):
        self.results.append(message)

    def cleaning_finished(self, results):
        self.results.append(f"\n{results}")
        self.results.append(t.get('clean_complete'))
        self.progress_bar.setValue(100)
        self.clean_btn.setEnabled(True)
        QMessageBox.information(self, t.get('clean_finished_title'), t.get('clean_finished_msg'))


class DriverUpdatePanel(QWidget):
    """Panel de actualización de drivers"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel(t.get('driver_title'))
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(self.title)

        self.info = QLabel(t.get('driver_info'))
        self.info.setFont(QFont("Segoe UI", 12))
        self.info.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        layout.addWidget(self.info)

        self.detect_btn = QPushButton(t.get('driver_detect'))
        self.detect_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #9C27B0, stop:1 #7B1FA2);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 15px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #7B1FA2, stop:1 #6A1B9A);
            }
        """)
        self.detect_btn.clicked.connect(self.detect_drivers)
        add_shadow(self.detect_btn)
        layout.addWidget(self.detect_btn)

        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setMinimumHeight(300)
        add_shadow(self.results)
        layout.addWidget(self.results)

        layout.addStretch()
        self.setLayout(layout)

    def detect_drivers(self):
        self.results.clear()
        self.results.append(t.get('driver_detecting'))

        try:
            # GPU - buscar VGA, 3D y Display
            result = subprocess.run(['lspci'], capture_output=True, text=True)
            gpu_found = False
            for line in result.stdout.split('\n'):
                if 'VGA' in line or '3D' in line or 'Display' in line:
                    gpu_info = line.split(':', 1)[-1].strip() if ':' in line else line.strip()
                    self.results.append(t.get('driver_gpu', gpu=gpu_info))
                    gpu_found = True
                    break

            if not gpu_found:
                self.results.append(t.get('driver_gpu_none'))

            # Red - buscar Network, Ethernet y Wireless
            net_found = False
            for line in result.stdout.split('\n'):
                if any(keyword in line.lower() for keyword in ['network', 'ethernet', 'wireless', 'wi-fi']):
                    net_info = line.split(':', 1)[-1].strip() if ':' in line else line.strip()
                    self.results.append(t.get('driver_net', net=net_info))
                    net_found = True
                    break

            if not net_found:
                self.results.append(t.get('driver_net_none'))

            self.results.append(t.get('driver_install_tip'))
            self.results.append(t.get('driver_install_cmd'))
            self.results.append(t.get('driver_check_tip'))
            self.results.append(t.get('driver_check_cmd'))

        except Exception as e:
            self.results.append(t.get('driver_error', error=str(e)))


class SystemUpdatePanel(QWidget):
    """Panel de actualización del sistema"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel(t.get('update_title'))
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(self.title)

        # Container de botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.check_btn = QPushButton(t.get('update_check'))
        self.check_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #FF9800, stop:1 #F57C00);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #F57C00, stop:1 #E64A19);
            }
        """)
        self.check_btn.clicked.connect(self.check_updates)
        add_shadow(self.check_btn)
        buttons_layout.addWidget(self.check_btn)

        self.update_btn = QPushButton(t.get('update_install'))
        self.update_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #F44336, stop:1 #D32F2F);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #D32F2F, stop:1 #C62828);
            }
        """)
        self.update_btn.clicked.connect(self.install_updates)
        add_shadow(self.update_btn)
        buttons_layout.addWidget(self.update_btn)

        layout.addLayout(buttons_layout)

        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setMinimumHeight(300)
        add_shadow(self.results)
        layout.addWidget(self.results)

        layout.addStretch()
        self.setLayout(layout)

    def check_updates(self):
        self.results.clear()
        self.results.append(t.get('update_checking'))
        self.check_btn.setEnabled(False)
        self.update_btn.setEnabled(False)

        self.worker = UpdateWorkerThread('check')
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.updates_checked)
        self.worker.start()

    def updates_checked(self, result):
        self.results.append(result)
        self.check_btn.setEnabled(True)
        self.update_btn.setEnabled(True)

    def update_progress(self, message):
        self.results.append(message)

    def install_updates(self):
        reply = QMessageBox.question(self, t.get('update_confirm_title'),
                                    t.get('update_confirm_msg'),
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.results.clear()
            self.results.append(t.get('update_installing'))
            self.check_btn.setEnabled(False)
            self.update_btn.setEnabled(False)

            self.worker = UpdateWorkerThread('install')
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.updates_installed)
            self.worker.start()

    def updates_installed(self, result):
        self.results.append(result)
        self.check_btn.setEnabled(True)
        self.update_btn.setEnabled(True)


class ToolsPanel(QWidget):
    """Panel de herramientas adicionales"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel(t.get('tools_title'))
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(self.title)

        # Botones de herramientas
        tools = [
            (t.get('tools_fix_nautilus'), self.fix_nautilus, "#FF5722"),
            (t.get('tools_clear_swap'), self.clear_swap, "#00BCD4"),
            (t.get('tools_fix_packages'), self.fix_packages, "#FFC107"),
            (t.get('tools_optimize_apt'), self.optimize_apt, "#8BC34A"),
        ]

        for tool_name, tool_func, color in tools:
            btn = QPushButton(tool_name)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    border: none;
                    border-radius: 15px;
                    color: white;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background: {color};
                    opacity: 0.8;
                }}
            """)
            btn.clicked.connect(tool_func)
            add_shadow(btn)
            layout.addWidget(btn)

        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setMinimumHeight(200)
        add_shadow(self.results)
        layout.addWidget(self.results)

        layout.addStretch()
        self.setLayout(layout)

    def fix_nautilus(self):
        self.results.append(t.get('tools_nautilus_fixing'))
        try:
            # Matar procesos de nautilus
            subprocess.run(['killall', 'nautilus'], stderr=subprocess.DEVNULL, check=False)
            self.results.append(t.get('tools_nautilus_stopped'))

            # Limpiar caché
            cache_path = os.path.expanduser('~/.cache/nautilus')
            if os.path.exists(cache_path):
                subprocess.run(['rm', '-rf', cache_path], check=False)
                self.results.append(t.get('tools_nautilus_cache'))

            # Limpiar metadata
            metadata_path = os.path.expanduser('~/.local/share/gvfs-metadata')
            if os.path.exists(metadata_path):
                subprocess.run(['rm', '-rf', metadata_path], check=False)
                self.results.append(t.get('tools_nautilus_metadata'))

            # Resetear configuración
            subprocess.run(['dconf', 'reset', '-f', '/org/gnome/nautilus/'],
                         stderr=subprocess.DEVNULL, check=False)
            self.results.append(t.get('tools_nautilus_reset'))

            self.results.append(t.get('tools_nautilus_complete'))
            self.results.append(t.get('tools_nautilus_restart'))
        except Exception as e:
            self.results.append(t.get('tools_error', error=str(e)))

    def clear_swap(self):
        self.results.append(t.get('tools_swap_clearing'))
        try:
            subprocess.run(['pkexec', 'swapoff', '-a'])
            subprocess.run(['pkexec', 'swapon', '-a'])
            self.results.append(t.get('tools_swap_complete'))
        except Exception as e:
            self.results.append(t.get('tools_error', error=str(e)))

    def fix_packages(self):
        self.results.append(t.get('tools_packages_fixing'))
        try:
            subprocess.run(['pkexec', 'dpkg', '--configure', '-a'])
            subprocess.run(['pkexec', 'apt', '--fix-broken', 'install'])
            self.results.append(t.get('tools_packages_complete'))
        except Exception as e:
            self.results.append(t.get('tools_error', error=str(e)))

    def optimize_apt(self):
        self.results.append(t.get('tools_apt_optimizing'))
        try:
            subprocess.run(['pkexec', 'apt', 'autoclean'])
            subprocess.run(['pkexec', 'apt', 'autoremove', '-y'])
            self.results.append(t.get('tools_apt_complete'))
        except Exception as e:
            self.results.append(t.get('tools_error', error=str(e)))


class SettingsPanel(QWidget):
    """Panel de configuración e información del sistema"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel(t.get('settings_title'))
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(self.title)

        # Información del sistema
        self.hardware_box = QGroupBox(t.get('settings_hardware'))
        hardware_layout = QVBoxLayout()
        hardware_layout.setSpacing(10)

        self.cpu_info = QLabel(t.get('settings_cpu', cpu=SystemInfo.get_cpu()))
        self.cpu_info.setFont(QFont("Segoe UI", 11))
        self.cpu_info.setStyleSheet("color: white;")
        self.cpu_info.setWordWrap(True)
        hardware_layout.addWidget(self.cpu_info)

        self.ram_info = QLabel(t.get('settings_ram', ram=SystemInfo.get_ram()))
        self.ram_info.setFont(QFont("Segoe UI", 11))
        self.ram_info.setStyleSheet("color: white;")
        hardware_layout.addWidget(self.ram_info)

        self.gpu_info = QLabel(t.get('settings_gpu', gpu=SystemInfo.get_gpu()))
        self.gpu_info.setFont(QFont("Segoe UI", 11))
        self.gpu_info.setStyleSheet("color: white;")
        self.gpu_info.setWordWrap(True)
        hardware_layout.addWidget(self.gpu_info)

        self.os_info = QLabel(t.get('settings_os', os=SystemInfo.get_os()))
        self.os_info.setFont(QFont("Segoe UI", 11))
        self.os_info.setStyleSheet("color: white;")
        self.os_info.setWordWrap(True)
        hardware_layout.addWidget(self.os_info)

        self.hardware_box.setLayout(hardware_layout)
        add_shadow(self.hardware_box)
        layout.addWidget(self.hardware_box)

        # Información de la aplicación
        self.info_box = QGroupBox(t.get('settings_about'))
        info_layout = QVBoxLayout()

        self.app_name = QLabel(t.get('app_title'))
        self.app_name.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.app_name.setStyleSheet("color: white;")
        info_layout.addWidget(self.app_name)

        self.version = QLabel(t.get('app_version'))
        self.version.setFont(QFont("Segoe UI", 12))
        self.version.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        info_layout.addWidget(self.version)

        self.description = QLabel(t.get('app_description'))
        self.description.setFont(QFont("Segoe UI", 11))
        self.description.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        self.description.setWordWrap(True)
        info_layout.addWidget(self.description)

        self.info_box.setLayout(info_layout)
        add_shadow(self.info_box)
        layout.addWidget(self.info_box)

        # Checkbox de autostart
        self.autostart_checkbox = QCheckBox(t.get('settings_autostart'))
        self.autostart_checkbox.setFont(QFont("Segoe UI", 12))
        self.autostart_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                padding: 15px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
            }
        """)
        self.autostart_checkbox.setChecked(self.is_autostart_enabled())
        self.autostart_checkbox.stateChanged.connect(self.toggle_autostart)
        add_shadow(self.autostart_checkbox)
        layout.addWidget(self.autostart_checkbox)

        # Label de estado de autostart
        self.autostart_status = QLabel()
        self.autostart_status.setFont(QFont("Segoe UI", 10))
        self.autostart_status.setStyleSheet("color: rgba(255, 255, 255, 0.7); padding-left: 20px;")
        self.autostart_status.setWordWrap(True)
        self.update_autostart_status()
        layout.addWidget(self.autostart_status)

        layout.addStretch()
        self.setLayout(layout)

    def is_autostart_enabled(self):
        """Verificar si autostart está habilitado"""
        autostart_dir = os.path.expanduser('~/.config/autostart')
        autostart_file = os.path.join(autostart_dir, 'jaime-system-care.desktop')
        return os.path.exists(autostart_file)

    def update_autostart_status(self):
        """Actualizar el label de estado"""
        if self.is_autostart_enabled():
            self.autostart_status.setText(t.get('settings_autostart_enabled'))
        else:
            self.autostart_status.setText(t.get('settings_autostart_disabled'))

    def toggle_autostart(self, state):
        """Activar o desactivar autostart"""
        autostart_dir = os.path.expanduser('~/.config/autostart')
        autostart_file = os.path.join(autostart_dir, 'jaime-system-care.desktop')

        if state == Qt.Checked:
            # Crear directorio si no existe
            os.makedirs(autostart_dir, exist_ok=True)

            # Determinar la ruta del ejecutable
            if os.path.exists('/usr/share/jaime/jaime.py'):
                # Instalado desde .deb
                exec_path = '/usr/bin/jaime'
            else:
                # Ejecutándose desde código fuente
                exec_path = os.path.abspath(__file__)

            # Crear archivo .desktop
            desktop_content = f"""[Desktop Entry]
Type=Application
Name=Jaime System Care
Comment=Sistema de mantenimiento y optimización para Linux
Exec=python3 {exec_path}
Icon=jaime
Terminal=false
Categories=System;Utility;
X-GNOME-Autostart-enabled=true
"""
            try:
                with open(autostart_file, 'w') as f:
                    f.write(desktop_content)
                self.update_autostart_status()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo activar autostart: {str(e)}")
                self.autostart_checkbox.setChecked(False)
        else:
            # Eliminar archivo .desktop
            try:
                if os.path.exists(autostart_file):
                    os.remove(autostart_file)
                self.update_autostart_status()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo desactivar autostart: {str(e)}")
                self.autostart_checkbox.setChecked(True)


class LanguagePanel(QWidget):
    """Panel de selección de idioma"""

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel(t.get('language_title'))
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(self.title)

        self.info = QLabel(t.get('language_info'))
        self.info.setFont(QFont("Segoe UI", 12))
        self.info.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        layout.addWidget(self.info)

        # Botones de idiomas con códigos de país
        languages = [
            ("[ES] Español", "#FF5722", "es"),       # España
            ("[GB] English", "#2196F3", "en"),       # Reino Unido
            ("[PT] Português", "#4CAF50", "pt"),     # Portugal
            ("[FR] Français", "#9C27B0", "fr"),      # Francia
            ("[IT] Italiano", "#FF9800", "it"),      # Italia
            ("[DE] Deutsch", "#00BCD4", "de"),       # Alemania
            ("[RU] Русский", "#E91E63", "ru"),       # Rusia
            ("[SA] العربية", "#009688", "ar"),       # Arabia Saudita
            ("[RO] Română", "#795548", "ro"),        # Rumanía
        ]

        for lang_name, color, lang_code in languages:
            btn = QPushButton(lang_name)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    border: none;
                    border-radius: 15px;
                    color: white;
                    padding: 20px;
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: {color};
                    opacity: 0.8;
                }}
            """)
            btn.clicked.connect(lambda checked, code=lang_code: self.change_language(code))
            add_shadow(btn)
            layout.addWidget(btn)

        self.status = QLabel(t.get('language_current', language=t.get_language_name()))
        self.status.setFont(QFont("Segoe UI", 14))
        self.status.setStyleSheet("color: white; margin-top: 20px;")
        layout.addWidget(self.status)

        layout.addStretch()
        self.setLayout(layout)

    def change_language(self, lang_code):
        """Cambiar el idioma de la aplicación"""
        if t.set_language(lang_code):
            lang_name = t.get_language_name(lang_code)
            self.status.setText(t.get('language_changed', language=lang_name))

            # Mostrar mensaje de confirmación
            restart_msg = "\n\nPor favor reinicia la aplicación para aplicar todos los cambios." if self.main_window else ""
            QMessageBox.information(self, t.get('language_title'),
                                  t.get('language_changed', language=lang_name) + restart_msg)

            # Actualizar la interfaz actual
            if self.main_window:
                self.main_window.update_ui_language()


class BackupPanel(QWidget):
    """Panel de copias de seguridad con Timeshift (sistema) y rsync (HOME)"""

    def __init__(self):
        super().__init__()
        self.selected_snapshot = None
        self.backup_location = os.path.expanduser('~/Backups')
        self.init_ui()

    def init_ui(self):
        from datetime import datetime
        from PyQt5.QtWidgets import QRadioButton, QButtonGroup, QFileDialog, QListWidget

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title = QLabel(t.get('backup_title'))
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(self.title)

        self.info = QLabel(t.get('backup_info'))
        self.info.setFont(QFont("Segoe UI", 12))
        self.info.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        self.info.setWordWrap(True)
        layout.addWidget(self.info)

        # Grupo: Tipo de backup
        self.type_group = QGroupBox(t.get('backup_type_label'))
        type_layout = QVBoxLayout()
        type_layout.setSpacing(12)

        self.backup_type_group = QButtonGroup()
        self.radio_home = QRadioButton(t.get('backup_type_home'))
        self.radio_home.setChecked(True)
        self.radio_home.setFont(QFont("Segoe UI", 11))
        self.backup_type_group.addButton(self.radio_home, 1)
        type_layout.addWidget(self.radio_home)

        self.radio_system = QRadioButton(t.get('backup_type_system'))
        self.radio_system.setFont(QFont("Segoe UI", 11))
        self.backup_type_group.addButton(self.radio_system, 2)
        type_layout.addWidget(self.radio_system)

        self.type_group.setLayout(type_layout)
        add_shadow(self.type_group)
        layout.addWidget(self.type_group)

        # Grupo: Ubicación (solo para HOME)
        self.location_group = QGroupBox(t.get('backup_location_label'))
        location_layout = QHBoxLayout()

        self.location_label = QLabel(self.backup_location)
        self.location_label.setFont(QFont("Segoe UI", 10))
        self.location_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); padding: 8px;")
        location_layout.addWidget(self.location_label)

        self.location_btn = QPushButton(t.get('backup_location_choose'))
        self.location_btn.clicked.connect(self.choose_location)
        location_layout.addWidget(self.location_btn)

        self.location_group.setLayout(location_layout)
        add_shadow(self.location_group)
        layout.addWidget(self.location_group)

        # Grupo: Tipo de restauración
        self.restore_type_group = QGroupBox(t.get('backup_restore_type_label'))
        restore_layout = QVBoxLayout()
        restore_layout.setSpacing(12)

        self.restore_button_group = QButtonGroup()
        self.radio_restore_full = QRadioButton(t.get('backup_restore_full'))
        self.radio_restore_full.setChecked(True)
        self.radio_restore_full.setFont(QFont("Segoe UI", 11))
        self.restore_button_group.addButton(self.radio_restore_full, 1)
        restore_layout.addWidget(self.radio_restore_full)

        self.radio_restore_selective = QRadioButton(t.get('backup_restore_selective'))
        self.radio_restore_selective.setFont(QFont("Segoe UI", 11))
        self.restore_button_group.addButton(self.radio_restore_selective, 2)
        restore_layout.addWidget(self.radio_restore_selective)

        self.restore_type_group.setLayout(restore_layout)
        add_shadow(self.restore_type_group)
        layout.addWidget(self.restore_type_group)

        # Botones de acción - Fila 1
        buttons_layout1 = QHBoxLayout()
        buttons_layout1.setSpacing(15)

        self.check_btn = QPushButton(t.get('backup_check_timeshift'))
        self.check_btn.setStyleSheet(self.get_button_style("#2196F3", "#1976D2"))
        self.check_btn.clicked.connect(self.check_timeshift)
        add_shadow(self.check_btn)
        buttons_layout1.addWidget(self.check_btn)

        self.install_btn = QPushButton(t.get('backup_install_timeshift'))
        self.install_btn.setStyleSheet(self.get_button_style("#FF9800", "#F57C00"))
        self.install_btn.clicked.connect(self.install_timeshift)
        add_shadow(self.install_btn)
        buttons_layout1.addWidget(self.install_btn)

        layout.addLayout(buttons_layout1)

        # Botones de acción - Fila 2
        buttons_layout2 = QHBoxLayout()
        buttons_layout2.setSpacing(15)

        self.create_btn = QPushButton(t.get('backup_create'))
        self.create_btn.setStyleSheet(self.get_button_style("#4CAF50", "#45a049"))
        self.create_btn.clicked.connect(self.create_backup)
        add_shadow(self.create_btn)
        buttons_layout2.addWidget(self.create_btn)

        self.list_btn = QPushButton(t.get('backup_list'))
        self.list_btn.setStyleSheet(self.get_button_style("#9C27B0", "#7B1FA2"))
        self.list_btn.clicked.connect(self.list_backups)
        add_shadow(self.list_btn)
        buttons_layout2.addWidget(self.list_btn)

        layout.addLayout(buttons_layout2)

        # Botones de acción - Fila 3
        buttons_layout3 = QHBoxLayout()
        buttons_layout3.setSpacing(15)

        self.restore_btn = QPushButton(t.get('backup_restore'))
        self.restore_btn.setStyleSheet(self.get_button_style("#00BCD4", "#0097A7"))
        self.restore_btn.clicked.connect(self.restore_backup)
        add_shadow(self.restore_btn)
        buttons_layout3.addWidget(self.restore_btn)

        self.delete_btn = QPushButton(t.get('backup_delete'))
        self.delete_btn.setStyleSheet(self.get_button_style("#F44336", "#D32F2F"))
        self.delete_btn.clicked.connect(self.delete_backup)
        add_shadow(self.delete_btn)
        buttons_layout3.addWidget(self.delete_btn)

        layout.addLayout(buttons_layout3)

        # Área de resultados
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setMinimumHeight(250)
        add_shadow(self.results)
        layout.addWidget(self.results)

        layout.addStretch()
        self.setLayout(layout)

    def get_button_style(self, color1, color2):
        """Generar estilo consistente para botones"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 {color1}, stop:1 {color2});
                border: none;
                border-radius: 15px;
                color: white;
                padding: 15px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 {color2}, stop:1 {color1});
            }}
            QPushButton:disabled {{
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }}
        """

    def choose_location(self):
        """Seleccionar ubicación para backups de HOME"""
        from PyQt5.QtWidgets import QFileDialog
        directory = QFileDialog.getExistingDirectory(self, t.get('backup_location_choose'),
                                                      self.backup_location)
        if directory:
            self.backup_location = directory
            self.location_label.setText(directory)

    def check_timeshift(self):
        """Verificar si Timeshift está instalado"""
        self.results.clear()
        self.results.append(t.get('backup_checking'))

        try:
            result = subprocess.run(['which', 'timeshift'], capture_output=True, text=True)
            if result.returncode == 0:
                # Obtener versión de Timeshift
                version_result = subprocess.run(['timeshift', '--version'],
                                              capture_output=True, text=True)
                version = version_result.stdout.strip() if version_result.returncode == 0 else "desconocida"
                self.results.append(t.get('backup_timeshift_found', version=version))
            else:
                self.results.append(t.get('backup_timeshift_notfound'))
        except Exception as e:
            self.results.append(t.get('backup_create_error', error=str(e)))

    def install_timeshift(self):
        """Instalar Timeshift usando pkexec"""
        self.results.clear()
        self.results.append(t.get('backup_timeshift_installing'))
        self.install_btn.setEnabled(False)

        try:
            result = subprocess.run(['pkexec', 'apt-get', 'install', '-y', 'timeshift'],
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                self.results.append(t.get('backup_timeshift_installed'))
            else:
                self.results.append(t.get('backup_timeshift_install_error', error=result.stderr))
        except subprocess.TimeoutExpired:
            self.results.append("⏱️ Timeout: La instalación tardó demasiado tiempo.\n")
        except Exception as e:
            self.results.append(t.get('backup_timeshift_install_error', error=str(e)))
        finally:
            self.install_btn.setEnabled(True)

    def create_backup(self):
        """Crear backup según el tipo seleccionado"""
        from datetime import datetime
        from PyQt5.QtWidgets import QMessageBox

        reply = QMessageBox.question(self, t.get('backup_confirm_title'),
                                    t.get('backup_confirm_create'),
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        self.results.clear()
        self.create_btn.setEnabled(False)

        try:
            if self.radio_system.isChecked():
                # Backup de sistema completo con Timeshift
                self.results.append(t.get('backup_creating'))
                self.results.append(t.get('backup_warning_root'))

                result = subprocess.run(['pkexec', 'timeshift', '--create',
                                       '--comments', 'Backup creado por Jaime System Care'],
                                      capture_output=True, text=True, timeout=600)
                if result.returncode == 0:
                    self.results.append(t.get('backup_create_success'))
                    self.results.append(f"\n{result.stdout}")
                else:
                    self.results.append(t.get('backup_create_error', error=result.stderr))
            else:
                # Backup de carpeta HOME con rsync
                self.results.append(t.get('backup_creating'))
                os.makedirs(self.backup_location, exist_ok=True)

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = os.path.join(self.backup_location, f'home_backup_{timestamp}')

                home_dir = os.path.expanduser('~')
                exclude_patterns = [
                    '--exclude=.cache',
                    '--exclude=.local/share/Trash',
                    '--exclude=.thumbnails',
                    '--exclude=Downloads',
                    '--exclude=Backups'
                ]

                rsync_cmd = ['rsync', '-av'] + exclude_patterns + [f'{home_dir}/', backup_path]
                result = subprocess.run(rsync_cmd, capture_output=True, text=True, timeout=1200)

                if result.returncode == 0:
                    self.results.append(t.get('backup_create_success'))
                    self.results.append(f"\n📁 Ubicación: {backup_path}\n")
                else:
                    self.results.append(t.get('backup_create_error', error=result.stderr))

        except subprocess.TimeoutExpired:
            self.results.append("⏱️ Timeout: El backup tardó demasiado tiempo.\n")
        except Exception as e:
            self.results.append(t.get('backup_create_error', error=str(e)))
        finally:
            self.create_btn.setEnabled(True)

    def list_backups(self):
        """Listar backups existentes"""
        from PyQt5.QtWidgets import QInputDialog

        self.results.clear()
        self.results.append(t.get('backup_listing'))

        try:
            if self.radio_system.isChecked():
                # Listar snapshots de Timeshift
                result = subprocess.run(['pkexec', 'timeshift', '--list'],
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    if result.stdout.strip():
                        self.results.append(t.get('backup_list_found'))
                        self.results.append(f"\n{result.stdout}")
                    else:
                        self.results.append(t.get('backup_list_empty'))
                else:
                    self.results.append(t.get('backup_create_error', error=result.stderr))
            else:
                # Listar backups de HOME
                if os.path.exists(self.backup_location):
                    backups = [d for d in os.listdir(self.backup_location)
                              if os.path.isdir(os.path.join(self.backup_location, d))
                              and d.startswith('home_backup_')]
                    if backups:
                        self.results.append(t.get('backup_list_found'))
                        for backup in sorted(backups, reverse=True):
                            backup_path = os.path.join(self.backup_location, backup)
                            size = self.get_dir_size(backup_path)
                            self.results.append(f"\n📁 {backup} ({self.format_size(size)})")
                    else:
                        self.results.append(t.get('backup_list_empty'))
                else:
                    self.results.append(t.get('backup_list_empty'))

        except subprocess.TimeoutExpired:
            self.results.append("⏱️ Timeout al listar backups.\n")
        except Exception as e:
            self.results.append(t.get('backup_create_error', error=str(e)))

    def restore_backup(self):
        """Restaurar desde backup"""
        from PyQt5.QtWidgets import QMessageBox, QInputDialog

        reply = QMessageBox.question(self, t.get('backup_confirm_title'),
                                    t.get('backup_confirm_restore'),
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        self.results.clear()
        self.restore_btn.setEnabled(False)

        try:
            if self.radio_system.isChecked():
                # Restauración de sistema con Timeshift
                self.results.append(t.get('backup_restoring'))
                self.results.append(t.get('backup_warning_root'))

                # Obtener lista de snapshots
                result = subprocess.run(['pkexec', 'timeshift', '--list'],
                                      capture_output=True, text=True, timeout=60)

                if result.returncode == 0 and result.stdout.strip():
                    # Pedir al usuario que seleccione snapshot (simplificado)
                    snapshot_name, ok = QInputDialog.getText(self,
                                                            t.get('backup_select_snapshot'),
                                                            "Nombre del snapshot:")
                    if ok and snapshot_name:
                        restore_result = subprocess.run(['pkexec', 'timeshift', '--restore',
                                                        '--snapshot', snapshot_name],
                                                       capture_output=True, text=True, timeout=1200)
                        if restore_result.returncode == 0:
                            self.results.append(t.get('backup_restore_success'))
                        else:
                            self.results.append(t.get('backup_restore_error', error=restore_result.stderr))
                    else:
                        self.results.append(t.get('backup_no_selection'))
                else:
                    self.results.append(t.get('backup_list_empty'))
            else:
                # Restauración de HOME
                if os.path.exists(self.backup_location):
                    backups = [d for d in os.listdir(self.backup_location)
                              if os.path.isdir(os.path.join(self.backup_location, d))
                              and d.startswith('home_backup_')]

                    if backups:
                        backup_name, ok = QInputDialog.getItem(self,
                                                              t.get('backup_select_snapshot'),
                                                              "Selecciona backup:",
                                                              sorted(backups, reverse=True), 0, False)
                        if ok and backup_name:
                            self.results.append(t.get('backup_restoring'))
                            backup_path = os.path.join(self.backup_location, backup_name)
                            home_dir = os.path.expanduser('~')

                            rsync_cmd = ['rsync', '-av', f'{backup_path}/', home_dir]
                            result = subprocess.run(rsync_cmd, capture_output=True, text=True, timeout=1200)

                            if result.returncode == 0:
                                self.results.append(t.get('backup_restore_success'))
                            else:
                                self.results.append(t.get('backup_restore_error', error=result.stderr))
                        else:
                            self.results.append(t.get('backup_no_selection'))
                    else:
                        self.results.append(t.get('backup_list_empty'))
                else:
                    self.results.append(t.get('backup_list_empty'))

        except subprocess.TimeoutExpired:
            self.results.append("⏱️ Timeout durante la restauración.\n")
        except Exception as e:
            self.results.append(t.get('backup_restore_error', error=str(e)))
        finally:
            self.restore_btn.setEnabled(True)

    def delete_backup(self):
        """Eliminar backup seleccionado"""
        from PyQt5.QtWidgets import QMessageBox, QInputDialog

        reply = QMessageBox.question(self, t.get('backup_confirm_title'),
                                    t.get('backup_confirm_delete'),
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        self.results.clear()
        self.delete_btn.setEnabled(False)

        try:
            if self.radio_system.isChecked():
                # Eliminar snapshot de Timeshift
                snapshot_name, ok = QInputDialog.getText(self,
                                                        t.get('backup_select_snapshot'),
                                                        "Nombre del snapshot:")
                if ok and snapshot_name:
                    self.results.append(t.get('backup_deleting'))
                    result = subprocess.run(['pkexec', 'timeshift', '--delete',
                                           '--snapshot', snapshot_name],
                                          capture_output=True, text=True, timeout=120)
                    if result.returncode == 0:
                        self.results.append(t.get('backup_delete_success'))
                    else:
                        self.results.append(t.get('backup_delete_error', error=result.stderr))
                else:
                    self.results.append(t.get('backup_no_selection'))
            else:
                # Eliminar backup de HOME
                if os.path.exists(self.backup_location):
                    backups = [d for d in os.listdir(self.backup_location)
                              if os.path.isdir(os.path.join(self.backup_location, d))
                              and d.startswith('home_backup_')]

                    if backups:
                        backup_name, ok = QInputDialog.getItem(self,
                                                              t.get('backup_select_snapshot'),
                                                              "Selecciona backup:",
                                                              sorted(backups, reverse=True), 0, False)
                        if ok and backup_name:
                            self.results.append(t.get('backup_deleting'))
                            backup_path = os.path.join(self.backup_location, backup_name)

                            import shutil
                            shutil.rmtree(backup_path)
                            self.results.append(t.get('backup_delete_success'))
                        else:
                            self.results.append(t.get('backup_no_selection'))
                    else:
                        self.results.append(t.get('backup_list_empty'))
                else:
                    self.results.append(t.get('backup_list_empty'))

        except subprocess.TimeoutExpired:
            self.results.append("⏱️ Timeout al eliminar backup.\n")
        except Exception as e:
            self.results.append(t.get('backup_delete_error', error=str(e)))
        finally:
            self.delete_btn.setEnabled(True)

    @staticmethod
    def get_dir_size(path):
        """Calcular tamaño de directorio"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size

    @staticmethod
    def format_size(size):
        """Formatear tamaño en bytes a formato legible"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"


class JaimeMainWindow(QMainWindow):
    """Ventana principal de Jaime"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Jaime System Care")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 500)  # Tamaño mínimo más pequeño para pantallas pequeñas

        # Configurar icono de la ventana (usar logo circular de 128px)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logo-Jaime-circular-128.png')
        # Fallback al logo original si no existe el circular
        if not os.path.exists(logo_path):
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logo-Jaime.png')

        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Barra superior con info del sistema (Secciones 1-2: 33% de altura)
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar, stretch=2)

        # Área de contenido (Secciones 3-4-5: 50% de altura) con scroll
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent;")

        # Añadir paneles con scroll
        self.health_panel = self.create_scrollable_panel(HealthCheckPanel())
        self.clean_panel = self.create_scrollable_panel(CustomCleanPanel())
        self.driver_panel = self.create_scrollable_panel(DriverUpdatePanel())
        self.update_panel = self.create_scrollable_panel(SystemUpdatePanel())
        self.tools_panel = self.create_scrollable_panel(ToolsPanel())
        self.backup_panel = self.create_scrollable_panel(BackupPanel())
        self.settings_panel = self.create_scrollable_panel(SettingsPanel())
        self.language_panel = self.create_scrollable_panel(LanguagePanel(main_window=self))

        self.stacked_widget.addWidget(self.health_panel)
        self.stacked_widget.addWidget(self.clean_panel)
        self.stacked_widget.addWidget(self.driver_panel)
        self.stacked_widget.addWidget(self.update_panel)
        self.stacked_widget.addWidget(self.tools_panel)
        self.stacked_widget.addWidget(self.backup_panel)
        self.stacked_widget.addWidget(self.settings_panel)
        self.stacked_widget.addWidget(self.language_panel)

        main_layout.addWidget(self.stacked_widget, stretch=3)

        # Barra inferior de navegación (Sección 6: 17% de altura)
        bottom_bar = self.create_bottom_bar()
        main_layout.addWidget(bottom_bar, stretch=1)

        # Aplicar estilos globales
        self.setStyleSheet(GLOBAL_STYLES)

    def create_scrollable_panel(self, panel_widget):
        """Envolver un panel en un área con scroll para hacerlo responsive"""
        scroll_area = QScrollArea()
        scroll_area.setWidget(panel_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.5);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        return scroll_area

    def create_top_bar(self):
        """Crear barra superior simple (Secciones 1-2)"""
        top_widget = QFrame()
        top_widget.setFrameStyle(QFrame.StyledPanel)
        top_widget.setStyleSheet("background-color: #2c3e50; color: white; padding: 20px;")

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        # Versión (izquierda)
        version_label = QLabel("v1.3.0")
        version_label.setFont(QFont("Arial", 14))
        layout.addWidget(version_label)

        layout.addStretch()

        # Logo central
        logo_container = QWidget()
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(15)
        logo_layout.setContentsMargins(0, 0, 0, 0)

        # Cargar imagen del logo (circular, más grande y visible)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logo-Jaime-circular-80.png')
        # Fallback al logo cuadrado si no existe el circular
        if not os.path.exists(logo_path):
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logo-Jaime.png')

        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            # Logo más grande (80px) para mejor visibilidad
            logo_scaled = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_img = QLabel()
            logo_img.setPixmap(logo_scaled)
            logo_layout.addWidget(logo_img)

        logo_label = QLabel("JAIME")
        logo_label.setFont(QFont("Arial", 28, QFont.Bold))
        logo_layout.addWidget(logo_label)

        logo_container.setLayout(logo_layout)
        layout.addWidget(logo_container)

        layout.addStretch()

        top_widget.setLayout(layout)
        return top_widget

    def create_bottom_bar(self):
        """Crear barra inferior de navegación"""
        bottom_widget = QFrame()
        bottom_widget.setStyleSheet("""
            QFrame {
                background: rgba(0, 0, 0, 0.3);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding: 10px;
            }
        """)

        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 10, 20, 10)

        self.buttons_data = [
            ('nav_health', 0),
            ('nav_clean', 1),
            ('nav_drivers', 2),
            ('nav_updates', 3),
            ('nav_tools', 4),
            ('nav_backup', 5),
            ('nav_settings', 6),
            ('nav_language', 7)
        ]

        self.nav_buttons = []

        for text_key, index in self.buttons_data:
            btn = QPushButton(t.get(text_key))
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                    color: white;
                    padding: 8px 12px;
                    font-size: 11px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 0.25);
                }
            """)
            btn.clicked.connect(lambda checked, i=index: self.switch_panel(i))
            add_shadow(btn)
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        add_shadow(bottom_widget)
        bottom_widget.setLayout(layout)
        return bottom_widget

    def switch_panel(self, index):
        """Cambiar de panel con animación"""
        self.stacked_widget.setCurrentIndex(index)

    def update_ui_language(self):
        """Actualizar textos de la interfaz cuando cambie el idioma"""
        # Actualizar botones de navegación
        for i, (text_key, _) in enumerate(self.buttons_data):
            if i < len(self.nav_buttons):
                self.nav_buttons[i].setText(t.get(text_key))


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Usar estilo Fusion para mejor apariencia

    # Configurar icono de la aplicación (circular 128px desde pixmaps)
    logo_path = '/usr/share/pixmaps/jaime.png'
    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))
    else:
        # Fallback a logo local si no está instalado
        local_logo = os.path.join(os.path.dirname(__file__), '..', 'logo-Jaime-circular-128.png')
        if os.path.exists(local_logo):
            app.setWindowIcon(QIcon(local_logo))

    window = JaimeMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
