from celery import shared_task
from django.core.files.storage import default_storage
from django.apps import apps
from PIL import Image
import imageio
from pydub import AudioSegment
import logging
import traceback
import subprocess
import json


logger = logging.getLogger(__name__)


@shared_task
def process_multimedia(multimedia_id):
    # Get the multimedia object
    Multimedia = apps.get_model("multimedia", "Multimedia")
    try:
        multimedia = Multimedia.objects.get(id=multimedia_id)
        if multimedia.media_type == "audio":
            generate_waveform.delay(multimedia_id)
        optimize_media.delay(multimedia_id)
        create_thumbnail.delay(multimedia_id)
    except Multimedia.DoesNotExist:
        pass  # Handle the case where the multimedia object does not exist


@shared_task
def generate_waveform(multimedia_id):
    logger.info(f"Starting to generate waveform for multimedia ID {multimedia_id}")

    # Get the multimedia object
    Multimedia = apps.get_model("multimedia", "Multimedia")
    multimedia = Multimedia.objects.get(id=multimedia_id)

    if multimedia.media_type == "audio":
        try:
            logger.info(f"multimedia.file.path: {multimedia.file.path}")
            # Generate waveform data using audiowaveform
            waveform_output = subprocess.run(
                [
                    "audiowaveform",
                    "-i",
                    multimedia.file.path,
                    "-b",
                    "8",
                    "-z",
                    "3000",
                    "--output-format",
                    "json",
                ],
                capture_output=True,
                text=True,
            )

            # Log the stdout and stderr of the subprocess
            logger.info(f"audiowaveform stdout: {waveform_output.stdout}")
            logger.info(f"audiowaveform stderr: {waveform_output.stderr}")

            # Check if the subprocess returned an error
            if waveform_output.returncode != 0:
                logger.error(
                    f"audiowaveform command failed with return code {waveform_output.returncode}"
                )
                return

            # Parse the JSON part of the output
            waveform_data_json = waveform_output.stdout.strip().split("\n")[
                -1
            ]  # Get the last line containing JSON data
            waveform_data = json.loads(waveform_data_json)

            # Extract amplitude data
            amplitude_data = waveform_data.get("data")

            if amplitude_data:
                # Generate time data based on the length of amplitude data
                sample_rate = waveform_data.get("sample_rate", 44100)
                duration = len(amplitude_data) / sample_rate
                time_step = duration / len(amplitude_data)
                time_data = [i * time_step for i in range(len(amplitude_data))]

                # Combine time and amplitude data
                amplitude_time_data = [
                    {"time": t, "amplitude": a}
                    for t, a in zip(time_data, amplitude_data)
                ]

                # Save the amplitude against time data in the metadata field
                multimedia.metadata = {"amplitude_time_data": amplitude_time_data}
                multimedia.save()

                # # Generate the media URL using the object's filename
                # media_url = multimedia.file.url

                # # Update the media URL for audio files
                # multimedia.media_url = media_url
                # multimedia.save(update_fields=["media_url"])

                logger.info(
                    f"Waveform data saved to metadata for multimedia ID {multimedia_id}"
                )
            else:
                logger.error("No amplitude data found in the waveform output.")

        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error generating waveform: {e}")
            logger.error(
                f"Exception in generate_waveform task for multimedia ID {multimedia_id}: {e}"
            )
            logger.error(traceback.format_exc())  # Log full traceback


@shared_task
def optimize_media(multimedia_id):
    Multimedia = apps.get_model("multimedia", "Multimedia")  # Dynamic model retrieval
    multimedia = Multimedia.objects.get(id=multimedia_id)
    # multimedia = Multimedia.objects.get(id=multimedia_id)
    try:
        if multimedia.media_type == "photo":
            with default_storage.open(multimedia.file.name, "rb") as f:
                img = Image.open(f)
                img = img.convert("RGB")
                if img.height > 3000 or img.width > 3000:
                    output_size = (3000, 3000)
                    img.thumbnail(output_size)
                img.save(multimedia.file.path, "JPEG")
        elif multimedia.media_type == "audio":
            audio = AudioSegment.from_file(multimedia.file.path)
            audio = audio.set_channels(1).set_frame_rate(22050)
            audio.export(multimedia.file.path, format="mp3", bitrate="64k")
        # Add optimization logic for other media types if needed
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error optimizing media: {e}")


@shared_task
def create_thumbnail(multimedia_id):
    Multimedia = apps.get_model("multimedia", "Multimedia")  # Dynamic model retrieval
    multimedia = Multimedia.objects.get(id=multimedia_id)
    # multimedia = Multimedia.objects.get(id=multimedia_id)
    try:
        if multimedia.media_type in ["photo", "video"]:
            thumbnail_path = multimedia.file.name.replace("media_files", "thumbnails")
            if multimedia.media_type == "photo":
                with default_storage.open(multimedia.file.name, "rb") as f:
                    img = Image.open(f)
                    img.thumbnail((300, 300))
                    img.save(default_storage.path(thumbnail_path), "JPEG")
            elif multimedia.media_type == "video":
                reader = imageio.get_reader(multimedia.file.path)
                img_array = reader.get_next_data()
                img = Image.fromarray(img_array)
                img.thumbnail((300, 300))
                img.save(default_storage.path(thumbnail_path), "JPEG")
            multimedia.thumbnail = default_storage.open(thumbnail_path, "rb")
            multimedia.save()
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error creating thumbnail: {e}")


# multimedia/tasks.py
