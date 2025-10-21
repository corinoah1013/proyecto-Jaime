# 🛠️ Jaime System Care

<p align="center">
  <img src="logo-Jaime-circular-256.png" alt="Jaime System Care Logo" width="200"/>
</p>

<p align="center">
  <strong>Sistema completo de mantenimiento y optimización para distribuciones Linux basadas en Debian</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.3.0-blue.svg" alt="Version 1.3.0"/>
  <img src="https://img.shields.io/badge/python-3.x-green.svg" alt="Python 3.x"/>
  <img src="https://img.shields.io/badge/license-GPL--3.0-orange.svg" alt="GPL-3.0"/>
  <img src="https://img.shields.io/badge/platform-Linux-lightgrey.svg" alt="Linux"/>
</p>

---

## 📋 Índice

- [Características](#-características)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Idiomas Soportados](#-idiomas-soportados)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Desarrollo](#-desarrollo)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Contacto](#-contacto)

---

## ✨ Características

### 🏥 Health Check del Sistema
- Verificación completa del estado del sistema
- Análisis de CPU, RAM, disco y temperatura
- Detección de procesos zombies
- Verificación de servicios críticos
- Reporte detallado con recomendaciones

### 🧹 Limpieza Personalizada
- Limpieza de caché de APT (`/var/cache/apt/archives/`)
- Eliminación de archivos temporales (`/tmp/`)
- Limpieza de logs antiguos (`/var/log/`)
- Vaciado de papelera del usuario (`~/.local/share/Trash/`)
- Limpieza de caché de thumbnails (`~/.cache/thumbnails/`)
- Selección individual de cada tipo de limpieza

### 💾 Sistema de Copias de Seguridad
- **Backup completo del sistema** con Timeshift
- **Backup de carpeta HOME** con rsync
- Selección de ubicación personalizada para backups
- Creación, listado y restauración de backups
- Eliminación de backups antiguos
- Opciones de restauración completa y selectiva
- Verificación e instalación automática de Timeshift

### 🔧 Actualización de Drivers
- Detección automática de drivers disponibles
- Instalación segura con pkexec
- Soporte para drivers propietarios de NVIDIA, AMD, Intel
- Actualización de firmware del sistema

### 🔄 Actualización del Sistema
- Actualización de paquetes con `apt update && apt upgrade`
- Limpieza automática post-actualización
- Progreso en tiempo real
- Manejo seguro de privilegios con pkexec

### 🛠️ Herramientas del Sistema
- Reparación de paquetes rotos (`dpkg --configure -a`, `apt --fix-broken install`)
- Limpieza de paquetes huérfanos (`deborphan`)
- Verificación de integridad del sistema de archivos
- Reparación de GRUB
- Recreación de initramfs

### ⚙️ Panel de Configuración
- **Inicio automático con el sistema** (autostart)
- Selector de idioma con 9 idiomas disponibles
- Temas visuales (claro/oscuro)
- Configuración de notificaciones
- Personalización de la interfaz

### 🌍 Soporte Multi-idioma
- **9 idiomas** completamente traducidos (159 claves de traducción)
- Soporte **RTL (Right-to-Left)** para Árabe
- Cambio de idioma en tiempo real sin reiniciar
- Traducción completa de toda la interfaz

### 🎨 Interfaz Moderna
- Diseño **Glassmorphism** con transparencia y blur
- Logos circulares de alta calidad (5 tamaños disponibles)
- Responsive y adaptable
- Iconos intuitivos y modernos
- Feedback visual para todas las acciones

---

## 📸 Capturas de Pantalla

> **Nota:** Agrega capturas de pantalla de la aplicación aquí cuando estén disponibles.

---

## 📦 Requisitos

### Requisitos del Sistema
- **SO:** Distribución Linux basada en Debian (Ubuntu, Debian, Linux Mint, etc.)
- **Python:** 3.x
- **Arquitectura:** all (compatible con cualquier arquitectura)

### Dependencias
Las siguientes dependencias se instalan automáticamente con el paquete `.deb`:

- `python3` - Intérprete de Python 3
- `python3-pyqt5` - Framework de interfaz gráfica
- `python3-psutil` - Información del sistema y procesos
- `policykit-1` - Gestión de privilegios
- `rsync` - Herramienta de sincronización para backups HOME
- `timeshift` - Herramienta de backup completo del sistema

### Dependencias Opcionales
- `deborphan` - Para detección de paquetes huérfanos
- Drivers propietarios según tu hardware (NVIDIA, AMD, etc.)

---

## 🚀 Instalación

### Opción 1: Instalación desde Paquete .deb (Recomendado)

1. **Descargar el paquete** `.deb` desde [Releases](../../releases):
   ```bash
   wget https://github.com/usuario/jaime-system-care/releases/download/v1.3.0/jaime-care_1.3.0_all.deb
   ```

2. **Instalar el paquete**:
   ```bash
   sudo dpkg -i jaime-care_1.3.0_all.deb
   ```

3. **Resolver dependencias** (si es necesario):
   ```bash
   sudo apt-get install -f
   ```

4. **Ejecutar la aplicación**:
   ```bash
   python3 /usr/share/jaime/jaime.py
   ```

   O buscar "Jaime System Care" en el menú de aplicaciones.

### Opción 2: Instalación desde Código Fuente

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/usuario/jaime-system-care.git
   cd jaime-system-care
   ```

2. **Instalar dependencias manualmente**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pyqt5 python3-psutil \
                        policykit-1 rsync timeshift
   ```

3. **Ejecutar desde el código fuente**:
   ```bash
   cd src
   python3 jaime.py
   ```

### Opción 3: Construir tu Propio Paquete .deb

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/usuario/jaime-system-care.git
   cd jaime-system-care
   ```

2. **Construir el paquete**:
   ```bash
   dpkg-deb --build debian
   mv debian.deb jaime-care_1.3.0_all.deb
   ```

3. **Instalar**:
   ```bash
   sudo dpkg -i jaime-care_1.3.0_all.deb
   sudo apt-get install -f
   ```

---

## 🎯 Uso

### Inicio Rápido

1. **Abrir Jaime System Care** desde el menú de aplicaciones o ejecutar:
   ```bash
   python3 /usr/share/jaime/jaime.py
   ```

2. **Navegar por los paneles** usando los botones del menú lateral:
   - 🏥 Health Check
   - 🧹 Custom Clean
   - 💾 Backup
   - 🔧 Driver Update
   - 🔄 System Update
   - 🛠️ Tools
   - ⚙️ Settings
   - 🌍 Language

3. **Realizar operaciones** haciendo clic en los botones de cada panel.

### Tareas Comunes

#### Realizar un Health Check
1. Ir al panel **Health Check**
2. Hacer clic en **"🔍 Ejecutar Health Check"**
3. Revisar el reporte detallado

#### Limpiar el Sistema
1. Ir al panel **Custom Clean**
2. Seleccionar los tipos de limpieza deseados
3. Hacer clic en **"🧹 Ejecutar Limpieza"**

#### Crear una Copia de Seguridad
1. Ir al panel **Backup**
2. Seleccionar tipo de backup:
   - **HOME**: Backup de carpeta personal
   - **Sistema**: Backup completo con Timeshift
3. (Opcional) Cambiar ubicación de backup
4. Hacer clic en **"💾 Crear Copia de Seguridad"**

#### Activar Inicio Automático
1. Ir al panel **Settings**
2. Activar checkbox **"🚀 Iniciar con el sistema"**
3. La aplicación se iniciará automáticamente al encender el PC

#### Cambiar Idioma
1. Ir al panel **Language**
2. Hacer clic en el idioma deseado
3. La interfaz cambia instantáneamente

---

## 🌍 Idiomas Soportados

Jaime System Care está completamente traducido a **9 idiomas**:

| Código | Idioma | Nombre Nativo | Claves Traducidas | RTL |
|--------|--------|---------------|-------------------|-----|
| ES | Español | Español | 159 | No |
| EN | Inglés | English | 159 | No |
| PT | Portugués | Português | 159 | No |
| FR | Francés | Français | 159 | No |
| IT | Italiano | Italiano | 159 | No |
| DE | Alemán | Deutsch | 159 | No |
| RU | Ruso | Русский | 159 | No |
| AR | Árabe | العربية | 159 | **Sí** |
| RO | Rumano | Română | 159 | No |

**Total:** 1,431 traducciones individuales

---

## 📁 Estructura del Proyecto

```
proyecto Jaime/
├── src/                              # Código fuente
│   ├── jaime.py                      # Aplicación principal (1740 líneas)
│   └── translations.py               # Sistema de traducciones (9 idiomas × 159 claves)
│
├── debian/                           # Estructura del paquete .deb
│   ├── DEBIAN/
│   │   ├── control                   # Metadatos del paquete
│   │   ├── postinst                  # Script post-instalación
│   │   └── prerm                     # Script pre-eliminación
│   │
│   └── usr/
│       ├── share/
│       │   ├── jaime/
│       │   │   ├── jaime.py          # App instalada (sincronizada con src/)
│       │   │   ├── logo-Jaime-circular-*.png  # Logos (5 tamaños)
│       │   │   └── translations.py   # Traducciones
│       │   │
│       │   └── pixmaps/
│       │       └── jaime.png         # Icono del sistema (128x128px)
│       │
│       └── bin/                      # (Opcional) Enlaces simbólicos
│
├── logo-Jaime.png                    # Logo original (1024×1024px)
├── logo-Jaime-circular-512.png       # Logo circular alta resolución
├── logo-Jaime-circular-256.png       # Logo circular media resolución
├── logo-Jaime-circular-128.png       # Logo circular icono de app
├── logo-Jaime-circular-80.png        # Logo circular UI principal
├── logo-Jaime-circular-60.png        # Logo circular UI secundaria
│
├── convert_logo_circular.py          # Script de conversión de logos
├── test_logos_visual.py              # Herramienta de test visual de logos
│
├── README.md                         # Este archivo
├── CHANGELOG.md                      # Historial de versiones
├── LOGOS_README.md                   # Documentación del sistema de logos
└── LICENSE                           # Licencia GPL-3.0
```

---

## 🔨 Desarrollo

### Configuración del Entorno de Desarrollo

1. **Clonar repositorio**:
   ```bash
   git clone https://github.com/usuario/jaime-system-care.git
   cd jaime-system-care
   ```

2. **Instalar dependencias de desarrollo**:
   ```bash
   sudo apt-get install python3 python3-pyqt5 python3-psutil \
                        python3-pil policykit-1 rsync timeshift \
                        dpkg-dev debhelper
   ```

3. **Ejecutar desde el código fuente**:
   ```bash
   cd src
   python3 jaime.py
   ```

### Modificar Traducciones

Editar `src/translations.py`:

```python
TRANSLATIONS = {
    'es': {
        'nueva_clave': 'Texto en español',
        # ... 159 claves
    },
    'en': {
        'nueva_clave': 'Text in English',
        # ... 159 claves
    },
    # ... 9 idiomas
}
```

**Importante:** Cada idioma debe tener exactamente **159 claves** para mantener consistencia.

### Regenerar Logos Circulares

Si actualizas `logo-Jaime.png`:

```bash
python3 convert_logo_circular.py
python3 test_logos_visual.py  # Verificar visualmente
```

Esto genera automáticamente los 5 tamaños y los sincroniza con `debian/`.

### Sincronizar Cambios entre src/ y debian/

Después de modificar archivos en `src/`:

```bash
# Sincronizar manualmente
cp src/jaime.py debian/usr/share/jaime/
cp src/translations.py debian/usr/share/jaime/

# Verificar diferencias
diff src/jaime.py debian/usr/share/jaime/jaime.py
```

### Construir Paquete .deb

```bash
# Desde el directorio raíz del proyecto
dpkg-deb --build debian
mv debian.deb jaime-care_1.3.0_all.deb

# Verificar el paquete
dpkg-deb --info jaime-care_1.3.0_all.deb
dpkg-deb --contents jaime-care_1.3.0_all.deb
```

### Testing

```bash
# Verificar sintaxis
python3 -m py_compile src/jaime.py
python3 -m py_compile src/translations.py

# Verificar traducciones
python3 -c "from src.translations import TRANSLATIONS; \
            print(f'Idiomas: {len(TRANSLATIONS)}'); \
            for lang in TRANSLATIONS: \
                print(f'{lang}: {len(TRANSLATIONS[lang])} claves')"

# Instalar localmente y probar
sudo dpkg -i jaime-care_1.3.0_all.deb
python3 /usr/share/jaime/jaime.py
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. **Fork** el repositorio
2. Crea una **rama** para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. **Commit** tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un **Pull Request**

### Guías de Contribución

- Mantén el estilo de código consistente con PyQt5
- Añade traducciones para **todos los 9 idiomas** al agregar nuevas funcionalidades
- Actualiza `CHANGELOG.md` con tus cambios
- Verifica que el paquete `.deb` se construya correctamente
- Prueba en al menos 2 distribuciones Debian (Ubuntu, Debian, etc.)

---

## 📄 Licencia

Este proyecto está licenciado bajo la **GNU General Public License v3.0**.

Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 📧 Contacto

**Desarrollador:** Sebastian Scuadroni / Amanda Software
**Email:** corinoah1013@gmail.com
**Versión:** 1.3.0
**Fecha:** 21 de octubre de 2025

---

## 🙏 Agradecimientos

- **Timeshift** - Por la excelente herramienta de backup del sistema
- **PyQt5** - Por el framework de interfaz gráfica
- **Comunidad de Debian/Ubuntu** - Por las herramientas y documentación
- **Traductores** - Por las contribuciones en diferentes idiomas

---

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para el historial completo de cambios.

### Versión Actual: 1.3.0 (2025-10-21)

**Nuevas Características:**
- Sistema de Copias de Seguridad (BackupPanel) con Timeshift + rsync
- Inicio automático con el sistema (autostart)
- Sistema de logos circulares (5 tamaños)
- Soporte completo multi-idioma (9 idiomas, 159 claves)
- Soporte RTL para Árabe

Ver el archivo completo para más detalles: [CHANGELOG.md](CHANGELOG.md)

---

<p align="center">
  <strong>Hecho con ❤️ para la comunidad Linux</strong>
</p>
