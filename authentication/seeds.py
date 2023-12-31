from managekit.utils.base_seed import BaseSeed
from .models import CustomUser
from django.utils import timezone
from utils.helpers import unix_to_datetime
import random
import string
from datetime import timedelta
import datetime
from django.contrib.auth.hashers import make_password


def random_string(length):
    # Generates a random string of the given length using ASCII letters
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


class CustomUserSeed(BaseSeed):
    raw_file = "users"
    model = CustomUser
    COMMON_PASSWORD_HASH = make_password("commonPassword=1")

    @classmethod
    def get_fields(cls, item):
        # Use the class variable for the password
        hashed_password = cls.COMMON_PASSWORD_HASH
        # hashed_password = make_password(item['password'])

        # Convert Unix timestamp to timezone-aware datetime
        print(f"Converting last_login: {item.get('last_login')}")
        last_login_time = (
            unix_to_datetime(item.get("last_login")) if item.get("last_login") else None
        )

        # Random Date of Birth
        end_date = timezone.now().date() - timedelta(days=18 * 365)  # 18 years ago
        start_date = end_date - timedelta(days=52 * 365)  # 70 years ago
        random_dob = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

        # Random Bio
        bios = [
            "I love reading and traveling.",
            "A passionate writer and coffee lover.",
            "Always looking for the next adventure.",
        ]
        random_bio = random.choice(bios)

        # Random has_completed_setup
        random_setup = random.choice([True, False])

        # Check if is_staff is present in the item, default to False if not
        is_staff_value = item.get("is_staff", False)

        gender = "male" if random.random() < 0.5 else "female"
        scrambled_text = random_string(4)
        display_photo_url = (
            f"https://xsgames.co/randomusers/avatar.php?g={gender}&r={scrambled_text}"
        )

        return {
            # "display_name": item["display_name"],
            "display_name": item[
                "display_name"
            ],  # Use 'display_name' instead of 'name'
            "username": item["username"],
            "email": item["email"],
            "password": hashed_password,
            "avatar_url": display_photo_url,
            "roles": item["roles"],
            "date_of_birth": random_dob.isoformat()
            if isinstance(random_dob, datetime.date)
            else random_dob,
            "bio": random_bio,
            "has_completed_setup": random_setup,
            "last_activity": last_login_time.isoformat() if last_login_time else None,
            "is_staff": is_staff_value,  # Add the is_staff field here
        }


# authentication/seeds.py
