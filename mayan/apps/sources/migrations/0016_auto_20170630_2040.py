from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0015_auto_20170206_0835')
    ]

    operations = [
        migrations.AlterField(
            model_name='sanescanner',
            name='resolution',
            field=models.PositiveIntegerField(
                blank=True,
                help_text='Sets the resolution of the scanned image in '
                'DPI (dots per inch). Typical value is 200. If this option '
                'is not supported by your scanner, leave it blank.',
                null=True, verbose_name='Resolution'
            )
        )
    ]
