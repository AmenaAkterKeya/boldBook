from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserAddress

class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    country = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = [
            'username', 'password1', 'password2', 'first_name', 
            'last_name', 'email', 'phone', 'postal_code', 
            'city', 'country', 'street_address'
        ]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserAddress.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone'),
                postal_code=self.cleaned_data.get('postal_code'),
                country=self.cleaned_data.get('country'),
                city=self.cleaned_data.get('city'),
                street_address=self.cleaned_data.get('street_address')
            )
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
class UserUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=15)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        if self.instance:
            try:
                user_address = self.instance.address
            except UserAddress.DoesNotExist:
                user_address = None

            if user_address:
                self.fields['phone'].initial = user_address.phone
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_address, created = UserAddress.objects.get_or_create(user=user)
            user_address.phone = self.cleaned_data['phone']
            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()
        return user
