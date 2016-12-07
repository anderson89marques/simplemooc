from django import forms
from django.conf import settings
from simplemooc.core.mail import send_mail_template


class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(
        label='Mensagem/Dúvida', widget=forms.Textarea  # Pra informar que é um TextArea
    )

    def send_mail(self, course):
        subject = '[{}] Contato'.format(course)
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'msg': self.cleaned_data['message']
        }

        to = [settings.CONTACT_EMAIL]
        template_name = 'courses/mail.html'

        send_mail_template(
            subject=subject, template_name=template_name, context=context, recipient_list=to
        )
