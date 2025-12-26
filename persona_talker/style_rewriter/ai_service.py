"""
Сервис для переписывания текста с помощью ИИ (бесплатный через g4f)
"""
import g4f


def rewrite_text_with_ai(original_text: str, persona_name: str, persona_style: str, message_type: str = 'custom') -> str:
    """
    Переписывает текст в стиле выбранной персоны с помощью бесплатного GPT API (g4f)
    
    Args:
        original_text: Оригинальный текст для переписывания
        persona_name: Имя персоны
        persona_style: Описание стиля персоны
        message_type: Тип сообщения (custom, pickup, congratulation, joke)
        
    Returns:
        Переписанный текст
        
    Raises:
        Exception: При ошибках API или сети
    """
    try:
        # Определяем задачу в зависимости от типа сообщения
        task_description = {
            'pickup': 'создай подкат (флирт, заигрывание)',
            'congratulation': 'создай поздравление',
            'joke': 'создай шутку',
            'custom': 'перепиши следующий текст'
        }.get(message_type, 'перепиши следующий текст')
        
        # Формируем промпт для переписывания текста
        system_prompt = f"""Ты - эксперт по стилизации текста. Твоя задача - {task_description} в стиле конкретной личности.

Персона: {persona_name}
Стиль: {persona_style}

Важные требования:
1. {'Создай оригинальный текст в указанном стиле' if message_type != 'custom' else 'Сохрани основную мысль и смысл оригинального текста'}
2. Полностью используй стиль указанной персоны
3. Используй характерные для этой персоны выражения, обороты речи и манеру изложения
4. Не добавляй префиксы типа "[В стиле...]" - просто создай/перепиши текст
5. {'Создай текст подходящей длины для типа сообщения' if message_type != 'custom' else 'Сохрани примерно тот же объем текста'}
6. Ответ должен быть только текстом, без дополнительных комментариев"""

        if message_type == 'custom':
            user_prompt = f"""Перепиши следующий текст в стиле {persona_name}:

{original_text}"""
        else:
            user_prompt = f"""Создай {task_description} в стиле {persona_name}. {'Используй следующий текст как основу или вдохновение' if original_text else ''}:

{original_text if original_text else 'Создай оригинальный текст'}"""

        # Используем g4f для бесплатного доступа к GPT
        # Пробуем разные модели, если одна не работает
        models_to_try = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4o-mini",
        ]
        
        last_error = None
        for model in models_to_try:
            try:
                response = g4f.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.8,
                )
                
                if response:
                    rewritten_text = None
                    
                    # g4f может вернуть строку напрямую
                    if isinstance(response, str):
                        rewritten_text = response.strip()
                    # Или генератор (streaming)
                    elif hasattr(response, '__iter__') and not isinstance(response, str):
                        # Собираем весь ответ из генератора
                        full_response = ""
                        for chunk in response:
                            if isinstance(chunk, str):
                                full_response += chunk
                            elif hasattr(chunk, 'content'):
                                full_response += chunk.content
                            elif hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                                full_response += chunk.choices[0].message.content
                            else:
                                full_response += str(chunk)
                        rewritten_text = full_response.strip()
                    # Или объект с атрибутами
                    elif hasattr(response, 'choices') and len(response.choices) > 0:
                        rewritten_text = response.choices[0].message.content.strip()
                    elif hasattr(response, 'content'):
                        rewritten_text = response.content.strip()
                    else:
                        rewritten_text = str(response).strip()
                    
                    # Убираем возможные артефакты ответа
                    if rewritten_text:
                        if rewritten_text.startswith('"') and rewritten_text.endswith('"'):
                            rewritten_text = rewritten_text[1:-1]
                        if rewritten_text.startswith("'") and rewritten_text.endswith("'"):
                            rewritten_text = rewritten_text[1:-1]
                        
                        if rewritten_text:
                            return rewritten_text
                    
            except Exception as e:
                last_error = e
                continue  # Пробуем следующую модель
        
        # Если все модели не сработали
        raise Exception(
            f"Не удалось получить ответ от ИИ. "
            f"Попробуйте позже или проверьте интернет-соединение. "
            f"Последняя ошибка: {str(last_error)}"
        )
        
    except Exception as e:
        error_msg = str(e)
        if "connection" in error_msg.lower() or "network" in error_msg.lower():
            raise Exception("Ошибка подключения к ИИ сервису. Проверьте интернет-соединение.")
        elif "rate limit" in error_msg.lower() or "limit" in error_msg.lower():
            raise Exception("Превышен лимит запросов. Попробуйте позже.")
        else:
            raise Exception(f"Ошибка при переписывании текста: {error_msg}")
