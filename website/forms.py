from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from website.models import Category, Wish

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]

class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "color"]

class WishCreationForm(forms.ModelForm):

    class Meta:
        model = Wish
        fields = ["name", "categories", "description", "link", "wish_image"]

    def __init__(self, *args,**kwargs):
        self.request = kwargs.pop('request')
        super (WishCreationForm,self ).__init__(*args,**kwargs)
        self.fields['categories'].queryset = Category.objects.filter(owner=self.request.user)