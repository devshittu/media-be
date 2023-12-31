import json
import os
from django.core.exceptions import FieldDoesNotExist


class BaseSeed:
    raw_file = None  # Can still be overridden at the class level if needed
    output_file = None
    model = None  # This should be set to the actual Django model
    fields = ["__all__"]  # Default behavior: use all fields
    pk_field = "id"  # Default primary key field

    def get_fields(self, item):
        """Fetch fields from the raw data based on the 'fields' attribute."""
        if self.fields == ["__all__"]:
            return {key: value for key, value in item.items() if key != self.pk_field}
        else:
            return {field: item[field] for field in self.fields if field in item}

    def validate_fields(self, fields):
        """Validate if the fields exist in the model."""
        for field in fields:
            try:
                self.model._meta.get_field(field)
            except FieldDoesNotExist:
                raise ValueError(
                    f"Field '{field}' does not exist in model '{self.model.__name__}'"
                )

    def get_raw_path(self, app_path):
        if not self.raw_file:
            raise ValueError(f"'raw_file' must be set in {self.__class__.__name__}")
        return os.path.join(app_path, "data", "raw", f"{self.raw_file}.json")

    def get_output_path(self, app_path):
        if self.output_file:
            return os.path.join(
                app_path, "data", "processed", f"{self.output_file}.json"
            )
        return os.path.join(
            app_path, "data", "processed", f"{self.raw_file}_processed.json"
        )

    def process_data(self, app_name, model_name, app_path):
        if not os.path.exists(self.get_raw_path(app_path)):
            raise FileNotFoundError(f"'{self.get_raw_path(app_path)}' does not exist")

        with open(self.get_raw_path(app_path), "r") as infile:
            raw_data = json.load(infile)

        processed_data = []
        for item in raw_data:
            fields = self.get_fields(item)
            self.validate_fields(fields.keys())
            processed_item = {
                "model": f"{app_name}.{model_name}",
                "pk": int(item[self.pk_field]),
                "fields": fields,
            }
            processed_data.append(processed_item)

        # Ensure the output directory exists
        output_dir = os.path.dirname(self.get_output_path(app_path))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the processed data to the output file
        with open(self.get_output_path(app_path), "w") as outfile:
            json.dump(processed_data, outfile, indent=4)


# managekit/utils/base_seed.py
