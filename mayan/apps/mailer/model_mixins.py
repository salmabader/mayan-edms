from furl import furl

from django.conf import settings
from django.core import mail
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.templating.classes import Template

from .events import event_email_sent
from .utils import split_recipient_list


class UserMailerBusinessLogicMixin:
    def get_connection(self):
        """
        Establishes a reusable connection to the server by loading the
        backend, initializing it, and the using the backend instance to get
        a connection.
        """
        backend_class = self.get_backend_class()

        return mail.get_connection(
            backend=backend_class.class_path, **self.get_backend_data()
        )

    def send(
        self, to, _event_action_object=None, attachments=None, bcc=None,
        body='', cc=None, reply_to=None, subject='', user=None
    ):
        """
        Send a simple email. There is no document or template knowledge.
        attachments is a list of dictionaries with the keys:
        filename, content, and mimetype.
        """
        recipient_list = split_recipient_list(
            recipients=[to]
        )

        if cc:
            cc_list = split_recipient_list(
                recipients=[cc]
            )
        else:
            cc_list = None

        if bcc:
            bcc_list = split_recipient_list(
                recipients=[bcc]
            )
        else:
            bcc_list = None

        if reply_to:
            reply_to_list = split_recipient_list(
                recipients=[reply_to]
            )
        else:
            reply_to_list = None

        backend_data = self.get_backend_data()

        with self.get_connection() as connection:
            email_message = mail.EmailMultiAlternatives(
                bcc=bcc_list, body=strip_tags(body), cc=cc_list,
                connection=connection, from_email=backend_data.get('from'),
                reply_to=reply_to_list, subject=subject,
                to=recipient_list
            )

            for attachment in attachments or ():
                email_message.attach(
                    content=attachment['content'],
                    filename=attachment['filename'],
                    mimetype=attachment['mimetype']
                )

            email_message.attach_alternative(body, 'text/html')

        try:
            email_message.send()

        except Exception as exception:
            self.error_log.create(
                text='{}; {}'.format(
                    exception.__class__.__name__, exception
                )
            )
        else:
            self.error_log.all().delete()

            event_email_sent.commit(
                action_object=_event_action_object, actor=user,
                target=self
            )

    def send_object(
        self, obj, to, as_attachment=False, bcc=None, body='', cc=None,
        content_function_dotted_path=None,
        mime_type_function_dotted_path=None, object_name=None,
        organization_installation_url='', reply_to=None, subject='',
        user=None
    ):
        """
        Send an object file using this user mailing profile.
        """
        context_dictionary = {
            'link': furl(organization_installation_url).join(
                obj.get_absolute_url()
            ).tostr(),
            'object': obj,
            'object_name': object_name
        }

        body_template = Template(template_string=body)
        body_html_content = body_template.render(
            context=context_dictionary
        )

        subject_template = Template(template_string=subject)
        subject_text = strip_tags(
            subject_template.render(context=context_dictionary)
        )

        attachments = []
        if as_attachment:
            if not content_function_dotted_path:
                raise ValueError(
                    'Must provide `content_function_dotted_path` '
                    'to allow sending the object as an attachment.'
                )

            if not mime_type_function_dotted_path:
                raise ValueError(
                    'Must provide `mime_type_function_dotted_path` to '
                    'allow sending the object as an attachment.'
                )

            content_function = import_string(
                dotted_path=content_function_dotted_path
            )

            mime_type_function = import_string(
                dotted_path=mime_type_function_dotted_path
            )
            mime_type = mime_type_function(obj=obj)

            with content_function(obj=obj) as file_object:
                attachments.append(
                    {
                        'content': file_object.read(),
                        'filename': str(obj),
                        'mimetype': mime_type
                    }
                )

        return self.send(
            _event_action_object=obj, attachments=attachments, bcc=bcc,
            body=body_html_content, cc=cc, reply_to=reply_to,
            subject=subject_text, to=to, user=user
        )

    def test(self, to, user=None):
        """
        Send a test message to make sure the mailing profile settings are
        correct.
        """
        try:
            self.send(
                subject=_('Test email from Mayan EDMS'), to=to, user=user
            )
        except Exception as exception:
            self.error_log.create(
                text='{}; {}'.format(
                    exception.__class__.__name__, exception
                )
            )
            if settings.DEBUG:
                raise
        else:
            self.error_log.all().delete()
