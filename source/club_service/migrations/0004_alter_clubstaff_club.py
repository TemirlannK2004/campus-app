# Generated by Django 4.2.7 on 2023-11-14 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("club_service", "0003_alter_club_club_logo_alter_club_club_members_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clubstaff",
            name="club",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="club_service.club"
            ),
        ),
    ]
