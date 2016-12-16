from django.db import models
from django.urls import reverse
from django.conf import settings


class CourseManager(models.Manager):
    def search(self, query):
        return models.Q(self.get_queryset().filter(name__icontains=query)) | \
               models.Q(self.get_queryset().filter(slug__icontains=query))


class Course(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')  # ajuda a definir urls mais amigáveis.
    description = models.TextField('Descrição Simples', blank=True)
    about = models.TextField('Sobre o curso', blank=True)
    start_date = models.DateField('Data de Inicío', null=True, blank=True)
    image = models.ImageField(
        upload_to='courses/images', verbose_name='Imagem'
        , null=True, blank=True
    )  # A path é baseada no MEDIA_ROOT e no MEDIA_URL definida no Settings
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        O Django identificará a url quando eu chamar esse método e não precisarei usar -> url 'details' slug=course.slug
        no template para acessar a url. O reverse gera a url a partir da view e dos parametros passados.
        """

        return reverse('details', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']


# classe que cuidará da inscrição dos usuário nos cursos
class Enrollment(models.Model):

    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='enrollments'
    )
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)  # Impedir repetição de enrollment que já tenha um user e course


class Announcement(models.Model):
    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='announcements'
    )
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')

    # O ideal é criar um model com esses campo e todos os models extenderem dele
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']


class Comment(models.Model):
    announcement = models.ForeignKey(
        Announcement, verbose_name='Anúncio', related_name='comments'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário')
    content = models.TextField('Conteúdo')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']
