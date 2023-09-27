from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_b, worker_c

queue_sources = CeleryQueue(
    label=_('Sources'), name='sources', worker=worker_b
)
queue_sources_periodic = CeleryQueue(
    label=_('Sources periodic'), name='sources_periodic', transient=True,
    worker=worker_c
)

queue_sources.add_task_type(
    label=_('Handle source backend action background task'),
    dotted_path='mayan.apps.sources.tasks.task_source_backend_action_background_task'
)
queue_sources_periodic.add_task_type(
    label=_('Check interval source'),
    dotted_path='mayan.apps.sources.tasks.task_source_backend_action_execute'
)
