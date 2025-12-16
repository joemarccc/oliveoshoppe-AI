from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
