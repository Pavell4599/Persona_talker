from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Persona, RewriteRequest
from .forms import RewriteForm, PersonaForm
from .ai_service import rewrite_text_with_ai


def home(request):
    """Главная страница с формой переписывания текста"""
    rewritten_text = None
    selected_persona_id = request.session.get('selected_persona_id')
    selected_persona = None
    
    if selected_persona_id:
        try:
            selected_persona = Persona.objects.get(pk=selected_persona_id)
        except Persona.DoesNotExist:
            request.session.pop('selected_persona_id', None)
    
    if request.method == 'POST':
        form = RewriteForm(request.POST, selected_persona=selected_persona)
        if form.is_valid():
            original_text = form.cleaned_data['original_text']
            persona = form.cleaned_data['persona']
            message_type = form.cleaned_data.get('message_type', 'custom')
            
            # Если выбран тип сообщения, генерируем текст
            if message_type != 'custom' and not original_text:
                original_text = form.get_default_text_for_type(message_type)
            
            try:
                # Переписываем текст с помощью ИИ (бесплатный g4f)
                rewritten_text = rewrite_text_with_ai(
                    original_text=original_text,
                    persona_name=persona.name,
                    persona_style=persona.style_description,
                    message_type=message_type
                )
                
                # Сохраняем запрос в базу (даже для анонимных пользователей)
                RewriteRequest.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    original_text=original_text,
                    persona=persona,
                    rewritten_text=rewritten_text
                )
                
                messages.success(request, 'Текст успешно переписан!')
            except Exception as e:
                # Ошибки (API, сеть и т.д.)
                messages.error(request, f'Ошибка при переписывании: {str(e)}')
                rewritten_text = None
    else:
        form = RewriteForm(selected_persona=selected_persona)
    
    # Получаем последний результат, если он есть
    if not rewritten_text and request.user.is_authenticated:
        last_request = RewriteRequest.objects.filter(user=request.user).first()
        if last_request:
            rewritten_text = last_request.rewritten_text
    
    context = {
        'form': form,
        'rewritten_text': rewritten_text,
        'selected_persona': selected_persona,
    }
    return render(request, 'style_rewriter/home.html', context)


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def personas_list(request):
    """Список всех персон в виде карточек"""
    personas = Persona.objects.all().order_by('-created_at')
    context = {
        'personas': personas,
    }
    return render(request, 'style_rewriter/personas_list.html', context)


def select_persona(request, pk):
    """Выбор персонажа и сохранение в сессии"""
    persona = get_object_or_404(Persona, pk=pk)
    request.session['selected_persona_id'] = persona.pk
    messages.success(request, f'Выбран персонаж: {persona.name}')
    return redirect('home')


def persona_detail(request, pk):
    """Детальная страница персоны"""
    persona = get_object_or_404(Persona, pk=pk)
    context = {
        'persona': persona,
    }
    return render(request, 'style_rewriter/persona_detail.html', context)


@login_required
def persona_create(request):
    """Создание новой персоны пользователем"""
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES)
        if form.is_valid():
            persona = form.save(commit=False)
            persona.user = request.user
            persona.save()
            messages.success(request, f'Персона "{persona.name}" успешно создана!')
            return redirect('persona_detail', pk=persona.pk)
    else:
        form = PersonaForm()
    return render(request, 'style_rewriter/persona_form.html', {'form': form, 'title': 'Создать персону'})


@login_required
def persona_edit(request, pk):
    """Редактирование персоны"""
    persona = get_object_or_404(Persona, pk=pk)
    
    # Проверяем права доступа
    if persona.user != request.user and not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для редактирования этой персоны.')
        return redirect('persona_detail', pk=pk)
    
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES, instance=persona)
        if form.is_valid():
            form.save()
            messages.success(request, f'Персона "{persona.name}" успешно обновлена!')
            return redirect('persona_detail', pk=persona.pk)
    else:
        form = PersonaForm(instance=persona)
    return render(request, 'style_rewriter/persona_form.html', {'form': form, 'persona': persona, 'title': 'Редактировать персону'})


@login_required
def persona_delete(request, pk):
    """Удаление персоны"""
    persona = get_object_or_404(Persona, pk=pk)
    
    # Проверяем права доступа
    if persona.user != request.user and not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для удаления этой персоны.')
        return redirect('persona_detail', pk=pk)
    
    if request.method == 'POST':
        persona_name = persona.name
        persona.delete()
        messages.success(request, f'Персона "{persona_name}" успешно удалена!')
        return redirect('personas_list')
    
    return render(request, 'style_rewriter/persona_confirm_delete.html', {'persona': persona})

