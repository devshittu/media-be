import requests
import random
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.utils import timezone
from utils.helpers import unix_to_datetime
from stories.models import Story
from multimedia.models import Multimedia
from managekit.utils.base_seed import BaseSeed
from authentication.seeds import CustomUserSeed
from stories.seeds import StorySeed


class MultimediaSeed(BaseSeed):
    raw_file = "multimedia"
    model = Multimedia
    dependencies = [StorySeed, CustomUserSeed]  # Assuming these seeds exist

    @classmethod
    def get_fields(cls, item):
        current_time = timezone.now().isoformat()
        # Fetch a random image from Unsplash
        random_id = get_random_string(length=12)
        image_width = 600
        image_height = 320
        # image_url = f"https://source.unsplash.com/random/{image_width}x{image_height}?sig={random_id}"

        # Fetch the story instance
        story = Story.objects.get(id=item["story"])

        # Use the story's category title in the Unsplash URL
        category_title = story.category.title if story.category else "random"
        image_url = f"https://source.unsplash.com/random/{image_width}x{image_height}?{category_title}&sig={random_id}"

        # response = requests.get(image_url)

        # Random Bio
        captions = [
            "Exploring the vibrant colors of street art in the city's heart",
            "A moment of tranquility: Morning yoga by the serene lakeside",
            "Culinary delights: A journey through the local food festival",
            "Urban oasis: Discovering hidden green spaces in the metropolis",
            "Fashion on the streets: Trends spotted in the downtown buzz",
            "The art of pottery: Crafting beauty with hands and clay",
            "Weekend market stroll: A treasure trove of local crafts",
            "Sunset escapades: Capturing the city skyline at dusk",
            "A cyclist's adventure through scenic trails and paths",
            "Café culture: Savoring the ambience of quaint downtown coffee shops",
        ]

        random_caption = random.choice(captions)
        # if response.status_code == 200:
        #     # Create a new Multimedia instance for each story
        #     for story in Story.objects.all():
        #         multimedia = cls.model()
        #         multimedia.file.save(
        #             f"{random_id}.jpg", ContentFile(response.content), save=False
        #         )
        #         multimedia.media_type = "photo"  # or other types based on your logic
        #         multimedia.user = story.user  # or assign a random user
        #         multimedia.story = story
        #         multimedia.save()
        # else:
        #     raise Exception("Failed to download image from Unsplash")

        return {
            "caption": random_caption,
            "user": item["user"],
            "story": item["story"],
            "media_type": "photo",
            "media_url": image_url,
            "created_at": current_time,
            "updated_at": current_time,
        }

    # ... rest of the class ...


# multimedia/seeds.py
