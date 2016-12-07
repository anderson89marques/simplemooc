from django import forms
from django.contrib.auth import get_user_model
from simplemooc.accounts.models import PasswordReset
from simplemooc.core.utils import generate_hash_key
from simplemooc.core.mail import send_mail_template


User = get_user_model()  # Agora o django irá buscar o user configurado, no caso o nosso Usuário customizado


class PasswordResetForm(forms.Form):  # extendir de form pois não usuarei um modelo como base para esse form

    email = forms.EmailField(label='E-mail')

    def clean_eamil(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        else:
            return forms.ValidationError('Nenhum usuário encontrado com este email')

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.email)
        reset = PasswordReset(user=user, key=key)
        reset.save()

        template_name = 'accounts/password_reset_mail.html'
        subject = 'Criar Nova senha no simple mooc'
        context = {
            'reset': reset
        }
        send_mail_template(subject=subject, template_name=template_name, context=context, recipient_list=[user.email])


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação da senha não está correta!')
        self.instance.username = self.cleaned_data.get('username')

        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)  # não fará o commit mas retornará o user
        user.set_password(self.cleaned_data['password1'])   # setando e criptografando o password

        if commit:
            user.save()

        return user

    class Meta:
        model = User  # Qual modelo será editado
        fields = ['username', 'email']  # Quais atributos serão manipulados


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User  # Qual modelo será editado
        fields = ['username', 'email', 'name']  # Quais atributos serão manipulados
