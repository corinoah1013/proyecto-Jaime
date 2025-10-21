#!/usr/bin/env python3
"""
Script para convertir el logo de Jaime a formato circular con transparencia
Genera múltiples tamaños optimizados para diferentes usos
"""

from PIL import Image, ImageDraw, ImageFilter
import os

def create_circular_logo(input_path, output_path, size=256, border_width=0):
    """
    Convierte una imagen a formato circular con transparencia

    Args:
        input_path: Ruta de la imagen original
        output_path: Ruta donde guardar la imagen circular
        size: Tamaño final de la imagen (ancho y alto)
        border_width: Ancho del borde circular (0 = sin borde)
    """
    # Abrir imagen original
    img = Image.open(input_path).convert("RGBA")

    # Redimensionar manteniendo aspecto cuadrado (compatible con Pillow 9.x)
    img = img.resize((size, size), Image.LANCZOS)

    # Crear máscara circular
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # Aplicar máscara circular
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)

    # Agregar borde si se especifica
    if border_width > 0:
        draw = ImageDraw.Draw(output)
        draw.ellipse(
            (border_width//2, border_width//2, size - border_width//2, size - border_width//2),
            outline=(255, 255, 255, 255),
            width=border_width
        )

    # Aplicar suavizado anti-aliasing
    output = output.filter(ImageFilter.SMOOTH)

    # Guardar imagen
    output.save(output_path, 'PNG', optimize=True)
    print(f"✓ Logo circular creado: {output_path} ({size}x{size}px)")

    return output

def main():
    # Rutas
    base_dir = "/home/seba/Escritorio/Jaime-cleaner/proyecto Jaime"
    input_logo = os.path.join(base_dir, "logo-Jaime.png")

    # Verificar que existe la imagen original
    if not os.path.exists(input_logo):
        print(f"❌ Error: No se encuentra el logo original en {input_logo}")
        return

    print("🎨 Convirtiendo logo a formato circular...")
    print(f"📂 Archivo original: {input_logo}")
    print()

    # Crear versiones en diferentes tamaños
    sizes = [
        (512, "logo-Jaime-circular-512.png", "Alta resolución"),
        (256, "logo-Jaime-circular-256.png", "Resolución media"),
        (128, "logo-Jaime-circular-128.png", "Iconos de aplicación"),
        (80, "logo-Jaime-circular-80.png", "Interfaz UI (grande)"),
        (60, "logo-Jaime-circular-60.png", "Interfaz UI (actual)"),
    ]

    created_files = []

    for size, filename, description in sizes:
        output_path = os.path.join(base_dir, filename)
        try:
            create_circular_logo(input_logo, output_path, size=size)
            created_files.append((filename, description, size))
        except Exception as e:
            print(f"❌ Error creando {filename}: {str(e)}")

    # Copiar versión principal a ubicaciones del proyecto
    if created_files:
        print()
        print("📋 Resumen de logos creados:")
        print()
        for filename, description, size in created_files:
            print(f"  • {filename}")
            print(f"    └─ {description} ({size}x{size}px)")

        # Copiar versión de 128px al directorio de Debian
        main_logo_128 = os.path.join(base_dir, "logo-Jaime-circular-128.png")
        debian_logo = os.path.join(base_dir, "debian/usr/share/pixmaps/jaime.png")

        if os.path.exists(main_logo_128):
            try:
                import shutil
                os.makedirs(os.path.dirname(debian_logo), exist_ok=True)
                shutil.copy2(main_logo_128, debian_logo)
                print()
                print(f"✓ Logo copiado a: {debian_logo}")
            except Exception as e:
                print(f"⚠ No se pudo copiar al directorio debian: {str(e)}")

        print()
        print("✅ Proceso completado exitosamente!")
        print()
        print("🎯 Recomendaciones de uso:")
        print("  • UI principal (jaime.py): logo-Jaime-circular-80.png (más grande y visible)")
        print("  • Icono de aplicación: logo-Jaime-circular-128.png")
        print("  • Alta calidad: logo-Jaime-circular-512.png")
    else:
        print()
        print("❌ No se pudo crear ningún logo circular.")

if __name__ == "__main__":
    main()
