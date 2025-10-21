# Instalación de Jaime System Cleaner v1.1

## 📦 Información del Paquete

**Nombre:** jaime-cleaner_1.0.0_all.deb
**Versión:** 1.1.0 (nombre interno 1.0.0)
**Tamaño:** 1.6 MB
**Arquitectura:** all (independiente de arquitectura)
**MD5:** 57f98595a75289fb9a6b1ca5bfe66f0c

---

## 🆕 Novedades de la Versión 1.1

✅ **Panel de Idiomas:** Selección entre Español, English, Português y Français
✅ **Sistema de Scroll:** Todos los paneles ahora tienen scroll para pantallas pequeñas
✅ **Interfaz Responsive:** Se adapta automáticamente a pantallas de 13.3" y superiores
✅ **Barra Superior Simplificada:** Más espacio para el contenido
✅ **Info de Hardware en Settings:** Información completa del sistema ahora en configuración

---

## 📋 Requisitos del Sistema

### Sistema Operativo
- Ubuntu 20.04 o superior
- Debian 10 o superior
- Linux Mint 20 o superior
- Zorin OS 16 o superior
- Cualquier distribución basada en Debian/Ubuntu

### Dependencias
- `python3` (3.6 o superior)
- `python3-pyqt5`
- `python3-psutil`
- `policykit-1`

---

## 🚀 Instalación Rápida

### Paso 1: Navegar al directorio
```bash
cd "/home/seba/Escritorio/proyecto Jaime"
```

### Paso 2: Instalar el paquete
```bash
sudo dpkg -i jaime-cleaner_1.0.0_all.deb
```

### Paso 3: Resolver dependencias (si es necesario)
```bash
sudo apt-get install -f
```

### Paso 4: Ejecutar la aplicación
```bash
jaime
```

O búscala en el menú de aplicaciones como "Jaime System Cleaner"

---

## 📝 Instalación Detallada

### Opción A: Instalación desde el directorio del proyecto

```bash
# 1. Abrir terminal
Ctrl + Alt + T

# 2. Navegar al proyecto
cd "/home/seba/Escritorio/proyecto Jaime"

# 3. Instalar el paquete
sudo dpkg -i jaime-cleaner_1.0.0_all.deb

# 4. Si hay dependencias faltantes:
sudo apt-get install -f

# 5. Verificar instalación
which jaime

# 6. Ejecutar
jaime
```

---

### Opción B: Instalación con doble clic

1. Abrir el explorador de archivos (Nautilus)
2. Navegar a: `/home/seba/Escritorio/proyecto Jaime`
3. Hacer doble clic en `jaime-cleaner_1.0.0_all.deb`
4. Click en "Instalar"
5. Ingresar contraseña de administrador
6. Esperar a que termine la instalación
7. Buscar "Jaime" en el menú de aplicaciones

---

## 🔍 Verificación de la Instalación

### Verificar que el paquete está instalado
```bash
dpkg -l | grep jaime
```

**Salida esperada:**
```
ii  jaime-cleaner  1.0.0  all  Jaime System Cleaner - CCleaner para Linux
```

### Verificar archivos instalados
```bash
dpkg -L jaime-cleaner
```

**Archivos instalados:**
- `/usr/bin/jaime` - Ejecutable principal
- `/usr/share/jaime/jaime.py` - Script Python
- `/usr/share/applications/jaime.desktop` - Acceso directo
- `/usr/share/pixmaps/jaime.png` - Icono

### Verificar que funciona
```bash
jaime --help 2>/dev/null || echo "Ejecuta: jaime"
```

---

## 🔄 Actualización desde v1.0.0

Si ya tienes la versión 1.0.0 instalada:

```bash
# 1. Desinstalar la versión anterior (opcional)
sudo apt remove jaime-cleaner

# 2. Instalar la nueva versión
cd "/home/seba/Escritorio/proyecto Jaime"
sudo dpkg -i jaime-cleaner_1.0.0_all.deb

# 3. Resolver dependencias
sudo apt-get install -f
```

**Nota:** No es necesario desinstalar la versión anterior, el nuevo paquete la sobrescribirá automáticamente.

---

## ❌ Desinstalación

### Desinstalar el paquete
```bash
sudo apt remove jaime-cleaner
```

### Desinstalar y eliminar configuración
```bash
sudo apt purge jaime-cleaner
```

### Verificar que se eliminó
```bash
dpkg -l | grep jaime
```

---

## 🛠️ Solución de Problemas

### Problema: "dpkg: error de dependencias"

**Solución:**
```bash
sudo apt-get install -f
sudo apt-get install python3-pyqt5 python3-psutil policykit-1
sudo dpkg -i jaime-cleaner_1.0.0_all.deb
```

---

### Problema: "jaime: comando no encontrado"

**Solución:**
```bash
# Verificar si está instalado
dpkg -l | grep jaime

# Si no está instalado, instalar
sudo dpkg -i jaime-cleaner_1.0.0_all.deb

# Recargar el PATH
hash -r

# Intentar ejecutar con ruta completa
/usr/bin/jaime
```

---

### Problema: "No se puede abrir el archivo .deb"

**Solución:**
```bash
# Verificar permisos
ls -l jaime-cleaner_1.0.0_all.deb

# Cambiar permisos si es necesario
chmod 644 jaime-cleaner_1.0.0_all.deb

# Verificar integridad del archivo
md5sum jaime-cleaner_1.0.0_all.deb
# Debe mostrar: 57f98595a75289fb9a6b1ca5bfe66f0c
```

---

### Problema: "La aplicación no se abre"

**Solución:**
```bash
# Ejecutar desde terminal para ver errores
jaime

# Verificar dependencias
dpkg -l | grep -E "(python3-pyqt5|python3-psutil)"

# Reinstalar dependencias
sudo apt-get install --reinstall python3-pyqt5 python3-psutil
```

---

### Problema: "Faltan permisos para ejecutar comandos de limpieza"

**Solución:**
- Esto es normal, la aplicación pedirá contraseña cuando sea necesario
- Usa `pkexec` o `sudo` cuando se solicite
- Verifica que `policykit-1` esté instalado:
```bash
dpkg -l | grep policykit
```

---

## 📊 Información del Paquete

### Contenido del paquete
```bash
dpkg -c jaime-cleaner_1.0.0_all.deb
```

### Información detallada
```bash
dpkg -I jaime-cleaner_1.0.0_all.deb
```

### Scripts de instalación
- **postinst**: Se ejecuta después de instalar
- **prerm**: Se ejecuta antes de desinstalar

---

## 🎯 Primeros Pasos Después de Instalar

1. **Ejecutar Jaime:**
   ```bash
   jaime
   ```

2. **Realizar un Health Check:**
   - Click en "🏥 Health Check"
   - Seleccionar todos los análisis
   - Click en "Iniciar Análisis"

3. **Hacer una limpieza:**
   - Click en "🧹 Custom Clean"
   - Seleccionar elementos a limpiar
   - Click en "Iniciar Limpieza"

4. **Cambiar idioma:**
   - Click en "🌐 Language"
   - Seleccionar tu idioma preferido

5. **Ver información del sistema:**
   - Click en "⚙️ Settings"
   - Ver información de CPU, GPU, RAM y OS

---

## 💡 Consejos

- **Primer uso:** Realiza un Health Check para conocer el estado de tu sistema
- **Limpieza regular:** Ejecuta Custom Clean semanalmente
- **Pantallas pequeñas:** Usa el scroll para ver todo el contenido
- **Actualizaciones:** Mantén el sistema actualizado con System Update
- **Herramientas rápidas:** Usa el panel Tools para reparaciones rápidas

---

## 🔐 Seguridad

- El paquete es seguro y no contiene malware
- El código fuente está disponible en `/usr/share/jaime/jaime.py`
- Usa `pkexec` para elevación segura de privilegios
- No guarda contraseñas ni información sensible

**Verificar integridad:**
```bash
md5sum jaime-cleaner_1.0.0_all.deb
# Debe mostrar: 57f98595a75289fb9a6b1ca5bfe66f0c
```

---

## 📞 Soporte

**Autor:** Sebastian Scuadroni / Amanda Software
**Versión:** 1.1.0
**Licencia:** MIT

---

## 📝 Changelog

### v1.1.0 (Actual)
- ✅ Añadido panel de selección de idiomas
- ✅ Implementado sistema de scroll en todos los paneles
- ✅ Interfaz responsive para pantallas pequeñas (13.3")
- ✅ Barra superior simplificada
- ✅ Información de hardware movida a Settings
- ✅ Tamaño mínimo reducido a 800x500

### v1.0.0
- Versión inicial
- 6 paneles funcionales
- Limpieza y mantenimiento básico

---

**¡Disfruta de Jaime System Cleaner v1.1!**

Para más información, consulta:
- `README.md` - Documentación completa
- `QUICKSTART.md` - Inicio rápido
- `archivos .md/jaimesystem cleaner ver.1.1.md` - Changelog detallado
