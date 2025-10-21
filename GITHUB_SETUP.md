# Guía para Subir Jaime System Cleaner a GitHub

## Preparar el Repositorio Local

### 1. Inicializar Git en el proyecto

```bash
cd "/home/seba/Escritorio/proyecto Jaime"
git init
```

### 2. Configurar Git (si no lo has hecho)

```bash
git config --global user.name "Sebastian Scuadroni"
git config --global user.email "tu-email@ejemplo.com"
```

### 3. Añadir todos los archivos

```bash
git add .
```

### 4. Crear el primer commit

```bash
git commit -m "Initial commit: Jaime System Cleaner v1.0.0

- Implementada interfaz gráfica completa con PyQt5
- Módulo Health Check del sistema
- Módulo Custom Clean con limpieza personalizada
- Módulo Driver Update
- Módulo System Update
- Panel de Tools con herramientas útiles
- Panel de Settings
- Empaquetado .deb para fácil instalación
- Documentación completa

Autor: Sebastian Scuadroni / Amanda Software
Licencia: MIT"
```

## Subir a GitHub

### Opción A: Crear repositorio desde GitHub.com

1. Ve a https://github.com/new
2. Nombre del repositorio: `jaime-system-cleaner`
3. Descripción: "Herramienta de limpieza y mantenimiento para Linux - CCleaner alternativo"
4. Selecciona "Public" o "Private"
5. NO marques "Initialize this repository with a README" (ya tienes uno)
6. Haz clic en "Create repository"

### Opción B: Crear repositorio desde la terminal (requiere GitHub CLI)

```bash
gh repo create jaime-system-cleaner --public --source=. --remote=origin
```

### 7. Conectar con el repositorio remoto

```bash
git remote add origin https://github.com/TU_USUARIO/jaime-system-cleaner.git
```

### 8. Verificar la conexión

```bash
git remote -v
```

### 9. Hacer push al repositorio

```bash
git branch -M main
git push -u origin main
```

## Añadir una Descripción Atractiva

En GitHub, añade estos topics (temas) al repositorio:

- `linux`
- `cleaner`
- `system-tools`
- `debian`
- `ubuntu`
- `pyqt5`
- `system-maintenance`
- `ccleaner-alternative`

## Crear Releases

### 1. Primero, crea el paquete .deb

```bash
./build.sh
```

### 2. Crear un release en GitHub

```bash
gh release create v1.0.0 jaime-cleaner_1.0.0_all.deb \
  --title "Jaime System Cleaner v1.0.0" \
  --notes "Primera versión estable de Jaime System Cleaner

Características:
- Health Check completo del sistema
- Limpieza personalizada
- Actualización de drivers
- Actualización del sistema
- Herramientas de mantenimiento
- Interfaz gráfica intuitiva

Instalación:
\`\`\`bash
sudo dpkg -i jaime-cleaner_1.0.0_all.deb
sudo apt-get install -f
\`\`\`"
```

O manualmente:
1. Ve a tu repositorio en GitHub
2. Click en "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Título: `Jaime System Cleaner v1.0.0`
5. Sube el archivo `jaime-cleaner_1.0.0_all.deb`
6. Añade las notas del release
7. Publica el release

## Estructura Final del README en GitHub

Tu README.md ya está optimizado para GitHub y mostrará:

- Logo (si logo-Jaime.png está en el repositorio)
- Badges automáticos
- Tabla de contenidos
- Instrucciones de instalación
- Características
- Capturas de pantalla (puedes añadirlas después)

## Añadir Badges (Opcional)

Puedes añadir al inicio del README.md:

```markdown
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.6+-yellow)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)
```

## Comandos Útiles para Futuras Actualizaciones

```bash
# Ver estado
git status

# Añadir cambios
git add .

# Commit
git commit -m "Descripción de los cambios"

# Push
git push origin main

# Crear nueva rama
git checkout -b feature/nueva-funcionalidad

# Ver historial
git log --oneline

# Ver diferencias
git diff
```

## Archivo .gitignore

Ya está incluido y evita subir:
- Archivos .deb compilados
- Cache de Python
- Archivos temporales
- Configuraciones de IDEs

## Colaboración

Para aceptar contribuciones:

1. Activa Issues en tu repositorio
2. Considera añadir un archivo `CONTRIBUTING.md`
3. Activa GitHub Actions para CI/CD (opcional)

## Promoción

Comparte tu proyecto:

- Reddit: r/linux, r/linuxquestions, r/opensource
- Twitter/X con hashtags: #Linux #OpenSource #SystemTools
- LinuxToday, OMG! Ubuntu, etc.

---

**¡Tu proyecto está listo para el mundo!**

Autor: Sebastian Scuadroni / Amanda Software
