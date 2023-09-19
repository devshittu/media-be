# Autoseed README Guide

## Introduction

Autoseed is a Django utility that automates the process of converting raw data into Django fixtures and seeding them into the database. It scans through each app in your Django project, checks for a `data` directory, processes the raw data, and then loads it into the database.

## Prerequisites

- Django project with apps that have a `data` directory containing raw data in JSON format.
- Each app's `data` directory should have a `raw` sub-directory containing the raw JSON files.

## Installation

1. Ensure the `autoseed` directory is in your Django project or is installed as a package.
2. Add `'autoseed'` to the `INSTALLED_APPS` list in your Django project's settings.

## Usage

### 1. Setting up your models for autoseeding

For each model you want to autoseed, create a corresponding seed class in a `seeds.py` file within the app. This seed class should inherit from `BaseSeed` and define the following:

- `raw_file`: The name of the raw data file (without the `.json` extension).
- `model`: The Django model that corresponds to the data.

Optionally, you can also define:

- `fields`: A list of fields you want to extract from the raw data. By default, it uses all fields.
- `output_file`: The name of the output file where processed data will be saved. By default, it uses the format `{raw_file}_processed.json`.

### 2. Running the autoseed command

To run the autoseed command:

```bash
python manage.py autoseed
```

This command will:

1. Go through each app in your Django project.
2. Check for a `data` directory.
3. Process the raw data based on the seed classes defined in `seeds.py`.
4. Load the processed data into the database.

## Examples

Let's say you have an app named `authentication` with a model `CustomUser`. You have raw data in `authentication/data/raw/users.json`.

1. Create a `seeds.py` file in the `authentication` app.
2. Define your seed class:

```python
from autoseed.utils.base_seed import BaseSeed
from .models import CustomUser

class CustomUserSeed(BaseSeed):
    raw_file = 'users'
    model = CustomUser

    @classmethod
    def get_fields(cls, item):
        return {
            'name': item['name'],
            'username': item['username'],
            'email': item['email'],
            'password': item['password'],
            ...
        }
```

3. Run the autoseed command:

```bash
python manage.py autoseed
```

This will process the raw data in `users.json`, create a processed JSON file in `authentication/data/processed/`, and then load this data into the `CustomUser` model in the database.

## Conclusion

Autoseed simplifies the process of seeding data into your Django database. By defining simple seed classes and placing your raw data in the right directories, you can automate the conversion and loading of data with a single command.