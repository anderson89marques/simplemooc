import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings

# Customizando nosso próprio usuário
# Precisei adicionar no settings AUTH_USER_MODEL para indicar ao django que o User a ser usado será o meu user customizado
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nome do Usuário', max_length=30, unique=True,
                                validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
                                                                      'O nome do usuário deve conter letras, dígitos ou '
                                                                      'os seguintes caracterres @/./+/-/_', 'invalid')])
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)  # nome completo, opcional
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)   # o django usa para verificar se está ativo
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)  # o django verifica se esse usuário pode acessar o django admin.
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'  # Indica para o django qual o campo único de referência
    REQUIRED_FIELDS = ['email']  # Campo que é requerido

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


# Para recuperação de senha
class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets'   # acessarei os PasswordReset a partir de user usando o atributo 'resets' e não 'passwordreset_set'
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas senhas'
        ordering = ['-created_at'] # ordenado de forma decrescente pelo atributo created_at
