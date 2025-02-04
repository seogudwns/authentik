# Generated by Django 4.1.7 on 2023-05-21 11:44

from django.apps.registry import Apps
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def migrate_user_type(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    db_alias = schema_editor.connection.alias
    User = apps.get_model("authentik_core", "User")

    from authentik.core.models import UserTypes

    for user in User.objects.using(db_alias).all():
        user.type = UserTypes.DEFAULT
        if "goauthentik.io/user/service-account" in user.attributes:
            user.type = UserTypes.SERVICE_ACCOUNT
        if "goauthentik.io/user/override-ips" in user.attributes:
            user.type = UserTypes.INTERNAL_SERVICE_ACCOUNT
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("authentik_core", "0029_provider_backchannel_applications_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="type",
            field=models.TextField(
                choices=[
                    ("default", "Default"),
                    ("external", "External"),
                    ("service_account", "Service Account"),
                    ("internal_service_account", "Internal Service Account"),
                ],
                default="default",
            ),
        ),
        migrations.RunPython(migrate_user_type),
    ]
