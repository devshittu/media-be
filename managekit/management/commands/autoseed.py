import importlib
import os
from django.conf import settings
from django.apps import apps
from django.core.management import call_command
from django.core.management.base import CommandError, BaseCommand
from managekit.utils.base_seed import BaseSeed


class Command(BaseCommand):
    help = "Automatically convert and seed data for all apps"

    def build_dependency_graph(self):
        graph = {}
        for app in apps.get_app_configs():
            # Only process apps that are in the CUSTOM_APPS list
            if app.name in settings.CUSTOM_APPS:
                try:
                    seed_module = importlib.import_module(f"{app.name}.seeds")
                    for attr_name in dir(seed_module):
                        attr = getattr(seed_module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, BaseSeed)
                            and attr is not BaseSeed
                        ):
                            graph[attr] = getattr(attr, "dependencies", [])
                except ImportError:
                    # If the seeds module doesn't exist, just continue to the next app
                    continue
        return graph

    def topological_sort(self, graph):
        visited = set()
        visiting = set()  # Nodes that are currently being visited
        order = []

        def visit(node):
            if node in visiting:
                raise CommandError(f"Circular dependency detected: {node}")
            if node not in visited:
                visiting.add(node)
                visited.add(node)
                for neighbor in graph[node]:
                    visit(neighbor)
                visiting.remove(node)
                order.append(node)

        for node in graph:
            if node not in visited:
                visit(node)

        return order

    def process_seed(self, app, seed_class):
        self.stdout.write(
            self.style.SUCCESS(
                f'Processing model: {seed_class.__name__.replace("Seed", "")}'
            )
        )

        # Create an instance of the seed class
        seed_instance = seed_class()

        # Process the data
        seed_instance.process_data(
            app.name, seed_class.__name__.replace("Seed", "").lower(), app.path
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Processed data for {app.name}.{seed_class.__name__.replace('Seed', '')}"
            )
        )

        # Load the processed data into the database
        try:
            fixture_file = seed_instance.get_output_path(app.path)
            call_command("loaddata", fixture_file)
            self.stdout.write(
                self.style.SUCCESS(f"Loaded data from {fixture_file} into the database")
            )
        except Exception as e:
            # If there's an error, add the seed_class to the retry queue
            self.retry_queue.append((app, seed_class))
            self.stdout.write(
                self.style.WARNING(
                    f"Error loading data for {app.name}.{seed_class.__name__}. Reason: {str(e)}. Will retry later."
                )
            )

    def handle(self, *args, **kwargs):

        settings.SEEDING = True
        self.retry_queue = (
            []
        )  # This will store BaseSeed subclasses that need to be retried

        graph = self.build_dependency_graph()
        order = self.topological_sort(graph)

        for SeedClass in order:
            app = apps.get_app_config(SeedClass.model._meta.app_label)
            self.process_seed(app, SeedClass)

        # Retry for seeds in the retry queue
        max_retries = 3  # You can adjust this number based on your needs
        for _ in range(max_retries):
            if not self.retry_queue:
                break  # If the retry queue is empty, we're done

            self.stdout.write(
                self.style.SUCCESS(f"Retrying for {len(self.retry_queue)} seeds...")
            )
            seeds_to_retry = self.retry_queue.copy()
            self.retry_queue.clear()  # Clear the retry queue for this iteration

            for app, seed_class in seeds_to_retry:
                self.process_seed(app, seed_class)

        if self.retry_queue:
            # If there are still seeds left in the retry queue after all retries, log an error
            failed_seeds = ", ".join(
                [
                    f"{app.name}.{seed_class.__name__}"
                    for app, seed_class in self.retry_queue
                ]
            )
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to load data for {failed_seeds} after {max_retries} retries."
                )
            )

        # Log the end of the command
        self.stdout.write(self.style.SUCCESS("Autoseed completed!"))
        settings.SEEDING = False


# managekit/management/commands/autoseed.py
