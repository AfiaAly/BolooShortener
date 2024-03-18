from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True,  widget= forms.TextInput(attrs={'placeholder':'Enter Email','class':'form-control'}))
    password = forms.CharField(max_length=30, required=True, validators=[validate_password], widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','class':'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'Password confirm password must match')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            self.add_error('email', 'This email is already in use! Try another email.')
        return email