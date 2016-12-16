from django.template import Library
from simplemooc.courses.models import Enrollment
register = Library()


@register.assignment_tag
def load_my_courses(user):

    if not user.is_staff:  # se não for super usuário
        return Enrollment.objects.filter(user=user)

    return Enrollment.objects.all()
