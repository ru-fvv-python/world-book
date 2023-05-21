from datetime import date

from django import forms


class AuthorsForm(forms.Form):
    """Форма для ввода и обновления информации об авторах книг"""
    first_name = forms.CharField(label='Имя автора')
    last_name = forms.CharField(label='Фамилия автора')
    date_of_birth = forms.DateField(label='Дата рождения',
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(
                                        attrs={'type': 'date'}))
    date_of_death = forms.DateField(label='Дата смерти',
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(
                                        attrs={'type': 'date'}))
