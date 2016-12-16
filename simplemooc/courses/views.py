from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from simplemooc.accounts.views import dashboard
from .models import Course, Enrollment
from .forms import ContactCourse


def list(request):
    courses = Course.objects.all()
    template_path = 'courses/index.html'

    context = {
        'courses': courses
    }
    return render(request, template_path, context=context)


def details(request, slug):
    course = get_object_or_404(Course, slug=slug)  # se não encontrar o objeto será retornado uma página com o erro 404

    context = {}

    if request.method == 'POST':
        form = ContactCourse(request.POST)  # Recebendo os dados do formulário
        if form.is_valid():
            print('is valid')
            context['is_valid'] = True
            form.send_mail(course)
            print(form.cleaned_data)  # quando eu quiser as informações sanitizadas eu tenho que pegar de form.cleaned_data
            form = ContactCourse()
    else:
        form = ContactCourse()

    context['course'] = course
    context['form'] = form

    template_name = 'courses/course.html'
    return render(request, template_name, context=context)


@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment_instance, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )

    if request.method == 'POST':
        enrollment_instance.delete()
        messages.success(request, 'Sua Inscrição foi cancelada com sucesso!')

        return redirect(dashboard)

    template_name = "courses/undo_enrollment.html"
    context = {
        'enrollment': enrollment_instance,
        'course': course
    }

    return render(request, template_name=template_name, context=context)


# processo de inscrição
@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment_instance, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )

    if created:
        enrollment_instance.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso!')
    else:
        messages.info(request, 'Você já está inscrito no curso!')

    return redirect(dashboard)


@login_required
def announcements(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if not request.user.is_staff:  # só verifica à aprovação se o usuário não for admin
        #verificando se o usuário está inscrito no curso
        enrollment_instance = get_object_or_404(Enrollment, user=request.user, course=course)

        if not enrollment_instance.is_approved():  # verificando se a inscrição do usuário foi aprovada
            messages.error(request, 'A sua inscrição está pendente')
            return redirect(dashboard)

    template_name = 'courses/announcements.html'
    context = dict()
    context['course'] = course

    return render(request, template_name=template_name, context=context)