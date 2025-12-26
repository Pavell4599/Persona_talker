from django.db import models
from django.contrib.auth.models import User


class Persona(models.Model):
    """Модель для хранения персонажей и их стилей переписывания"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Создатель",
        help_text="Пользователь, создавший персону (null для системных персон)"
    )
    name = models.CharField(max_length=200, verbose_name="Имя персонажа")
    style_description = models.TextField(
        verbose_name="Описание стиля",
        help_text="Краткое описание стиля, например: «Философский, пафосный, с метафорами о воле и сверхчеловеке»"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Полное описание",
        help_text="Подробное описание знаменитости, биография, достижения"
    )
    image = models.ImageField(
        upload_to='personas/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Фото знаменитости"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def is_system_persona(self):
        """Проверяет, является ли персона системной (созданной администратором)"""
        return self.user is None


class RewriteRequest(models.Model):
    """Модель для хранения запросов на переписывание текста"""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        help_text="Пользователь, сделавший запрос (null для анонимных)"
    )
    original_text = models.TextField(verbose_name="Оригинальный текст")
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        verbose_name="Персона"
    )
    rewritten_text = models.TextField(verbose_name="Переписанный текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Запрос на переписывание"
        verbose_name_plural = "Запросы на переписывание"
        ordering = ['-created_at']

    def __str__(self):
        user_str = self.user.username if self.user else "Аноним"
        return f"{user_str} - {self.persona.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

