from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField, PasswordResetForm)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from quotes_app.models import Author, Quote, Tag  # noqa

form_style = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"


class RegisterForm(UserCreationForm):
    username = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": form_style}),
    )
    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={"class": form_style}),
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={"class": form_style}),
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": form_style})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": form_style}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "password"]


form_field_style = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-600 dark:focus:ring-blue-500 dark:focus:border-blue-500"
form_textfield_style = "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"


class AddQuoteForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        widget=forms.Select(attrs={"class": form_field_style}),
    )
    quote = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": form_textfield_style, "rows": 4})
        # Adjust cols and rows as needed "cols": 80
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": form_field_style}),
    )

    class Meta:
        model = Quote
        fields = ["author", "quote", "tags"]


class AddAuthorForm(forms.ModelForm):
    fullname = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": form_field_style}),
    )
    born_date = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": form_field_style}),
    )
    born_location = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": form_field_style}),
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": form_textfield_style, "rows": 4}),
    )

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class AddTagForm(forms.ModelForm):
    word = forms.CharField(
        max_length=35,
        required=True,
        widget=forms.TextInput(attrs={"class": form_style}),
    )

    class Meta:
        model = Tag
        fields = ["word"]

class ResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": form_style})
    )