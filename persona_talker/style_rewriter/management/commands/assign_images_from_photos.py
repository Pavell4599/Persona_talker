from django.core.management.base import BaseCommand
from django.core.files import File
from style_rewriter.models import Persona
from pathlib import Path
import re


class Command(BaseCommand):
    help = 'Автоматически присваивает изображения из папки photos персонажам по совпадению имени'

    def handle(self, *args, **options):
        # Путь к папке photos
        photos_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / 'photos'
        
        if not photos_dir.exists():
            self.stdout.write(
                self.style.ERROR(f'Папка photos не найдена: {photos_dir}')
            )
            return
        
        # Получаем все изображения из папки
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(photos_dir.glob(f'*{ext}'))
            image_files.extend(photos_dir.glob(f'*{ext.upper()}'))
        
        if not image_files:
            self.stdout.write(
                self.style.WARNING('В папке photos не найдено изображений')
            )
            return
        
        # Получаем всех системных персонажей
        personas = Persona.objects.filter(user=None)
        
        updated_count = 0
        skipped_count = 0
        
        for persona in personas:
            # Если у персоны уже есть изображение, пропускаем
            if persona.image:
                skipped_count += 1
                continue
            
            # Нормализуем имя персонажа для поиска
            persona_name_normalized = re.sub(r'[^\w\s]', '', persona.name.lower())
            persona_name_normalized = persona_name_normalized.replace(' ', '_')
            
            # Ищем подходящее изображение
            matched_image = None
            for image_file in image_files:
                # Нормализуем имя файла
                file_name_normalized = re.sub(r'[^\w\s]', '', image_file.stem.lower())
                file_name_normalized = file_name_normalized.replace(' ', '_')
                
                # Проверяем совпадение
                if (persona_name_normalized in file_name_normalized or 
                    file_name_normalized in persona_name_normalized or
                    any(word in file_name_normalized for word in persona_name_normalized.split('_') if len(word) > 3)):
                    matched_image = image_file
                    break
            
            if matched_image:
                try:
                    with open(matched_image, 'rb') as f:
                        persona.image.save(
                            matched_image.name,
                            File(f),
                            save=True
                        )
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[+] Изображение добавлено для "{persona.name}": {matched_image.name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'[!] Ошибка при добавлении изображения для "{persona.name}": {str(e)}')
                    )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'[-] Изображение не найдено для "{persona.name}"')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nГотово! Обновлено: {updated_count}, пропущено: {skipped_count}'
            )
        )



