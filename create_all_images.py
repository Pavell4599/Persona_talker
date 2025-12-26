"""
Скрипт для создания placeholder изображений для ВСЕХ персонажей
"""
import os
import sys
import django
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

# Настройка Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'persona_talker'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'persona_talker.settings')
django.setup()

from style_rewriter.models import Persona
from django.core.files import File

# Цвета для фона
COLORS = [
    (102, 126, 234),  # Синий
    (118, 75, 162),   # Фиолетовый
    (237, 100, 166),  # Розовый
    (255, 159, 64),   # Оранжевый
    (75, 192, 192),   # Бирюзовый
    (153, 102, 255), # Фиолетовый 2
    (255, 99, 132),  # Красный
    (54, 162, 235),  # Голубой
    (255, 206, 86),  # Желтый
    (255, 159, 64),  # Оранжевый 2
]

def create_placeholder_image(persona_name, output_path, size=(400, 400)):
    """Создает placeholder изображение с именем персонажа"""
    # Выбираем случайный цвет
    bg_color = random.choice(COLORS)
    
    # Создаем изображение
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Пытаемся использовать системный шрифт
    try:
        # Windows
        font_path = "C:/Windows/Fonts/arial.ttf"
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 40)
        else:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Разбиваем имя на строки
    words = persona_name.split()
    lines = []
    current_line = []
    current_width = 0
    
    for word in words:
        word_width = len(word) * 20
        if current_width + word_width > size[0] - 40:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                lines.append(word)
                current_width = 0
        else:
            current_line.append(word)
            current_width += word_width + 20
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Вычисляем позицию для текста
    total_height = len(lines) * 50
    start_y = (size[1] - total_height) // 2
    
    # Рисуем текст
    for i, line in enumerate(lines):
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            # Fallback для старых версий PIL
            text_width = len(line) * 20
            text_height = 40
        
        x = (size[0] - text_width) // 2
        y = start_y + i * 50
        
        # Рисуем текст с обводкой
        draw.text((x-1, y-1), line, fill=(0, 0, 0, 128), font=font)
        draw.text((x+1, y-1), line, fill=(0, 0, 0, 128), font=font)
        draw.text((x-1, y+1), line, fill=(0, 0, 0, 128), font=font)
        draw.text((x+1, y+1), line, fill=(0, 0, 0, 128), font=font)
        draw.text((x, y), line, fill=(255, 255, 255), font=font)
    
    # Сохраняем изображение
    img.save(output_path, 'PNG')
    return output_path

def main():
    print('=' * 60)
    print('Создание изображений для ВСЕХ персонажей')
    print('=' * 60)
    
    # Путь к папке photos
    photos_dir = Path(__file__).parent / 'photos'
    photos_dir.mkdir(exist_ok=True)
    
    # Получаем ВСЕХ системных персонажей
    personas = Persona.objects.filter(user=None)
    
    if not personas.exists():
        print('\nПерсонажи не найдены!')
        return
    
    print(f'\nСоздание изображений для {personas.count()} персонажей...\n')
    
    created_count = 0
    updated_count = 0
    error_count = 0
    
    for persona in personas:
        try:
            # Создаем безопасное имя файла
            safe_name = persona.name.replace(' ', '_').replace('(', '').replace(')', '').replace('\'', '').replace('/', '_')
            filename = f"{safe_name}.png"
            filepath = photos_dir / filename
            
            # Создаем placeholder изображение
            create_placeholder_image(persona.name, filepath)
            
            # Удаляем старое изображение, если есть
            if persona.image:
                try:
                    persona.image.delete(save=False)
                except:
                    pass
            
            # Присваиваем новое изображение персоне
            with open(filepath, 'rb') as f:
                persona.image.save(filename, File(f), save=True)
            
            if persona.image:
                updated_count += 1
                try:
                    print(f'[+] Обновлено изображение для: {persona.name}')
                except:
                    print(f'[+] Обновлено изображение')
            else:
                created_count += 1
                try:
                    print(f'[+] Создано изображение для: {persona.name}')
                except:
                    print(f'[+] Создано изображение')
            
        except Exception as e:
            error_count += 1
            try:
                print(f'[!] Ошибка: {str(e)}')
            except:
                print(f'[!] Ошибка при создании изображения')
    
    print(f'\n{"=" * 60}')
    print(f'Готово! Создано: {created_count}, обновлено: {updated_count}, ошибок: {error_count}')
    print(f'{"=" * 60}')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nПрервано пользователем')
    except Exception as e:
        print(f'\n\nКритическая ошибка: {str(e)}')
        import traceback
        traceback.print_exc()

