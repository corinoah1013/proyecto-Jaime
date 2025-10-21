#!/bin/bash

# Script para construir el paquete .deb de Jaime System Cleaner

echo "=== Construyendo Jaime System Cleaner ==="

# Limpiar build anterior si existe
rm -f jaime-cleaner_1.0.0_all.deb

# Copiar archivos al directorio de build
echo "Copiando archivos..."

# Copiar el script principal
cp src/jaime.py debian/usr/share/jaime/jaime.py

# Crear el wrapper ejecutable
cat > debian/usr/bin/jaime << 'EOF'
#!/bin/bash
python3 /usr/share/jaime/jaime.py "$@"
EOF

# Copiar el logo
if [ -f "logo-Jaime.png" ]; then
    cp logo-Jaime.png debian/usr/share/pixmaps/jaime.png
    echo "Logo copiado"
else
    echo "ADVERTENCIA: logo-Jaime.png no encontrado"
fi

# Dar permisos de ejecución a los scripts
chmod +x debian/usr/bin/jaime
chmod +x debian/DEBIAN/postinst
chmod +x debian/DEBIAN/prerm

# Construir el paquete .deb
echo "Construyendo paquete .deb..."
dpkg-deb --build debian jaime-cleaner_1.0.0_all.deb

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Paquete creado exitosamente: jaime-cleaner_1.0.0_all.deb"
    echo ""
    echo "Para instalar, ejecuta:"
    echo "  sudo dpkg -i jaime-cleaner_1.0.0_all.deb"
    echo "  sudo apt-get install -f  # Para instalar dependencias si falta alguna"
    echo ""
    echo "Para desinstalar:"
    echo "  sudo apt remove jaime-cleaner"
else
    echo "❌ Error al construir el paquete"
    exit 1
fi
