# Jaime System Care v1.3.0 - Documentación Completa

## 📦 Información del Paquete

**Nombre:** jaime-cleaner_1.3.0_all.deb
**Versión:** 1.3.0
**Nombre Oficial:** Jaime System Care
**Arquitectura:** all (independiente de arquitectura)
**Tamaño:** ~1.8 MB

---

## 🆕 Novedades de la Versión 1.3

### Cambios Visuales y de Marca
✅ **Nuevo Nombre:** "Jaime System Care" (antes "Jaime System Cleaner")
✅ **Logo Rediseñado:** Logo circular con diseño moderno
✅ **Interfaz Mejorada:** Botones de navegación optimizados para pantallas pequeñas

### Funcionalidades Nuevas
✅ **Panel de Backup:** Nueva sección 💾 Backup con dos métodos:
   - **Backup del Sistema:** Integración con Timeshift para snapshots completos
   - **Backup de HOME:** Sincronización con rsync para respaldo de datos de usuario

### Mejoras Técnicas
✅ **Diseño Responsivo:** Botones ajustados para ventanas minimizadas (800x500)
✅ **Optimización de Espacios:** Padding y fuentes reducidos para mejor visualización
✅ **8 Paneles Activos:** Todos los paneles funcionando correctamente

---

## 🎯 Características Principales

### Panel de Backup (NUEVO)
El nuevo panel de Backup ofrece dos opciones de respaldo:

#### 1. Backup del Sistema (Timeshift)
- Crea snapshots completos del sistema
- Permite restauración total en caso de fallos
- Verifica automáticamente si Timeshift está instalado
- Muestra progreso en tiempo real

#### 2. Backup de HOME (rsync)
- Sincroniza carpeta HOME a ubicación de respaldo
- Preserva permisos y atributos de archivos
- Respaldo incremental eficiente
- Ideal para datos personales y documentos

### Otros Paneles Disponibles
1. **🏥 Health Check** - Análisis completo del sistema
2. **🧹 Custom Clean** - Limpieza personalizada
3. **🔄 System Update** - Actualización del sistema
4. **🛠️ Tools** - Herramientas de mantenimiento
5. **💾 Backup** - Sistema de respaldos (NUEVO)
6. **🌐 Language** - Selector de idioma (9 idiomas)
7. **ℹ️ About** - Información de la aplicación
8. **⚙️ Settings** - Configuración y hardware info

---

## 🌍 Idiomas Soportados

1. **Español (ES)** - Idioma por defecto
2. **English (EN)** - Inglés
3. **Português (PT)** - Portugués
4. **Français (FR)** - Francés
5. **Italiano (IT)** - Italiano
6. **Deutsch (DE)** - Alemán
7. **Русский (RU)** - Ruso
8. **العربية (AR)** - Árabe
9. **Română (RO)** - Rumano

---

## 📋 Requisitos del Sistema

### Sistema Operativo
- Ubuntu 20.04 o superior
- Debian 10 o superior
- Linux Mint 20 o superior
- Zorin OS 16 o superior
- Pop!_OS 20.04 o superior
- Cualquier distribución basada en Debian/Ubuntu

### Dependencias Obligatorias
- `python3` (3.6 o superior)
- `python3-pyqt5`
- `python3-psutil`
- `policykit-1`

### Dependencias Opcionales (para Backup)
- `timeshift` - Para backups del sistema
- `rsync` - Para backups de HOME (generalmente preinstalado)

---

## 🚀 Instalación

### Instalación Automática de Dependencias Opcionales

Para instalar Timeshift (recomendado para backup del sistema):
```bash
sudo apt update
sudo apt install timeshift
```

### Paso 1: Navegar al directorio
```bash
cd "/home/seba/Escritorio/Jaime-cleaner/proyecto Jaime"
```

### Paso 2: Instalar el paquete
```bash
sudo dpkg -i jaime-cleaner_1.3.0_all.deb
```

### Paso 3: Resolver dependencias (si es necesario)
```bash
sudo apt-get install -f
```

### Paso 4: Ejecutar la aplicación
```bash
jaime
```

O búscala en el menú de aplicaciones como "Jaime System Care"

---

## 💾 Uso del Panel de Backup

### Realizar Backup del Sistema (Timeshift)

1. Abrir Jaime System Care
2. Click en **💾 Backup**
3. Marcar checkbox **☑ System (Timeshift)**
4. Click en **"Verify Timeshift"** para verificar instalación
5. Click en **"Create Backup"**
6. Ingresar contraseña cuando se solicite
7. Esperar a que se complete el snapshot

**Notas:**
- Requiere Timeshift instalado
- Necesita permisos de administrador
- El proceso puede tardar varios minutos
- Se creará un punto de restauración completo

### Realizar Backup de HOME (rsync)

1. Abrir Jaime System Care
2. Click en **💾 Backup**
3. Marcar checkbox **☑ HOME (rsync)**
4. Click en **"Create Backup"**
5. Ingresar contraseña cuando se solicite
6. Esperar a que se complete la sincronización

**Notas:**
- rsync generalmente viene preinstalado
- Crea respaldo en `/backup/home_backup/`
- Preserva todos los permisos y atributos
- Respaldo incremental (solo copia cambios)

### Realizar Backup Completo (Sistema + HOME)

1. Marcar ambos checkboxes: **☑ System** y **☑ HOME**
2. Click en **"Create Backup"**
3. Se ejecutarán ambos respaldos secuencialmente

---

## 🔍 Verificación de la Instalación

### Verificar paquete instalado
```bash
dpkg -l | grep jaime
```

**Salida esperada:**
```
ii  jaime-cleaner  1.3.0  all  Jaime System Care - Sistema de mantenimiento para Linux
```

### Verificar archivos instalados
```bash
dpkg -L jaime-cleaner
```

**Archivos principales:**
- `/usr/bin/jaime` - Ejecutable principal
- `/usr/share/jaime/jaime.py` - Script Python principal
- `/usr/share/jaime/translations.py` - Sistema de traducciones
- `/usr/share/applications/jaime.desktop` - Acceso directo
- `/usr/share/pixmaps/jaime.png` - Logo circular
- `/usr/share/jaime/logo-Jaime-circular-60.png` - Logo 60px
- `/usr/share/jaime/logo-Jaime-circular-80.png` - Logo 80px

### Verificar Timeshift (opcional)
```bash
which timeshift
timeshift --version
```

---

## 🔄 Actualización desde v1.2 o v1.1

Si ya tienes una versión anterior instalada:

```bash
# 1. Instalar la nueva versión (sobrescribirá automáticamente)
cd "/home/seba/Escritorio/Jaime-cleaner/proyecto Jaime"
sudo dpkg -i jaime-cleaner_1.3.0_all.deb

# 2. Resolver dependencias si es necesario
sudo apt-get install -f

# 3. Verificar versión instalada
jaime --version 2>/dev/null || dpkg -l | grep jaime
```

**Nota:** No es necesario desinstalar la versión anterior.

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

### Verificar eliminación
```bash
dpkg -l | grep jaime
```

---

## 🛠️ Solución de Problemas

### Problema: "Timeshift no está instalado"

**Síntoma:** Al intentar crear backup del sistema aparece error

**Solución:**
```bash
# Instalar Timeshift
sudo apt update
sudo apt install timeshift

# Verificar instalación
which timeshift

# Reintentar backup desde Jaime
```

---

### Problema: "Error al crear backup de HOME"

**Síntoma:** El backup de HOME falla o no se completa

**Solución:**
```bash
# Verificar que rsync está instalado
which rsync

# Si no está instalado
sudo apt install rsync

# Verificar permisos del directorio de backup
ls -ld /backup/
sudo mkdir -p /backup/home_backup
sudo chown $USER:$USER /backup/home_backup

# Reintentar backup
```

---

### Problema: "Botones solapados en ventana pequeña"

**Síntoma:** Los botones de navegación se superponen cuando la ventana está minimizada

**Solución:**
Este problema fue corregido en v1.3.0. Si persiste:
- Maximiza la ventana
- Actualiza a la última versión
- Verifica que estás ejecutando v1.3.0: `dpkg -l | grep jaime`

---

### Problema: "La aplicación no arranca"

**Solución:**
```bash
# Ejecutar desde terminal para ver errores
jaime

# Verificar dependencias
dpkg -l | grep -E "(python3-pyqt5|python3-psutil)"

# Reinstalar dependencias
sudo apt-get install --reinstall python3-pyqt5 python3-psutil policykit-1

# Reinstalar Jaime
sudo dpkg -i jaime-cleaner_1.3.0_all.deb
sudo apt-get install -f
```

---

## 🎯 Guía de Uso Rápido

### Primera Ejecución

1. **Ejecutar Jaime:**
   ```bash
   jaime
   ```

2. **Cambiar idioma (opcional):**
   - Click en **🌐 Language**
   - Seleccionar idioma preferido

3. **Realizar Health Check:**
   - Click en **🏥 Health Check**
   - Marcar todos los análisis
   - Click en "Iniciar Análisis"

4. **Configurar Backup:**
   - Click en **💾 Backup**
   - Click en "Verify Timeshift"
   - Si no está instalado: `sudo apt install timeshift`

### Uso Regular Recomendado

**Diariamente:**
- 🏥 Health Check rápido

**Semanalmente:**
- 🧹 Custom Clean
- 💾 Backup de HOME

**Mensualmente:**
- 🔄 System Update
- 💾 Backup completo (Sistema + HOME)
- 🛠️ Tools - Reparar paquetes rotos

---

## 💡 Consejos y Mejores Prácticas

### Backup
- **Frecuencia:** Realiza backups de HOME semanalmente y del sistema mensualmente
- **Espacio:** Verifica que tengas espacio suficiente antes de crear backups
- **Timeshift:** Configura Timeshift para crear snapshots automáticos
- **Verificación:** Prueba restaurar un backup para verificar que funciona

### Rendimiento
- **Limpieza regular:** Ejecuta Custom Clean semanalmente
- **Caché:** Limpia caché de navegadores y aplicaciones regularmente
- **Logs:** Mantén logs bajo control

### Seguridad
- **Actualizaciones:** Mantén el sistema actualizado con System Update
- **Privilegios:** Jaime pedirá contraseña solo cuando sea necesario
- **Permisos:** Usa pkexec para operaciones seguras

---

## 📊 Arquitectura del Sistema

### Estructura de Archivos
```
/usr/
├── bin/
│   └── jaime                          # Ejecutable principal
├── share/
│   ├── applications/
│   │   └── jaime.desktop             # Launcher
│   ├── pixmaps/
│   │   └── jaime.png                 # Icono principal
│   └── jaime/
│       ├── jaime.py                  # Script principal
│       ├── translations.py           # Sistema de i18n
│       ├── logo-Jaime-circular-60.png
│       └── logo-Jaime-circular-80.png
```

### Componentes Principales

**JaimeWindow (Clase Principal)**
- Gestión de ventana principal
- Sistema de navegación con 8 botones
- QStackedWidget para paneles

**BackupPanel (Nuevo en v1.3)**
- Integración con Timeshift
- Integración con rsync
- Verificación de dependencias
- Ejecución de comandos con privilegios

**TranslationManager**
- Gestión de 9 idiomas
- Traducciones en tiempo real
- Persistencia de preferencias

---

## 🔐 Seguridad y Privacidad

### Seguridad del Código
- ✅ Código fuente visible en `/usr/share/jaime/jaime.py`
- ✅ Sin ofuscación ni código malicioso
- ✅ Usa `pkexec` para elevación segura de privilegios
- ✅ No se conecta a internet
- ✅ No recopila datos del usuario

### Privacidad
- ✅ No guarda contraseñas
- ✅ No envía telemetría
- ✅ No accede a archivos personales sin permiso
- ✅ Backups locales únicamente

### Permisos
- Jaime solo requiere permisos de administrador para:
  - Limpieza de caché del sistema
  - Actualización de paquetes
  - Creación de backups del sistema
  - Reparación de paquetes

---

## 📞 Información de Contacto

**Desarrollador:** Sebastian Scuadroni
**Empresa:** Amanda Software
**Versión:** 1.3.0
**Nombre:** Jaime System Care
**Licencia:** MIT
**Año:** 2025

---

## 📝 Changelog Completo

### v1.3.0 (Actual - 2025)
**Cambios de Marca:**
- ✅ Renombrado a "Jaime System Care"
- ✅ Logo circular rediseñado (60px y 80px)
- ✅ Identidad visual actualizada

**Nuevas Funcionalidades:**
- ✅ Panel de Backup completo
- ✅ Integración con Timeshift para backups del sistema
- ✅ Integración con rsync para backups de HOME
- ✅ Verificación automática de dependencias
- ✅ Progreso en tiempo real de operaciones

**Mejoras de UI:**
- ✅ Botones de navegación optimizados (8px 12px padding)
- ✅ Fuente reducida a 11px para mejor ajuste
- ✅ Border-radius reducido a 12px
- ✅ Diseño responsivo mejorado para ventanas pequeñas

**Traducciones:**
- ✅ Añadida traducción de 'nav_backup' en 9 idiomas

### v1.2.0
- ✅ Añadidos 3 idiomas nuevos (Italiano, Alemán, Ruso)
- ✅ Soporte para 9 idiomas total
- ✅ Panel Settings mejorado
- ✅ Información de hardware detallada

### v1.1.0
- ✅ Panel de selección de idiomas (4 idiomas)
- ✅ Sistema de scroll en todos los paneles
- ✅ Interfaz responsive para pantallas pequeñas
- ✅ Barra superior simplificada
- ✅ Info de hardware en Settings

### v1.0.0
- Versión inicial
- 6 paneles funcionales
- Limpieza y mantenimiento básico

---

## 🎓 Casos de Uso

### Caso 1: Usuario Doméstico
**Perfil:** Usuario que usa Linux para tareas cotidianas

**Flujo de trabajo:**
1. Instalar Jaime System Care
2. Ejecutar Health Check al iniciar la semana
3. Limpieza semanal con Custom Clean
4. Backup de HOME los viernes
5. System Update mensual

**Beneficios:**
- Sistema siempre limpio y optimizado
- Datos personales respaldados
- Mantenimiento preventivo

---

### Caso 2: Desarrollador
**Perfil:** Programador que necesita ambiente estable

**Flujo de trabajo:**
1. Backup del sistema antes de cambios importantes
2. Limpieza de caché de compiladores
3. Health Check después de instalar dependencias
4. Backup de HOME con proyectos importantes
5. Tools para reparar dependencias rotas

**Beneficios:**
- Rollback rápido con Timeshift
- Ambiente de desarrollo limpio
- Recuperación de código en caso de fallo

---

### Caso 3: Administrador de Sistemas
**Perfil:** Administrador de múltiples equipos Linux

**Flujo de trabajo:**
1. Instalación en múltiples equipos
2. Configurar backups automáticos con Timeshift
3. Limpieza programada con Custom Clean
4. Monitoreo con Health Check
5. Actualizaciones controladas con System Update

**Beneficios:**
- Mantenimiento centralizado
- Backups consistentes
- Reducción de tickets de soporte

---

## 🚀 Roadmap Futuro

### v1.4.0 (Próxima versión)
- [ ] Checkbox "Iniciar con el sistema"
- [ ] Traducciones en Japonés (10 idiomas total)
- [ ] Configuración avanzada de backups
- [ ] Programación de tareas automáticas
- [ ] Notificaciones de sistema

### v1.5.0 (Planeada)
- [ ] Panel de estadísticas y gráficos
- [ ] Historial de limpiezas
- [ ] Comparación de backups
- [ ] Temas personalizables

---

## 📚 Recursos Adicionales

### Documentación
- `README.md` - Documentación principal del proyecto
- `INSTALL.md` - Guía de instalación
- `QUICKSTART.md` - Inicio rápido
- `GITHUB_SETUP.md` - Configuración para GitHub

### Comandos Útiles
```bash
# Ver logs de Jaime
journalctl -xe | grep jaime

# Información del paquete
apt show jaime-cleaner

# Archivos modificados
dpkg -V jaime-cleaner

# Reinstalar desde cero
sudo apt purge jaime-cleaner
sudo dpkg -i jaime-cleaner_1.3.0_all.deb
sudo apt-get install -f
```

---

## ⚠️ Advertencias Importantes

1. **Backups del Sistema:** Requieren espacio significativo. Verifica tener al menos 20GB libres.

2. **Timeshift:** Primera ejecución puede tardar mucho tiempo. Sé paciente.

3. **Permisos de Administrador:** Jaime pedirá contraseña. Esto es normal y necesario.

4. **Backup de HOME:** No incluye archivos temporales ni caché por defecto.

5. **Restauración:** Para restaurar backups de Timeshift, usa `sudo timeshift-gtk` o `sudo timeshift --restore`.

---

## 🎉 Conclusión

Jaime System Care v1.3.0 representa una evolución significativa de la herramienta, incorporando un sistema robusto de backups que complementa perfectamente las funciones de limpieza y mantenimiento existentes. Con el nuevo panel de Backup, los usuarios pueden proteger tanto su sistema completo como sus datos personales de manera fácil y eficiente.

La integración con Timeshift y rsync proporciona soluciones profesionales de respaldo sin la complejidad de configuración manual, manteniendo la filosofía de Jaime: "Mantenimiento potente, interfaz simple."

**¡Gracias por usar Jaime System Care!**

---

**Documento generado:** 2025-01-17
**Versión del documento:** 1.0
**Aplicación:** Jaime System Care v1.3.0
