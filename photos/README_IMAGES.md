# Инструкция по добавлению изображений персонажей

## Автоматическое скачивание

Запустите скрипт (может не работать из-за ограничений Wikipedia):
```bash
python download_images.py
```

## Ручное добавление изображений

1. Найдите изображения персонажей в интернете
2. Сохраните их в папку `photos` с именами, соответствующими именам персонажей
3. Используйте формат: `Имя_Персонажа.jpg` (замените пробелы на подчеркивания, уберите скобки)

### Примеры имен файлов:
- `Дудь.jpg`
- `BTS_RM.jpg`
- `BLACKPINK_Jennie.jpg`
- `MrBeast.jpg`
- `Илон_Маск.jpg`
- `Шрек.png`

## После добавления изображений

Запустите команду Django для автоматического присвоения:
```bash
cd persona_talker
python manage.py assign_images_from_photos
```

Эта команда автоматически найдет изображения по совпадению имени и присвоит их персонажам.

## Список персонажей, которым нужны изображения:

### Российские блогеры:
- Дудь
- Варламов
- Катя Клэп
- Маша Вэй
- Амина
- Ивангай
- SlivkiShow
- Андрей Шевченко
- Эльдар Джарахов
- Ляйсан Утяшева

### Иностранные блогеры:
- MrBeast
- PewDiePie
- Logan Paul
- Jake Paul
- KSI
- David Dobrik
- Emma Chamberlain
- Charli D'Amelio
- Addison Rae
- Zach King

### Корейские айдолы:
- BTS (RM)
- BTS (Jungkook)
- BTS (V)
- BLACKPINK (Jennie)
- BLACKPINK (Lisa)
- BLACKPINK (Rosé)
- BLACKPINK (Jisoo)
- IU
- G-Dragon
- Taeyang
- EXO (Baekhyun)
- EXO (Kai)
- Red Velvet (Irene)
- Red Velvet (Seulgi)
- TWICE (Nayeon)
- TWICE (Sana)
- aespa (Karina)
- aespa (Winter)
- NewJeans (Hanni)
- NewJeans (Minji)
- LE SSERAFIM (Chaewon)
- LE SSERAFIM (Sakura)
- IVE (Wonyoung)
- IVE (Yujin)

### Дополнительные:
- Эрик Давидыч
- Гарик Харламов
- Илон Маск
- Джокер
- Шрек



