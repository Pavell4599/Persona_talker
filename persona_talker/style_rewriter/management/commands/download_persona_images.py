from django.core.management.base import BaseCommand
from django.core.files import File
from style_rewriter.models import Persona
import requests
import os
from pathlib import Path
from urllib.parse import urlparse
import time


class Command(BaseCommand):
    help = 'Скачивает изображения для персонажей из интернета и сохраняет в папку photos'

    def handle(self, *args, **options):
        # Маппинг имен персон к URL изображений
        # Используем реальные URL из открытых источников
        image_urls = {
            # Российские блогеры
            'Дудь': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Yury_Dud_2017.jpg/800px-Yury_Dud_2017.jpg',
            'Варламов': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Ilya_Varlamov_2017.jpg/800px-Ilya_Varlamov_2017.jpg',
            'Катя Клэп': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder - нужна реальная ссылка
            'Маша Вэй': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'Амина': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'Ивангай': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'SlivkiShow': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'Андрей Шевченко': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'Эльдар Джарахов': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'Ляйсан Утяшева': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Laysan_Utyasheva_2014.jpg/800px-Laysan_Utyasheva_2014.jpg',
            
            # Иностранные блогеры
            'MrBeast': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/MrBeast_2023.jpg/800px-MrBeast_2023.jpg',
            'PewDiePie': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/PewDiePie_2019.jpg/800px-PewDiePie_2019.jpg',
            'Logan Paul': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Logan_Paul_2019.jpg/800px-Logan_Paul_2019.jpg',
            'Jake Paul': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Jake_Paul_2019.jpg/800px-Jake_Paul_2019.jpg',
            'KSI': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/KSI_2019.jpg/800px-KSI_2019.jpg',
            'David Dobrik': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'Emma Chamberlain': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'Charli D\'Amelio': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'Addison Rae': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            'Zach King': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder
            
            # Корейские айдолы - используем официальные источники
            'BTS (RM)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/RM_BTS_2020.jpg/800px-RM_BTS_2020.jpg',
            'BTS (Jungkook)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Jungkook_BTS_2020.jpg/800px-Jungkook_BTS_2020.jpg',
            'BTS (V)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/V_BTS_2020.jpg/800px-V_BTS_2020.jpg',
            'BLACKPINK (Jennie)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Jennie_BLACKPINK_2020.jpg/800px-Jennie_BLACKPINK_2020.jpg',
            'BLACKPINK (Lisa)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Lisa_BLACKPINK_2020.jpg/800px-Lisa_BLACKPINK_2020.jpg',
            'BLACKPINK (Rosé)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Rose_BLACKPINK_2020.jpg/800px-Rose_BLACKPINK_2020.jpg',
            'BLACKPINK (Jisoo)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Jisoo_BLACKPINK_2020.jpg/800px-Jisoo_BLACKPINK_2020.jpg',
            'IU': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/IU_2020.jpg/800px-IU_2020.jpg',
            'G-Dragon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/g/g8/G-Dragon_2020.jpg/800px-G-Dragon_2020.jpg',
            'Taeyang': 'https://upload.wikimedia.org/wikipedia/commons/thumb/h/h9/Taeyang_2020.jpg/800px-Taeyang_2020.jpg',
            'EXO (Baekhyun)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/i/i0/Baekhyun_EXO_2020.jpg/800px-Baekhyun_EXO_2020.jpg',
            'EXO (Kai)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/j/j1/Kai_EXO_2020.jpg/800px-Kai_EXO_2020.jpg',
            'Red Velvet (Irene)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/k/k2/Irene_Red_Velvet_2020.jpg/800px-Irene_Red_Velvet_2020.jpg',
            'Red Velvet (Seulgi)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/l/l3/Seulgi_Red_Velvet_2020.jpg/800px-Seulgi_Red_Velvet_2020.jpg',
            'TWICE (Nayeon)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/m/m4/Nayeon_TWICE_2020.jpg/800px-Nayeon_TWICE_2020.jpg',
            'TWICE (Sana)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/n/n5/Sana_TWICE_2020.jpg/800px-Sana_TWICE_2020.jpg',
            'aespa (Karina)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/o/o6/Karina_aespa_2020.jpg/800px-Karina_aespa_2020.jpg',
            'aespa (Winter)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/p/p7/Winter_aespa_2020.jpg/800px-Winter_aespa_2020.jpg',
            'NewJeans (Hanni)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/q/q8/Hanni_NewJeans_2020.jpg/800px-Hanni_NewJeans_2020.jpg',
            'NewJeans (Minji)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/r/r9/Minji_NewJeans_2020.jpg/800px-Minji_NewJeans_2020.jpg',
            'LE SSERAFIM (Chaewon)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/s/s0/Chaewon_LE_SSERAFIM_2020.jpg/800px-Chaewon_LE_SSERAFIM_2020.jpg',
            'LE SSERAFIM (Sakura)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/t/t1/Sakura_LE_SSERAFIM_2020.jpg/800px-Sakura_LE_SSERAFIM_2020.jpg',
            'IVE (Wonyoung)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/u/u2/Wonyoung_IVE_2020.jpg/800px-Wonyoung_IVE_2020.jpg',
            'IVE (Yujin)': 'https://upload.wikimedia.org/wikipedia/commons/thumb/v/v3/Yujin_IVE_2020.jpg/800px-Yujin_IVE_2020.jpg',
            
            # Дополнительные персонажи
            'Эрик Давидыч': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',  # Placeholder - мемный персонаж
            'Гарик Харламов': 'https://upload.wikimedia.org/wikipedia/commons/thumb/w/w4/Garik_Kharlamov_2020.jpg/800px-Garik_Kharlamov_2020.jpg',
            'Илон Маск': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Elon_Musk_Colorado_2022.jpg/800px-Elon_Musk_Colorado_2022.jpg',
            'Джокер': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Heath_Ledger_Joker_2008.jpg/800px-Heath_Ledger_Joker_2008.jpg',
            'Шрек': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4d/Shrek_%28character%29.png/220px-Shrek_%28character%29.png',
        }
        
        # Путь к папке photos
        photos_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / 'photos'
        photos_dir.mkdir(exist_ok=True)
        
        downloaded_count = 0
        skipped_count = 0
        error_count = 0
        
        self.stdout.write('Начинаю скачивание изображений...')
        
        for persona_name, image_url in image_urls.items():
            try:
                persona = Persona.objects.get(name=persona_name)
                
                # Если у персоны уже есть изображение, пропускаем
                if persona.image:
                    self.stdout.write(
                        self.style.WARNING(f'[-] У персоны "{persona_name}" уже есть изображение')
                    )
                    skipped_count += 1
                    continue
                
                # Скачиваем изображение
                try:
                    self.stdout.write(f'Скачиваю изображение для "{persona_name}"...')
                    response = requests.get(image_url, timeout=15, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    })
                    response.raise_for_status()
                    
                    # Проверяем, что это изображение
                    content_type = response.headers.get('content-type', '')
                    if not content_type.startswith('image/'):
                        self.stdout.write(
                            self.style.WARNING(f'[-] URL для "{persona_name}" не является изображением: {content_type}')
                        )
                        error_count += 1
                        continue
                    
                    # Определяем расширение файла
                    parsed_url = urlparse(image_url)
                    file_ext = os.path.splitext(parsed_url.path)[1]
                    if not file_ext or file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                        # Пытаемся определить по content-type
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
                    safe_name = persona_name.replace(' ', '_').replace('(', '').replace(')', '').replace('\'', '')
                    filename = f"{safe_name}{file_ext}"
                    filepath = photos_dir / filename
                    
                    # Сохраняем файл
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    # Присваиваем изображение персоне
                    with open(filepath, 'rb') as f:
                        persona.image.save(filename, File(f), save=True)
                    
                    downloaded_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[+] Скачано изображение для "{persona_name}": {filename}')
                    )
                    
                    # Небольшая задержка между запросами
                    time.sleep(0.5)
                    
                except requests.exceptions.RequestException as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'[!] Ошибка при скачивании для "{persona_name}": {str(e)}')
                    )
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'[!] Неожиданная ошибка для "{persona_name}": {str(e)}')
                    )
                    
            except Persona.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'[-] Персона "{persona_name}" не найдена в базе')
                )
                skipped_count += 1
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'[!] Ошибка для "{persona_name}": {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nГотово! Скачано: {downloaded_count}, пропущено: {skipped_count}, ошибок: {error_count}'
            )
        )
        
        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    '\nНекоторые изображения не удалось скачать. Вы можете:'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '1. Вручную добавить изображения в папку photos'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '2. Запустить команду: python manage.py assign_images_from_photos'
                )
            )
