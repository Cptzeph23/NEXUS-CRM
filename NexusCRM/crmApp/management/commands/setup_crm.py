from django.core.management.base import BaseCommand

from crmApp.models import Pipeline, PipelineStage


class Command(BaseCommand):

    help = "Create default NexusCRM sales pipeline."

    def handle(self, *args, **options):

        pipeline, created = Pipeline.objects.get_or_create(
            name="Standard Sales Pipeline",
            defaults={
                "description":
                    "Default sales pipeline for NexusCRM."
            }
        )

        stages = [
            {
                "name": "New",
                "probability": 10,
                "order": 1,
                "is_closed": False,
                "is_won": False,
            },
            {
                "name": "Contacted",
                "probability": 20,
                "order": 2,
                "is_closed": False,
                "is_won": False,
            },
            {
                "name": "Qualified",
                "probability": 40,
                "order": 3,
                "is_closed": False,
                "is_won": False,
            },
            {
                "name": "Proposal",
                "probability": 60,
                "order": 4,
                "is_closed": False,
                "is_won": False,
            },
            {
                "name": "Negotiation",
                "probability": 80,
                "order": 5,
                "is_closed": False,
                "is_won": False,
            },
            {
                "name": "Won",
                "probability": 100,
                "order": 6,
                "is_closed": True,
                "is_won": True,
            },
            {
                "name": "Lost",
                "probability": 0,
                "order": 7,
                "is_closed": True,
                "is_won": False,
            },
        ]

        for stage_data in stages:

            PipelineStage.objects.update_or_create(
                pipeline=pipeline,
                name=stage_data["name"],
                defaults=stage_data,
            )

        if created:

            self.stdout.write(
                self.style.SUCCESS(
                    "Created Standard Sales Pipeline."
                )
            )

        else:

            self.stdout.write(
                "Standard Sales Pipeline already exists."
            )

        self.stdout.write(
            self.style.SUCCESS(
                "CRM pipeline setup complete."
            )
        )