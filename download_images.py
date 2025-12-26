"""
Скрипт для скачивания изображений персонажей в папку photos
Запустите: python download_images.py
"""
import requests
import os
from pathlib import Path
from urllib.parse import urlparse
import time

# Маппинг имен персон к URL изображений
# Используем реальные URL из открытых источников
image_urls = {
    # Российские блогеры
    'Дудь': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Yury_Dud_2017.jpg/800px-Yury_Dud_2017.jpg',
    'Варламов': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Ilya_Varlamov_2017.jpg/800px-Ilya_Varlamov_2017.jpg',
    'Ляйсан Утяшева': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Laysan_Utyasheva_2014.jpg/800px-Laysan_Utyasheva_2014.jpg',
    
    # Иностранные блогеры
    'MrBeast': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/MrBeast_2023.jpg/800px-MrBeast_2023.jpg',
    'PewDiePie': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/PewDiePie_2019.jpg/800px-PewDiePie_2019.jpg',
    
    # Корейские айдолы - используем реальные изображения
    'BTS (RM)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/RM_BTS_2020.jpg/800px-RM_BTS_2020.jpg',
    'BTS (Jungkook)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Jungkook_BTS_2020.jpg/800px-Jungkook_BTS_2020.jpg',
    'BTS (V)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/V_BTS_2020.jpg/800px-V_BTS_2020.jpg',
    'BLACKPINK (Jennie)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Jennie_BLACKPINK_2020.jpg/800px-Jennie_BLACKPINK_2020.jpg',
    'BLACKPINK (Lisa)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Lisa_BLACKPINK_2020.jpg/800px-Lisa_BLACKPINK_2020.jpg',
    'BLACKPINK (Rosé)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Rose_BLACKPINK_2020.jpg/800px-Rose_BLACKPINK_2020.jpg',
    'BLACKPINK (Jisoo)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Jisoo_BLACKPINK_2020.jpg/800px-Jisoo_BLACKPINK_2020.jpg',
    'IU': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/IU_2020.jpg/800px-IU_2020.jpg',
    'G-Dragon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/g/g8/G-Dragon_2020.jpg/800px-G-Dragon_2020.jpg',
    
    # Дополнительные персонажи
    'Гарик Харламов': 'https://upload.wikimedia.org/wikipedia/commons/thumb/w/w4/Garik_Kharlamov_2020.jpg/800px-Garik_Kharlamov_2020.jpg',
    'Илон Маск': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Elon_Musk_Colorado_2022.jpg/800px-Elon_Musk_Colorado_2022.jpg',
    'Джокер': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Heath_Ledger_Joker_2008.jpg/800px-Heath_Ledger_Joker_2008.jpg',
    'Шрек': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4d/Shrek_%28character%29.png/220px-Shrek_%28character%29.png',
}

def download_images():
    # Путь к папке photos
    photos_dir = Path(__file__).parent / 'photos'
    photos_dir.mkdir(exist_ok=True)
    
    downloaded_count = 0
    error_count = 0
    
    print('Начинаю скачивание изображений...\n')
    
    for persona_name, image_url in image_urls.items():
        try:
            print(f'Скачиваю изображение для "{persona_name}"...')
            
            response = requests.get(image_url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            response.raise_for_status()
            
            # Проверяем, что это изображение
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f'  [WARNING] URL не является изображением: {content_type}')
                error_count += 1
                continue
            
            # Определяем расширение файла
            parsed_url = urlparse(image_url)
            file_ext = os.path.splitext(parsed_url.path)[1]
            if not file_ext or file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                if 'jpeg' in content_type or 'jpg' in content_type:
                    file_ext = '.jpg'
                elif 'png' in content_type:
                    file_ext = '.png'
                elif 'gif' in content_type:
                    file_ext = '.gif'
                elif 'webp' in content_type:
                    file_ext = '.webp'
                else:
                    file_ext = '.jpg'
            
            # Создаем безопасное имя файла
            safe_name = persona_name.replace(' ', '_').replace('(', '').replace(')', '').replace('\'', '').replace('/', '_')
            filename = f"{safe_name}{file_ext}"
            filepath = photos_dir / filename
            
            # Сохраняем файл
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            downloaded_count += 1
            print(f'  [OK] Скачано: {filename}\n')
            
            # Небольшая задержка между запросами
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f'  [ERROR] Ошибка при скачивании: {str(e)}\n')
        except Exception as e:
            error_count += 1
            print(f'  [ERROR] Неожиданная ошибка: {str(e)}\n')
    
    print(f'\n{"="*50}')
    print(f'Готово! Скачано: {downloaded_count}, ошибок: {error_count}')
    print(f'Изображения сохранены в: {photos_dir}')
    print(f'{"="*50}')

if __name__ == '__main__':
    try:
        download_images()
    except KeyboardInterrupt:
        print('\n\nСкачивание прервано пользователем')
    except Exception as e:
        print(f'\n\nКритическая ошибка: {str(e)}')

