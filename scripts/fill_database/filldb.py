from pathlib import Path
import sys, os, django

BASE_DIR = Path(__file__).resolve().parent.parent.parent
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

def create_address():
    with open(FOLDER + "/data.json") as file:
        address_data = json.load(file)["address"]
        for address in address_data:
            Address.objects.create(** address)

def create_role():
    with open(FOLDER + "/data.json") as file:
        role_data = json.load(file)["role"]
        for role in role_data:
            Role.objects.create(** role)

def create_staff():
    with open(FOLDER + "/data.json") as file:
        staff_data = json.load(file)["staff"]
        for staff in staff_data:
            Staff.objects.create(** staff)






if __name__ == '__main__':
    # create_user()
    # create_address()
    # create_role()
    create_staff()