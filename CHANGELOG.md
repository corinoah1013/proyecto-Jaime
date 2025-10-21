# Changelog - Jaime System Care

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [1.3.0] - 2025-10-21

### ✨ Añadido
- **Sistema de Copias de Seguridad (BackupPanel)**
  - Backup completo del sistema usando Timeshift
  - Backup de carpeta HOME usando rsync
  - Creación, listado, restauración y eliminación de backups
  - Selección de ubicación personalizada para backups HOME
  - Opciones de restauración completa y selectiva
  - Verificación e instalación automática de Timeshift
  - 6 botones de acción con UI moderna
  - Radio buttons para selección de tipo de backup/restauración

- **Inicio Automático con el Sistema**
  - Checkbox en Panel de Configuración para autostart
  - Creación/eliminación automática de archivo .desktop
  - Indicador visual del estado de autostart
  - Compatible con GNOME, KDE, XFCE, MATE, Cinnamon

- **Sistema de Logos Circulares**
  - Logo circular de 512x512px (alta resolución)
  - Logo circular de 256x256px (resolución media)
  - Logo circular de 128x128px (icono de aplicación)
  - Logo circular de 80x80px (UI principal)
  - Logo circular de 60x60px (UI secundaria)
  - Script de conversión automática (convert_logo_circular.py)
  - Script de test visual (test_logos_visual.py)
  - Transparencia completa y anti-aliasing
  - Documentación completa (LOGOS_README.md)

- **Soporte Multi-idioma Completo**
  - 9 idiomas soportados: ES, EN, PT, FR, IT, DE, RU, AR, RO
  - 159 claves de traducción por idioma
  - 44 nuevas claves para BackupPanel
  - 3 nuevas claves para Autostart
  - Soporte RTL (Right-to-Left) para Árabe
  - Botones de idioma con códigos de país en texto

### 🔧 Mejorado
- Interfaz de usuario más moderna y responsive
- Mejor organización de paneles con scroll
- Logos circulares en lugar de cuadrados
- Sincronización completa entre src/ y debian/
- Documentación expandida

### 🐛 Corregido
- Inconsistencias en traducciones (language_romanian)
- Renderizado de banderas emoji en botones de idioma
- Permisos de archivos en paquete .deb
- Estructura de directorios para instalación

### 📦 Paquete
- Tamaño del .deb: 327 KB
- Versión: 1.3.0
- Dependencias actualizadas con timeshift y rsync
- Scripts postinst y prerm mejorados

---

## [1.2.0] - 2025-10-17

### ✨ Añadido
- Sistema multi-idioma mejorado
- Traducciones iniciales para BackupPanel (ES, EN)
- Logos circulares preliminares

### 🔧 Mejorado
- Rendimiento general de la aplicación
- Interfaz de usuario

---

## [1.0.0] - Fecha anterior

### ✨ Añadido
- Health Check Panel
- Custom Clean Panel
- Driver Update Panel
- System Update Panel
- Tools Panel
- Settings Panel
- Language Panel
- Interfaz gráfica con PyQt5
- Estilo glassmorphism

---

## Tipos de Cambios

- `✨ Añadido` - para funcionalidades nuevas
- `🔧 Mejorado` - para cambios en funcionalidades existentes
- `🐛 Corregido` - para corrección de errores
- `🗑️ Eliminado` - para funcionalidades eliminadas
- `🔒 Seguridad` - para correcciones de seguridad
- `📦 Paquete` - para cambios en el empaquetado

---

[1.3.0]: https://github.com/usuario/jaime-system-care/releases/tag/v1.3.0
[1.2.0]: https://github.com/usuario/jaime-system-care/releases/tag/v1.2.0
[1.0.0]: https://github.com/usuario/jaime-system-care/releases/tag/v1.0.0
