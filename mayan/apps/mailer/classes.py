import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.backends.class_mixins import DynamicFormBackendMixin
from mayan.apps.backends.classes import ModelBaseBackend

__all__ = ('MailerBackend',)
logger = logging.getLogger(name=__name__)


class MailerBackend(DynamicFormBackendMixin, ModelBaseBackend):
    """
    Base class for the mailing backends. This class is mainly a wrapper
    for other Django backends that adds a few metadata to specify the
    fields it needs to be instanciated at runtime.
    """
    _loader_module_name = 'mailers'
    _backend_app_label = 'mailer'
    _backend_model_name = 'UserMailer'
    class_path = ''  # Dot path to the actual class that will handle the mail.

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = (
            (
                _('General'), {
                    'fields': ('label', 'enabled')
                }
            ),
        )

        return fieldsets


class MailerBackendBaseEmail(MailerBackend):
    class_path = None
    form_fields = {
        'from': {
            'label': _('From'),
            'class': 'django.forms.CharField', 'default': '',
            'help_text': _(
                'The sender\'s address. Some system will refuse to send '
                'messages if this value is not set.'
            ), 'kwargs': {
                'max_length': 48
            }, 'required': False
        }
    }
    label = None

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = super().get_form_fieldsets()

        fieldsets += (
            (
                _('Compatibility'), {
                    'fields': ('from',)
                }
            ),
        )

        return fieldsets


class NullBackend(MailerBackend):
    label = _('Null backend')
