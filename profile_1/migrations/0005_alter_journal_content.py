from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profile_1", "0004_alter_skill_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="journal",
            name="content",
            field=models.TextField(help_text="Full article content (HTML is supported)"),
        ),
    ]
