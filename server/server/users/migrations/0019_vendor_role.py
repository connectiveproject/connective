# Generated by Django 3.1.14 on 2022-04-03 10:07

from django.db import migrations


def do_nothing(apps, schema_editor):
    pass


def add_vendor_role(apps, schema_editor):
    Vendor = apps.get_model("users", "Vendor")

    for vendor in Vendor.objects.filter(user_type="VENDOR"):

        if (
            hasattr(vendor, "organization_member")
            and vendor.organization_member
            and vendor.organization_member.organization
        ):
            print(f"Vendor ID={vendor.id}, email={vendor.email}")
            organization = vendor.organization_member.organization
            if vendor.roles.filter(role_code="VENDOR_ADMIN").exists():
                print("VENDOR_ADMIN role already exists")
            else:
                vendor.roles.create(
                    role_code="VENDOR_ADMIN",
                    organization=organization,
                    site=vendor.site,
                )
                print("VENDOR_ADMIN applyed successfully")
        else:
            print(f"Could not find organization for vendor {vendor.id}")


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0018_coordinator_role"),
    ]

    operations = [migrations.RunPython(add_vendor_role, reverse_code=do_nothing)]
