from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Ваше имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    subject = forms.CharField(
        max_length=200,
        label='Тема сообщения',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Тема сообщения'
        })
    )
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Введите ваше сообщение...'
        })
    )

    def save(self):
        cleaned_data = self.cleaned_data
        print(f"Contact form submission: {cleaned_data}")