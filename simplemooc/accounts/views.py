from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages

from simplemooc.accounts.forms import RegisterForm, EditAccountForm, PasswordResetForm
from simplemooc.accounts.models import PasswordReset
from simplemooc.core.views import home
from simplemooc.courses.models import Enrollment



User = get_user_model()


@login_required  # indica que só terá acesso a essa view quem estiver logado
def dashboard(request):
    template_name = 'accounts/dashboard.html'

    return render(request, template_name=template_name)


def register(request):
    template_name = "accounts/register.html"
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Após cadastrar o usuário é feito logo o login
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            login(request, user)

            return redirect(home)  # redirecionando para login

    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, template_name=template_name, context=context)


def password_reset(request):
    template_name = 'accounts/password_reset.html'

    # Pra não ficar instânciando duas vezes o form uma com parametro e outra sem parametro
    # assim não preciso fazer a verificação da sequinte forma : if request.method == 'POST': e etc
    # preciso refatorar os outros métodos
    form = PasswordResetForm(request.POST or None)
    context = dict()

    if form.is_valid():
        form.save()
        messages.success(request, 'Um email lhe foi enviado!!')

    context['form'] = form

    return render(request=request, template_name=template_name, context=context)


def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = dict()
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Sua senha foi criada com sucesso!!')
    context['form'] = form

    return render(request, template_name, context)


@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = dict()

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Salvando as alterações
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso!!')
            return redirect(dashboard)
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form

    return render(request=request, template_name=template_name, context=context)


@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = dict()

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)  # o django já tem um form para tratar a mudança de senha.

        if form.is_valid():
            form.save()
            context['success'] = True

            # Tive que fazer a atualização do hash da sessão usando a função abaixo, assim o usuário continua logado
            # porém com seus dados de sessão atualizados.
            # Ver documentação na seção: Invalidação de Sessão após a Troca de Senha.
            update_session_auth_hash(request, form.user)  # Atualiza o hash de sessão apropriadamente
    else:
        form = PasswordChangeForm(user=request.user)

    context['form'] = form
    return render(request=request, template_name=template_name, context=context)
