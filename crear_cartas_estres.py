import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Cargar los datos desde el archivo CSV
df = pd.read_csv('elementos_estres.csv')

# Configuración de la carta incluyendo el área de sangrado (bleeding area)
bleed = 9  # 9 pixels for 3mm bleeding at 33 DPI
width, height = 447 + 2 * bleed, 597 + 2 * bleed  # Añadir área de sangrado a ambos lados
inner_width, inner_height = 447, 597  # Tamaño real del diseño sin sangrado
dpi = 33
max_text_width = int((inner_width - 60) * 0.9 * 0.9)  # Further reducing the max text width by 10%

# Cargar una fuente para el texto y reducir el tamaño de la fuente en un 10%
font_path = "C:/Windows/Fonts/DejaVuSans-Bold.ttf"
font_large = ImageFont.truetype(font_path, int(30 * 0.9 * 0.9))  # 10% smaller from the last size
font_medium = ImageFont.truetype(font_path, int(24 * 0.9 * 0.9) - 2)  # 2 points smaller
font_small = ImageFont.truetype(font_path, int(18 * 0.9 * 0.9) - 2)  # 2 points smaller

# Colores de fondo según la dimensión (11 colores diferentes con mayor variación)
background_colors = [
    (139, 69, 19),   # Darker Brown for Dimension 1
    (205, 92, 92),   # Lighter Brown for Dimension 2
    (165, 42, 42),   # Darker Red for Dimension 3
    (244, 164, 96),  # Light Ocre for Dimension 4
    (210, 105, 30),  # Chocolate for Dimension 5
    (128, 70, 27),   # Dark Brown for Dimension 6
    (222, 184, 135), # Burlywood for Dimension 7
    (160, 82, 45),   # Sienna for Dimension 8
    (178, 34, 34),   # Firebrick for Dimension 9
    (210, 180, 140), # Tan for Dimension 10
    (255, 127, 80)   # Coral for Dimension 11
]

# Función para centrar y ajustar el texto dentro de un área específica
def draw_text_centered(draw, text, position_y, font, max_width):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and draw.textlength(line + words[0], font=font) <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    
    y = position_y
    for line in lines:
        # Calcular el ancho del texto para centrarlo
        text_width = draw.textlength(line, font=font)
        position_x = (inner_width - text_width) / 2 + bleed  # Centrar horizontalmente con el área de sangrado
        draw.text((position_x, y), line, font=font, fill=(0, 0, 0))
        y += draw.textbbox((0, 0), line, font=font)[3]  # Ajustar la posición Y para la siguiente línea

# Crear las cartas
for index, row in df.iterrows():
    # Determinar el índice de la dimensión para seleccionar el color de fondo y la imagen
    dimension_index = int(row['Dimensión'].split('.')[0]) - 1  # Convertir la dimensión a un índice basado en 0
    bg_color = background_colors[dimension_index]

    img = Image.new('RGB', (width, height), color=bg_color)  # Fondo incluyendo el área de sangrado

    d = ImageDraw.Draw(img)

    # Ajustar la posición vertical inicial para bajar todo el contenido
    initial_y_offset = bleed + 80  # Más espacio en la parte superior

    # Dibujar los textos centrados en la carta (ajustado con initial_y_offset)
    draw_text_centered(d, row['Elemento'], initial_y_offset, font_large, max_text_width)

    # Cargar la imagen correspondiente a la dimensión
    dim_img_path = f"dim{dimension_index+1:02d}.webp"
    dim_img = Image.open(dim_img_path).convert("RGB")  # Convertir a "RGB" para eliminar la transparencia
    factor = 0.2  # Factor de redimensionamiento
    dim_img = dim_img.resize((int(dim_img.width * factor), int(dim_img.height * factor)))  # Redimensionar

    # Ajustar la posición para dejar menos espacio entre el nombre y la imagen (ajustado con initial_y_offset)
    image_y_position = initial_y_offset + 90  # Further reducing space between the text and image
    img.paste(dim_img, ((width - dim_img.width) // 2, image_y_position))  # Centrar la imagen

    # Dibujar los textos restantes centrados en la carta (ajustado con initial_y_offset)
    draw_text_centered(d, f"Dimensión: {row['Dimensión']}", initial_y_offset + 320, font_medium, max_text_width)
    draw_text_centered(d, f"Subdimensión: {row['Subdimensión']}", initial_y_offset + 365, font_medium, max_text_width)  # Reduced space
    draw_text_centered(d, f"Eje: {row['Eje']}", initial_y_offset + 410, font_small, max_text_width)

    # Guardar la imagen como PNG
    img.save(f"carta_{index+1}.png", dpi=(dpi, dpi))

print("Cartas creadas con éxito.")
