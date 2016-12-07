from django.db import models
from django.urls import reverse


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
