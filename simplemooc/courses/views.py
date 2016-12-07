from django.shortcuts import render, get_object_or_404
from .models import Course
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


# def details(request, pk):
#     course = get_object_or_404(Course, pk=pk) # se não encontrar o objeto será retornado uma página com o erro 404
#     context = {
#         'course': course
#     }
#     template_name = 'courses/details.html'
#     return render(request, template_name, context=context)

