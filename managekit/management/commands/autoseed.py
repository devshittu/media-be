from django.apps import apps
from django.core.management import call_command
from django.core.management.base import CommandError, BaseCommand
from managekit.utils.base_seed import BaseSeed
import importlib
import os


class ListOutput:
    def __init__(self):
        self.data = []

    def write(self, s):
        self.data.append(s)

    def getvalue(self):
        return "\n".join(self.data)


class UnmigratedMigrationsError(CommandError):
    pass

# def check_for_unmigrated_migrations():
#     # Capture the output of the showmigrations command
#     output = ListOutput()
#     call_command("showmigrations", stdout=output, stderr=output)
#     output_str = output.getvalue()
#     print(f"Processed data for {output_str}")

#     # Check for any lines that don't start with "[X]", which indicates an unmigrated migration

#     for line in output_str.splitlines():
#         line = line.strip()  # Remove leading/trailing whitespace
#         if (
#             line
#             and "_" in line
#             and not line.startswith("[X]")
#             and any(char.isdigit() for char in line)
#         ):
#             print(f"Unmigrated: {line}")  # Print the unmigrated line for debugging
#             raise UnmigratedMigrationsError(
#                 "There are unmigrated migrations. Please run 'python manage.py migrate' before using autoseed."
#             )


class Command(BaseCommand):
    help = "Automatically convert and seed data for all apps"

    def handle(self, *args, **kwargs):
        # Check for unmigrated migrations
        # check_for_unmigrated_migrations()

        retry_queue = []  # This will store BaseSeed subclasses that need to be retried

        def process_seed(app, seed_class):
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
                    self.style.SUCCESS(
                        f"Loaded data from {fixture_file} into the database"
                    )
                )
                
            except Exception as e:
                # If there's an error, add the seed_class to the retry queue
                retry_queue.append((app, seed_class))
                self.stdout.write(
                    self.style.WARNING(
                        f"Error loading data for {app.name}.{seed_class.__name__}. Reason: {str(e)}. Will retry later."
                    )
                )


        # Process all apps and their seeds
        for app in apps.get_app_configs():
            self.stdout.write(self.style.SUCCESS(f"Checking app: {app.name}"))
            if os.path.exists(os.path.join(app.path, "data")):
                self.stdout.write(
                    self.style.SUCCESS(f"Found 'data' directory in {app.name}")
                )
                seed_module = importlib.import_module(f"{app.name}.seeds")
                for attr_name in dir(seed_module):
                    attr = getattr(seed_module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, BaseSeed)
                        and attr is not BaseSeed
                    ):
                        process_seed(app, attr)
            else:
                self.stdout.write(
                    self.style.WARNING(f"No 'data' directory found in {app.name}")
                )

        # Retry for seeds in the retry queue
        max_retries = 3  # You can adjust this number based on your needs
        for _ in range(max_retries):
            if not retry_queue:
                break  # If the retry queue is empty, we're done

            self.stdout.write(
                self.style.SUCCESS(f"Retrying for {len(retry_queue)} seeds...")
            )
            seeds_to_retry = retry_queue.copy()
            retry_queue.clear()  # Clear the retry queue for this iteration

            for app, seed_class in seeds_to_retry:
                process_seed(app, seed_class)

        if retry_queue:
            # If there are still seeds left in the retry queue after all retries, log an error
            failed_seeds = ", ".join(
                [f"{app.name}.{seed_class.__name__}" for app, seed_class in retry_queue]
            )
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to load data for {failed_seeds} after {max_retries} retries."
                )
            )

        # Log the end of the command
        self.stdout.write(self.style.SUCCESS("Autoseed completed!"))


# autoseed/management/commands/autoseed.py
