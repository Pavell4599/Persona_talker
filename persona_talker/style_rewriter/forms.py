from django import forms
from .models import Persona


class PersonaForm(forms.ModelForm):
    """Форма для создания/редактирования персоны"""
    class Meta:
        model = Persona
        fields = ['name', 'style_description', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Альберт Эйнштейн'
            }),
            'style_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Краткое описание стиля речи...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Подробное описание знаменитости, биография...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'name': 'Имя персонажа',
            'style_description': 'Описание стиля',
            'description': 'Полное описание',
            'image': 'Изображение',
        }


class RewriteForm(forms.Form):
    """Форма для запроса переписывания текста"""
    MESSAGE_TYPES = [
        ('custom', 'Своя фраза'),
        ('pickup', 'Подкат'),
        ('congratulation', 'Поздравление'),
        ('joke', 'Шутка'),
    ]
    
    message_type = forms.ChoiceField(
        choices=MESSAGE_TYPES,
        initial='custom',
        label="Тип сообщения",
        widget=forms.RadioSelect(attrs={
            'class': 'message-type-radio'
        }),
        required=True
    )
    
    original_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 50,
            'placeholder': 'Введите текст, который нужно переписать...',
            'style': 'width: 100%; padding: 10px; font-size: 14px; border: 1px solid #ddd; border-radius: 4px;',
            'id': 'original_text_field'
        }),
        label="Текст",
        required=False
    )
    
    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        empty_label="Выберите персону...",
        label="Персона",
        widget=forms.Select(attrs={
            'style': 'width: 100%; padding: 10px; font-size: 14px; border: 1px solid #ddd; border-radius: 4px;'
        }),
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        selected_persona = kwargs.pop('selected_persona', None)
        super().__init__(*args, **kwargs)
        
        if selected_persona:
            self.fields['persona'].initial = selected_persona
    
    def get_default_text_for_type(self, message_type):
        """Возвращает текст по умолчанию для типа сообщения"""
        defaults = {
            'pickup': 'Привет, как дела?',
            'congratulation': 'Поздравляю с праздником!',
            'joke': 'Расскажи шутку',
        }
        return defaults.get(message_type, '')
    
    def clean(self):
        cleaned_data = super().clean()
        message_type = cleaned_data.get('message_type')
        original_text = cleaned_data.get('original_text', '').strip()
        
        if message_type == 'custom' and not original_text:
            raise forms.ValidationError('Введите текст для переписывания или выберите тип сообщения.')
        
        return cleaned_data

