from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):

    help = "Create default NexusCRM roles."

    roles = [
        "Administrator",
        "Manager",
        "Sales Representative",
        "Support",
        "Viewer",
    ]

    def handle(self, *args, **options):

        for role in self.roles:

            group, created = Group.objects.get_or_create(
                name=role
            )

            if created:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created role: {role}"
                    )
                )

            else:

                self.stdout.write(
                    f"Role already exists: {role}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "NexusCRM roles are ready."
            )
        )