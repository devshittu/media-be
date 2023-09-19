from django.apps import apps
from django.core.management import call_command 
from django.core.management.base import BaseCommand
from autoseed.utils.base_seed import BaseSeed
import importlib
import os

class Command(BaseCommand):
    help = 'Automatically convert and seed data for all apps'

    def handle(self, *args, **kwargs):
        try:
            # Log the start of the command
            self.stdout.write(self.style.SUCCESS('Starting autoseed...'))

            for app in apps.get_app_configs():
                # Log the current app being processed
                self.stdout.write(self.style.SUCCESS(f'Checking app: {app.name}'))

                if os.path.exists(os.path.join(app.path, 'data')):
                    # Log if data directory is found
                    self.stdout.write(self.style.SUCCESS(f"Found 'data' directory in {app.name}"))

                    seed_module = importlib.import_module(f"{app.name}.seeds")
                    for attr_name in dir(seed_module):
                        attr = getattr(seed_module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, BaseSeed) and attr is not BaseSeed:
                            # Log the current model being processed
                            self.stdout.write(self.style.SUCCESS(f'Processing model: {attr_name.replace("Seed", "")}'))
                            
                            # Create an instance of the seed class
                            seed_instance = attr()
                            
                            # Process the data
                            seed_instance.process_data(app.name, attr_name.replace("Seed", "").lower(), app.path)
                            self.stdout.write(self.style.SUCCESS(f"Processed data for {app.name}.{attr_name.replace('Seed', '')}"))

                            # Load the processed data into the database
                            fixture_file = seed_instance.get_output_path(app.path)
                            call_command('loaddata', fixture_file)
                            self.stdout.write(self.style.SUCCESS(f"Loaded data from {fixture_file} into the database"))

                            # attr.process_data(app.name, attr_name.replace("Seed", "").lower(), app.path)
                            # self.stdout.write(self.style.SUCCESS(f"Processed data for {app.name}.{attr_name.replace('Seed', '')}"))


                            # # Load the processed data into the database
                            # fixture_file = attr.get_output_path(app.path)
                            # call_command('loaddata', fixture_file)
                            # self.stdout.write(self.style.SUCCESS(f"Loaded data from {fixture_file} into the database"))

                else:
                    # Log if data directory is not found
                    self.stdout.write(self.style.WARNING(f"No 'data' directory found in {app.name}"))

            # Log the end of the command
            self.stdout.write(self.style.SUCCESS('Autoseed completed!'))

        except Exception as e:
            # Log any exception that occurs
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))


# autoseed/management/commands/autoseed.py