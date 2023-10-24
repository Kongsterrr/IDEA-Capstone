from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'search', 'class': 'search-input'}),
        required=True
    )