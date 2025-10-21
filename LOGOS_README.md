# 🎨 Sistema de Logos - Jaime System Care v1.3.0

## 📋 Resumen

El sistema de logos de Jaime System Care utiliza **logos circulares con transparencia** para una mejor integración visual con la interfaz moderna de la aplicación.

---

## 📁 Archivos Disponibles

### Logo Original
- **logo-Jaime.png** (1024x1024px, 1.5 MB)
  - Logo original en alta resolución
  - Formato cuadrado con transparencia
  - Base para generar versiones circulares

### Logos Circulares (5 tamaños)

| Archivo | Dimensiones | Tamaño | Uso |
|---------|------------|--------|-----|
| `logo-Jaime-circular-512.png` | 512x512px | 206 KB | Alta resolución / Marketing |
| `logo-Jaime-circular-256.png` | 256x256px | 58 KB | Resolución media |
| `logo-Jaime-circular-128.png` | 128x128px | 18 KB | **Icono de aplicación** |
| `logo-Jaime-circular-80.png` | 80x80px | 9 KB | **UI principal (barra superior)** |
| `logo-Jaime-circular-60.png` | 60x60px | 5 KB | UI secundaria |

**Características:**
- ✅ Formato PNG con canal alpha (RGBA)
- ✅ Transparencia completa (circular)
- ✅ Anti-aliasing suave
- ✅ Optimizados para tamaño de archivo

---

## 📂 Ubicaciones en el Proyecto

### 1. Directorio Raíz
```
/proyecto Jaime/
├── logo-Jaime.png                    # Original
├── logo-Jaime-circular-512.png
├── logo-Jaime-circular-256.png
├── logo-Jaime-circular-128.png
├── logo-Jaime-circular-80.png
└── logo-Jaime-circular-60.png
```

### 2. Paquete Debian - Recursos
```
/proyecto Jaime/debian/usr/share/jaime/
├── logo-Jaime-circular-512.png
├── logo-Jaime-circular-256.png
├── logo-Jaime-circular-128.png
├── logo-Jaime-circular-80.png
└── logo-Jaime-circular-60.png
```

### 3. Paquete Debian - Icono del Sistema
```
/proyecto Jaime/debian/usr/share/pixmaps/
└── jaime.png                         # Copia de logo-Jaime-circular-128.png
```

---

## 🔧 Uso en el Código

### Icono de Ventana (WindowIcon)
**Archivo:** `src/jaime.py` línea 1531

```python
logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'logo-Jaime-circular-128.png')
if not os.path.exists(logo_path):
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            'logo-Jaime.png')

if os.path.exists(logo_path):
    self.setWindowIcon(QIcon(logo_path))
```

**Logo usado:** `logo-Jaime-circular-128.png` (128x128px)
**Fallback:** `logo-Jaime.png`

---

### Logo UI Principal (Barra Superior)
**Archivo:** `src/jaime.py` línea 1638

```python
logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'logo-Jaime-circular-80.png')
if not os.path.exists(logo_path):
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            'logo-Jaime.png')

if os.path.exists(logo_path):
    logo_pixmap = QPixmap(logo_path)
    logo_scaled = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio,
                                     Qt.SmoothTransformation)
    logo_img = QLabel()
    logo_img.setPixmap(logo_scaled)
```

**Logo usado:** `logo-Jaime-circular-80.png` (80x80px)
**Fallback:** `logo-Jaime.png`

---

### Icono de Aplicación Global
**Archivo:** `src/jaime.py` línea 1737

```python
# Configurar icono de la aplicación (circular 128px desde pixmaps)
logo_path = '/usr/share/pixmaps/jaime.png'
if os.path.exists(logo_path):
    app.setWindowIcon(QIcon(logo_path))
else:
    # Fallback a logo local si no está instalado
    local_logo = os.path.join(os.path.dirname(__file__), '..',
                              'logo-Jaime-circular-128.png')
    if os.path.exists(local_logo):
        app.setWindowIcon(QIcon(local_logo))
```

**Logo usado:** `/usr/share/pixmaps/jaime.png` (instalado)
**Fallback:** `logo-Jaime-circular-128.png` (local)

---

## 🛠️ Scripts Disponibles

### 1. Generar Logos Circulares
**Archivo:** `convert_logo_circular.py`

```bash
python3 convert_logo_circular.py
```

**Funciones:**
- ✅ Convierte `logo-Jaime.png` a formato circular
- ✅ Genera 5 tamaños diferentes (60, 80, 128, 256, 512px)
- ✅ Aplica transparencia y anti-aliasing
- ✅ Optimiza tamaño de archivo
- ✅ Copia automáticamente a `debian/usr/share/pixmaps/jaime.png`

**Dependencias:**
- Python 3.x
- Pillow (PIL)

---

### 2. Test Visual de Logos
**Archivo:** `test_logos_visual.py`

```bash
python3 test_logos_visual.py
```

**Funciones:**
- ✅ Muestra todos los logos en una ventana
- ✅ Verifica que existan los archivos
- ✅ Muestra información de cada logo (tamaño, dimensiones, etc.)
- ✅ Interfaz visual para validación rápida

**Dependencias:**
- Python 3.x
- PyQt5

---

## 📦 Empaquetado Debian

Al construir el paquete `.deb`, los logos se instalan en:

```
/usr/share/jaime/
├── logo-Jaime-circular-512.png
├── logo-Jaime-circular-256.png
├── logo-Jaime-circular-128.png
├── logo-Jaime-circular-80.png
└── logo-Jaime-circular-60.png

/usr/share/pixmaps/
└── jaime.png (128x128px, icono del sistema)
```

---

## 🎯 Recomendaciones de Uso

| Contexto | Logo Recomendado | Dimensiones |
|----------|-----------------|-------------|
| Icono de aplicación (escritorio) | `jaime.png` | 128x128px |
| Ventana principal | `logo-Jaime-circular-128.png` | 128x128px |
| Barra superior UI | `logo-Jaime-circular-80.png` | 80x80px |
| Elementos pequeños | `logo-Jaime-circular-60.png` | 60x60px |
| Documentación web | `logo-Jaime-circular-256.png` | 256x256px |
| Marketing/Impresión | `logo-Jaime-circular-512.png` | 512x512px |

---

## 🔄 Actualizar Logos

Si necesitas regenerar los logos circulares desde el original:

1. **Actualizar logo original** (opcional):
   ```bash
   # Reemplaza logo-Jaime.png con tu nuevo logo
   # Debe ser cuadrado (1024x1024px recomendado)
   ```

2. **Regenerar logos circulares**:
   ```bash
   python3 convert_logo_circular.py
   ```

3. **Verificar visualmente**:
   ```bash
   python3 test_logos_visual.py
   ```

4. **Sincronizar con debian**:
   ```bash
   # Los logos ya se copian automáticamente con convert_logo_circular.py
   # Pero si necesitas hacerlo manual:
   cp logo-Jaime-circular-*.png debian/usr/share/jaime/
   cp logo-Jaime-circular-128.png debian/usr/share/pixmaps/jaime.png
   ```

---

## ✅ Checklist de Verificación

- [x] Logo original presente (logo-Jaime.png)
- [x] 5 logos circulares generados
- [x] Transparencia correcta en todos los logos
- [x] Logos copiados a debian/usr/share/jaime/
- [x] Icono del sistema en debian/usr/share/pixmaps/
- [x] Referencias correctas en src/jaime.py
- [x] Fallbacks configurados correctamente
- [x] Script de conversión funcional
- [x] Script de test visual creado

---

## 📝 Notas Técnicas

### Formato del Logo
- **Tipo:** PNG con canal alpha (RGBA)
- **Forma:** Circular con fondo transparente
- **Anti-aliasing:** Sí, filtro SMOOTH aplicado
- **Optimización:** Activada para reducir tamaño de archivo

### Compatibilidad
- **PyQt5:** ✅ Compatible
- **X11/Wayland:** ✅ Transparencia soportada
- **Gestores de ventanas:** ✅ Probado en GNOME, KDE, XFCE

### Rendimiento
- Tamaños optimizados para carga rápida
- Uso de cache de PyQt5 para mejor rendimiento
- Escalado con Qt.SmoothTransformation para calidad óptima

---

## 📧 Soporte

Para reportar problemas con los logos:
1. Verificar que todos los archivos existan
2. Ejecutar `python3 test_logos_visual.py` para validación visual
3. Revisar permisos de archivos
4. Regenerar con `python3 convert_logo_circular.py` si es necesario

---

**Última actualización:** 20 de octubre de 2025
**Versión de Jaime System Care:** 1.3.0
