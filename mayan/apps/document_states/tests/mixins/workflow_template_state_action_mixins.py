from django.db.models import Q

from ...models.workflow_state_action_models import WorkflowStateAction

from ..literals import (
    DOCUMENT_WORKFLOW_LAUNCH_ACTION_CLASS_PATH,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_GENERIC_DOTTED_PATH,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_WHEN
)

from .workflow_instance_mixins import WorkflowInstanceTestMixin
from .workflow_template_state_mixins import WorkflowTemplateStateTestMixin


class WorkflowTemplateStateActionTestMixin(
    WorkflowInstanceTestMixin, WorkflowTemplateStateTestMixin
):
    _test_workflow_template_state_action_path = TEST_WORKFLOW_TEMPLATE_STATE_ACTION_GENERIC_DOTTED_PATH
    auto_add_test_workflow_template_test_document_type = True
    auto_create_test_workflow_template = True
    auto_create_test_workflow_template_state = True
    auto_create_test_document_stub = False
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._test_workflow_template_state_actions = []
        self._create_test_document_stub()

    def _create_test_workflow_template_state_action(
        self, extra_data=None, workflow_state_index=0
    ):
        total_test_workflow_template_state_actions = len(
            self._test_workflow_template_state_actions
        )
        label = '{}_{}'.format(
            TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
            total_test_workflow_template_state_actions
        )

        data = {
            'label': label,
            'backend_path': self._test_workflow_template_state_action_path
        }

        if extra_data:
            data.update(extra_data)

        self._test_workflow_template_state_action = self._test_workflow_template_states[
            workflow_state_index
        ].actions.create(
            **data
        )

        self._test_workflow_template_state_actions.append(
            self._test_workflow_template_state_action
        )

    def _execute_workflow_template_state_action(
        self, klass, context=None, kwargs=None
    ):
        final_context = {
            'workflow_instance': self._test_workflow_instance
        }

        if context:
            final_context.update(context)

        final_kwargs = {
            'model_instance_id': 1  # Fake ID to allow direct instance.
        }

        if kwargs:
            final_kwargs.update(kwargs)

        action = klass(**final_kwargs)

        return action.execute(context=final_context)


class WorkflowTemplateStateActionAPIViewTestMixin(
    WorkflowTemplateStateActionTestMixin
):
    def _request_test_workflow_template_state_action_create_api_view(self):
        pk_list = list(
            WorkflowStateAction.objects.values_list('pk', flat=True)
        )

        total_test_workflow_template_state_actions = len(
            self._test_workflow_template_state_actions
        )
        label = '{}_{}'.format(
            TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
            total_test_workflow_template_state_actions
        )

        data = {
            'label': label,
            'backend_path': self._test_workflow_template_state_action_path
        }

        response = self.post(
            viewname='rest_api:workflow-template-state-action-list',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_state.pk
            }, data=data
        )

        try:
            self._test_workflow_template_state_action = WorkflowStateAction.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowStateAction.DoesNotExist:
            self._test_workflow_template_state_action = None

        return response

    def _request_test_workflow_template_state_action_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-state-action-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_state.pk,
                'workflow_template_state_action_id': self._test_workflow_template_state_action.pk
            }
        )

    def _request_test_workflow_template_state_action_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-state-action-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_state.pk,
                'workflow_template_state_action_id': self._test_workflow_template_state_action.pk
            }
        )

    def _request_test_workflow_template_state_action_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-state-action-list', kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_state.pk
            }
        )

    def _request_test_workflow_template_state_action_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-state-action-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_state.pk,
                'workflow_template_state_action_id': self._test_workflow_template_state_action.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL_EDITED
            }
        )

    def _request_test_workflow_template_state_action_edit_put_api_view(self):
        return self.put(
            viewname='rest_api:workflow-template-state-action-detail',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_state.pk,
                'workflow_template_state_action_id': self._test_workflow_template_state_action.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL_EDITED,
                'backend_path': self._test_workflow_template_state_action_path
            }
        )


class WorkflowTemplateStateActionLaunchViewTestMixin(
    WorkflowTemplateStateActionTestMixin
):
    def _request_document_workflow_template_launch_action_create_view(
        self, extra_data=None
    ):
        data = {
            'enabled': True,
            'label': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
            'when': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_WHEN
        }

        if extra_data:
            data.update(extra_data)

        return self.post(
            viewname='document_states:workflow_template_state_action_create',
            kwargs={
                'workflow_template_state_id': self._test_workflow_template_state.pk,
                'backend_path': DOCUMENT_WORKFLOW_LAUNCH_ACTION_CLASS_PATH
            }, data=data
        )


class WorkflowTemplateStateActionViewTestMixin(
    WorkflowTemplateStateActionTestMixin
):
    def _request_test_workflow_template_state_action_create_get_view(
        self, backend_path
    ):
        return self.get(
            viewname='document_states:workflow_template_state_action_create',
            kwargs={
                'workflow_template_state_id': self._test_workflow_template_state.pk,
                'backend_path': backend_path
            }
        )

    def _request_test_workflow_template_state_action_create_post_view(
        self, backend_path, extra_data=None
    ):
        data = {
            'label': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
            'when': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_WHEN
        }
        if extra_data:
            data.update(extra_data)

        pk_list = list(
            WorkflowStateAction.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='document_states:workflow_template_state_action_create',
            kwargs={
                'workflow_template_state_id': self._test_workflow_template_state.pk,
                'backend_path': backend_path
            }, data=data
        )

        try:
            self._test_workflow_template_state_action = WorkflowStateAction.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowStateAction.DoesNotExist:
            self._test_workflow_template_state_action = None

        return response

    def _request_test_worflow_template_state_action_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_action_delete',
            kwargs={
                'workflow_template_state_action_id': self._test_workflow_template_state_action.pk
            }
        )

    def _request_test_worflow_template_state_action_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_action_edit',
            kwargs={
                'workflow_template_state_action_id': self._test_workflow_template_state_action.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL_EDITED,
                'when': self._test_workflow_template_state_action.when
            }
        )

    def _request_test_worflow_template_state_action_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_state_action_list',
            kwargs={
                'workflow_template_state_id': self._test_workflow_template_state.pk
            }
        )

    def _request_test_workflow_template_state_action_selection_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_action_selection',
            kwargs={
                'workflow_template_state_id': self._test_workflow_template_state.pk
            }, data={
                'klass': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH
            }
        )
