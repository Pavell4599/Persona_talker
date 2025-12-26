from django.core.management.base import BaseCommand
from django.core.files import File
from style_rewriter.models import Persona
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Привязывает изображения из папки photos к персонам'

    def handle(self, *args, **options):
        # Маппинг имен файлов к именам персон (обновлено с новыми именами файлов)
        image_mapping = {
            'Ницше': ['Ницше_Фридрих.jpg'],
            'Достоевский': ['2fd51e50d4280300b6a627d74d4b08b8_XL.jpg', 'KYA_000093_01187_1_t218_122335.jpg'],
            'Стив Джобс': ['Steve_Jobs_Headshot_2010-CROP.jpg'],
            'Бабушка из деревни': ['babushka.jpg'],
            'Эйнштейн': ['einstein.jpg'],
            'Чехов': ['chehov.jpeg'],
            'Наполеон': ['Napoleon_Paul_Delaroche.jpg'],
            'Шекспир': ['chekspir.jpg'],
            'Марк Твен': ['oskarrr.jpg'],
            'Конфуций': ['Konfuci.png'],
            'Оскар Уайльд': ['oskarrr.jpg'],
            'Карл Маркс': ['marx.png'],
        }
        
        # Путь к папке photos (на уровень выше persona_talker)
        photos_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / 'photos'
        
        if not photos_dir.exists():
            self.stdout.write(
                self.style.ERROR(f'Папка photos не найдена: {photos_dir}')
            )
            return
        
        updated_count = 0
        skipped_count = 0
        
        for persona_name, image_files in image_mapping.items():
            try:
                persona = Persona.objects.get(name=persona_name)
                
                # Если у персоны уже есть изображение, пропускаем
                if persona.image:
                    self.stdout.write(
                        self.style.WARNING(f'[-] У персоны "{persona_name}" уже есть изображение')
                    )
                    skipped_count += 1
                    continue
                
                # Ищем первое доступное изображение
                image_path = None
                for img_file in image_files:
                    potential_path = photos_dir / img_file
                    if potential_path.exists():
                        image_path = potential_path
                        break
                
                if image_path:
                    # Открываем и сохраняем изображение
                    with open(image_path, 'rb') as f:
                        persona.image.save(
                            image_path.name,
                            File(f),
                            save=True
                        )
                    self.stdout.write(
                        self.style.SUCCESS(f'[+] Изображение добавлено для "{persona_name}": {image_path.name}')
                    )
                    updated_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'[-] Изображение не найдено для "{persona_name}"')
                    )
                    skipped_count += 1
                    
            except Persona.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'[-] Персона "{persona_name}" не найдена в базе')
                )
                skipped_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'[!] Ошибка при обработке "{persona_name}": {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nГотово! Обновлено: {updated_count}, пропущено: {skipped_count}'
            )
        )

