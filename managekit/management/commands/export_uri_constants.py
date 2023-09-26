from django.core.management import call_command
from django.core.management.base import BaseCommand
import re
import json
import os


class Command(BaseCommand):
    help = "Generate API constants from the show_urls command output"

    def add_arguments(self, parser):
        # Specify the lang option
        parser.add_argument(
            "--lang",
            type=str,
            default="ts",
            choices=["ts", "java", "php"],
            help="Output language (default is ts for TypeScript)",
        )

    def handle(self, *args, **kwargs):
        lang = kwargs.get("lang", "ts")

        # Step 1: Generate the app-urls.json using the show_urls command
        with open("app-urls.json", "w") as f:
            call_command("show_urls", format="json", stdout=f)

        # Step 2: Use the generated app-urls.json to create the constants file
        self.generate_constants_from_json("app-urls.json", lang)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated constants for {lang}")
        )

    def generate_constants_from_json(self, json_file, lang="ts"):
        with open(json_file, "r") as f:
            data = json.load(f)

        written_constants = set()  # Keep track of written constants to avoid duplicates

        if lang == "ts":
            filename = "api-constants.ts"
            declaration_format = f'export const URI{{}} = "{{}}";\n'
        elif lang == "java":
            filename = "APIConstants.java"
            declaration_format = f'public static final String URI{{}} = "{{}}";\n'
        elif lang == "php":
            filename = "api-constants.php"
            declaration_format = f'const URI{{}} = "{{}}";\n'
        else:
            filename = "api-constants.txt"
            declaration_format = 'URI{} = "{}"\n'

        with open(filename, "w") as f:
            for entry in data:
                url = entry.get("url")
                if url and url.startswith("/api"):
                    constant_name_suffix = url[4:].replace("/", "_").upper()
                    constant_name_suffix = constant_name_suffix.replace(
                        "-", "_"
                    ).rstrip("_")

                    for match in re.finditer(r"<([^>]+)>", constant_name_suffix):
                        _, part_name = match.group(1).split(":")
                        replace_with = f"_BY_{part_name.upper()}"
                        constant_name_suffix = constant_name_suffix.replace(
                            match.group(0), replace_with
                        )

                    constant_name_suffix = constant_name_suffix.replace("__", "_")
                    formatted_url = re.sub(r"<[^:]+:([^>]+)>", r"{{\1}}", url)

                    # Removing the '/api' prefix from the URL
                    formatted_url = formatted_url[4:]

                    constant_declaration = declaration_format.format(
                        constant_name_suffix, formatted_url
                    )

                    if constant_declaration not in written_constants:
                        f.write(constant_declaration)
                        written_constants.add(constant_declaration)

        os.remove(json_file)
