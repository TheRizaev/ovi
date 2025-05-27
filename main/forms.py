from django import forms
from .models import JobApplication, ContactMessage

class JobApplicationForm(forms.ModelForm):
    agreement = forms.BooleanField(
        required=True,
        label="Я согласен(а) с условиями обработки персональных данных"
    )
    
    class Meta:
        model = JobApplication
        fields = [
            'full_name', 'email', 'phone', 'profession', 
            'experience', 'education', 'availability', 'message'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите ваше полное имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите ваш email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+998 XX XXX XX XX'
            }),
            'profession': forms.Select(attrs={
                'class': 'form-input form-select'
            }),
            'experience': forms.Select(attrs={
                'class': 'form-input form-select'
            }),
            'education': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Название учебного заведения'
            }),
            'availability': forms.Select(attrs={
                'class': 'form-input form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Расскажите о себе, своих навыках и мотивации...',
                'rows': 5
            }),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите ваш email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+998 XX XXX XX XX'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-input form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Опишите ваш вопрос или предложение...',
                'rows': 5
            }),
        }