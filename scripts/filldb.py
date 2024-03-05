from pathlib import Path
import sys, os, django

BASE_DIR = Path(__file__).resolve().parent.parent 
sys.path.append(str(BASE_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
) ; django.setup()


from apps.user.models import (
    User,
    Address,
    Role,
    Staff
)

from django.core.files import File
import json


FOLDER = str(Path(__file__).resolve().parent)


def create_user():
    with open(FOLDER + "/data.json") as file:
        users_data = json.load(file)["user"]
        for user_data in users_data:
            image_path = FOLDER + user_data.pop("image")
            user = User.objects.create_user(** user_data)
            with open(image_path, 'rb') as img_file:
                user.image.save(Path(img_file.name).name, File(img_file))





if __name__ == '__main__':
    create_user()