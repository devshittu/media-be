import pytest
from django.core.management import call_command
from authentication.models import CustomUser
from autoseed.utils.base_seed import BaseSeed
import os
import json

@pytest.mark.django_db
def test_autoseed_command():
    # Run the autoseed command
    call_command('autoseed')

    # Check if the data was loaded correctly
    user = CustomUser.objects.get(id=1)
    assert user.name == "Test User"
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_base_seed_process_data():
    # Create an instance of the seed class
    seed = BaseSeed()
    seed.raw_file = 'users_test'
    seed.model = CustomUser

    # Mock the app path
    app_path = 'authentication'

    # Process the data
    seed.process_data('authentication', 'customuser', app_path)

    # Check if the processed file exists
    output_path = seed.get_output_path(app_path)
    assert os.path.exists(output_path)

    # Check if the processed data is correct
    with open(output_path, 'r') as f:
        data = json.load(f)
    assert data[0]['model'] == 'authentication.customuser'
    assert data[0]['pk'] == 21
    assert data[0]['fields']['name'] == "Test User"
