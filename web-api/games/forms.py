from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Player

# https://docs.djangoproject.com/en/dev/topics/auth/#a-full-example
class PlayerCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Player
        fields = ('username', 'email', 'initial_points', 'is_staff')
        exclude = ('is_active', 'date_joined', 'last_login', 'age',
                  'first_name', 'last_name', 'password')
 
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        player = super(PlayerCreationForm, self).save(commit=False)
        player.set_password(self.cleaned_data["password1"])
        if commit:
            player.save()

        return player
