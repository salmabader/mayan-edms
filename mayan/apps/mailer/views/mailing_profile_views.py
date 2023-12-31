from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.backends.views import (
    ViewSingleObjectDynamicFormModelBackendCreate,
    ViewSingleObjectDynamicFormModelBackendEdit
)
from mayan.apps.views.generics import (
    FormView, SingleObjectDeleteView, SingleObjectListView
)
from mayan.apps.views.view_mixins import ExternalObjectViewMixin

from ..classes import MailerBackend
from ..forms import (
    UserMailerBackendSelectionForm, UserMailerSetupDynamicForm,
    UserMailerTestForm
)
from ..icons import (
    icon_user_mailer_backend_select, icon_user_mailer_create,
    icon_user_mailer_delete, icon_user_mailer_edit, icon_user_mailer_list,
    icon_user_mailer_test
)
from ..links import link_user_mailer_create
from ..models import UserMailer
from ..permissions import (
    permission_user_mailer_create, permission_user_mailer_delete,
    permission_user_mailer_edit, permission_user_mailer_use,
    permission_user_mailer_view
)


class UserMailerBackendSelectionView(FormView):
    extra_context = {
        'title': _('New mailing profile backend selection'),
    }
    form_class = UserMailerBackendSelectionForm
    view_icon = icon_user_mailer_backend_select
    view_permission = permission_user_mailer_create

    def form_valid(self, form):
        backend = form.cleaned_data['backend']
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='mailer:user_mailer_create', kwargs={
                    'backend_path': backend
                }
            )
        )


class UserMailingCreateView(ViewSingleObjectDynamicFormModelBackendCreate):
    backend_class = MailerBackend
    form_class = UserMailerSetupDynamicForm
    post_action_redirect = reverse_lazy(viewname='mailer:user_mailer_list')
    view_icon = icon_user_mailer_create
    view_permission = permission_user_mailer_create

    def get_extra_context(self):
        backend_class = self.get_backend_class()

        return {
            'title': _(
                'Create a "%s" mailing profile'
            ) % backend_class.label
        }

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'backend_path': self.kwargs['backend_path']
        }


class UserMailingDeleteView(SingleObjectDeleteView):
    model = UserMailer
    object_permission = permission_user_mailer_delete
    pk_url_kwarg = 'mailer_id'
    post_action_redirect = reverse_lazy(viewname='mailer:user_mailer_list')
    view_icon = icon_user_mailer_delete

    def get_extra_context(self):
        return {
            'title': _('Delete mailing profile: %s') % self.object
        }


class UserMailingEditView(ViewSingleObjectDynamicFormModelBackendEdit):
    form_class = UserMailerSetupDynamicForm
    model = UserMailer
    object_permission = permission_user_mailer_edit
    pk_url_kwarg = 'mailer_id'
    view_icon = icon_user_mailer_edit

    def get_extra_context(self):
        return {
            'title': _('Edit mailing profile: %s') % self.object
        }

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class UserMailerListView(SingleObjectListView):
    model = UserMailer
    object_permission = permission_user_mailer_view
    view_icon = icon_user_mailer_list

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_user_mailer_list,
            'no_results_main_link': link_user_mailer_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Mailing profiles are email configurations. '
                'Mailing profiles allow sending documents as '
                'attachments or as links via email.'
            ),
            'no_results_title': _('No mailing profiles available'),
            'title': _('Mailing profiles')
        }

    def get_form_schema(self):
        backend_class = self.get_backend_class()
        return {
            'fields': backend_class.fields
        }


class UserMailerTestView(ExternalObjectViewMixin, FormView):
    external_object_class = UserMailer
    external_object_permission = permission_user_mailer_use
    external_object_pk_url_kwarg = 'mailer_id'
    form_class = UserMailerTestForm
    view_icon = icon_user_mailer_test

    def form_valid(self, form):
        self.external_object.test(
            to=form.cleaned_data['email'], user=self.request.user
        )
        messages.success(
            message=_('Test email sent.'), request=self.request
        )
        return super().form_valid(form=form)

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.external_object,
            'submit_label': _('Test'),
            'title': _('Test mailing profile: %s') % self.external_object
        }
