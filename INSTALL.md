# Guía de Instalación - Jaime System Cleaner

## Instalación Rápida

### Opción 1: Construir e Instalar (Recomendado)

```bash
cd "/home/seba/Escritorio/proyecto Jaime"
./build.sh
sudo dpkg -i jaime-cleaner_1.0.0_all.deb
sudo apt-get install -f
```

### Opción 2: Instalar Dependencias y Ejecutar Directamente

```bash
# Instalar dependencias
sudo apt install python3 python3-pyqt5 python3-psutil policykit-1

# Ejecutar la aplicación
cd "/home/seba/Escritorio/proyecto Jaime"
python3 src/jaime.py
```

## Verificar Instalación

Después de instalar el paquete .deb, puedes ejecutar:

```bash
jaime
```

O buscar "Jaime System Cleaner" en el menú de aplicaciones de tu sistema.

## Dependencias Necesarias

- **python3**: Python 3.6 o superior
- **python3-pyqt5**: Framework de interfaz gráfica
- **python3-psutil**: Librería para información del sistema
- **policykit-1**: Para operaciones administrativas

### Instalar Dependencias en Ubuntu/Debian/Zorin OS

```bash
sudo apt update
sudo apt install python3 python3-pyqt5 python3-psutil policykit-1
```

### Instalar Dependencias en Linux Mint

```bash
sudo apt update
sudo apt install python3 python3-pyqt5 python3-psutil policykit-1
```

## Desinstalación

```bash
sudo apt remove jaime-cleaner
```

## Solución de Problemas

### Error: "No se encontró el comando jaime"

Verifica que el paquete esté instalado:
```bash
dpkg -l | grep jaime
```

Si no está instalado, instala el paquete .deb nuevamente.

### Error: "Dependencias no satisfechas"

Ejecuta:
```bash
sudo apt-get install -f
```

Esto instalará automáticamente las dependencias faltantes.

### Error al ejecutar: "ModuleNotFoundError: No module named 'PyQt5'"

Instala PyQt5:
```bash
sudo apt install python3-pyqt5
```

### La aplicación no abre

Ejecuta desde terminal para ver los errores:
```bash
python3 /usr/share/jaime/jaime.py
```

O si no está instalado:
```bash
python3 src/jaime.py
```

## Desarrollo

Para desarrollar o modificar Jaime:

1. Edita el archivo `src/jaime.py`
2. Prueba los cambios ejecutando:
   ```bash
   python3 src/jaime.py
   ```
3. Cuando estés satisfecho, reconstruye el paquete:
   ```bash
   ./build.sh
   ```

## Notas

- Se requieren permisos de administrador para algunas operaciones de limpieza
- La aplicación usa `pkexec` para solicitar permisos de forma segura
- Algunas operaciones pueden tardar varios segundos

---

**Autor:** Sebastian Scuadroni / Amanda Software
**Versión:** 1.0.0
