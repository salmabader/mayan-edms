from mayan.apps.testing.tests.base import MayanMigratorTestCase


class SourceBackendPathMigrationTestCase(MayanMigratorTestCase):
    migrate_from = ('sources', '0028_auto_20210905_0558')
    migrate_to = (
        'source_staging_folders', '0001_update_source_backend_paths'
    )

    def prepare(self):
        Source = self.old_state.apps.get_model(
            app_label='sources', model_name='Source'
        )

        Source.objects.create(
            backend_path='mayan.apps.sources.source_backends.staging_folder_backends.SourceBackendStagingFolder',
            label='test source staging folder'
        )

    def test_source_backend_path_updates(self):
        Source = self.old_state.apps.get_model(
            app_label='sources', model_name='Source'
        )

        self.assertEqual(
            Source.objects.get(label='test source staging folder').backend_path,
            'mayan.apps.source_staging_folders.source_backends.staging_folder_backends.SourceBackendStagingFolder'
        )
