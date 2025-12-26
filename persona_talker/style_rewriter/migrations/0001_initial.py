# Generated manually for StyleRewriter app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Имя персонажа')),
                ('style_description', models.TextField(help_text='Краткое описание стиля, например: «Философский, пафосный, с метафорами о воле и сверхчеловеке»', verbose_name='Описание стиля')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Персона',
                'verbose_name_plural': 'Персоны',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RewriteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_text', models.TextField(verbose_name='Оригинальный текст')),
                ('rewritten_text', models.TextField(verbose_name='Переписанный текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='style_rewriter.persona', verbose_name='Персона')),
                ('user', models.ForeignKey(blank=True, help_text='Пользователь, сделавший запрос (null для анонимных)', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Запрос на переписывание',
                'verbose_name_plural': 'Запросы на переписывание',
                'ordering': ['-created_at'],
            },
        ),
    ]

