from django import forms
from .models import CustomUser, Employer, MailDetails
from django.contrib.auth.hashers import check_password

def no_username_validator(value):
    return None

class EmployeeSignUpForm(forms.ModelForm):
    username = forms.CharField(label='Username', error_messages={
        'required': 'Please enter a username.',
        'invalid': 'This username is invalid.',
    }, widget=forms.TextInput(attrs={'autofocus': 'true'}), validators=[no_username_validator])
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class EmployerSignUpForm(forms.ModelForm):
    username = forms.CharField(label='Username', error_messages={
        'required': 'Please enter a username.',
        'invalid': 'This username is invalid.',
    }, widget=forms.TextInput(attrs={'autofocus': 'true'}), validators=[no_username_validator])
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(EmployerSignUpForm, self).__init__(*args, **kwargs)
        self.fields['company_name'] = forms.CharField(max_length=255)

    def save(self, commit=True):
        user = super(EmployerSignUpForm, self).save(commit=False)
        user.user_type = 'employer'
        if commit:
            user.save()
            employer = Employer(user=user, company_name=self.cleaned_data['company_name'])
            employer.save()
        return user

class MailUpdateForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class EmailForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient Email')
    subject = forms.CharField(label='Subject')
    message = forms.CharField(label='Message', widget=forms.Textarea)
    password = forms.CharField(label='Password', required=False, widget=forms.PasswordInput)
