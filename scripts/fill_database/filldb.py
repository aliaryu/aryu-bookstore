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
from apps.product.models import (
    Category,
    Genre,
    Tag,
    Author,
    Book
)
from apps.discount.models import Discount
from apps.comment.models import Comment


from django.core.files import File
from django.utils import timezone
import json


FOLDER = str(Path(__file__).resolve().parent)


def create_user():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        users_data = json.load(file)["user"]
        for user_data in users_data:
            image_path = FOLDER + user_data.pop("image")
            user = User.objects.create_user(** user_data)
            with open(image_path, 'rb') as img_file:
                user.image.save(Path(img_file.name).name, File(img_file))

def create_address():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        address_data = json.load(file)["address"]
        for address in address_data:
            Address.objects.create(** address)

def create_role():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        role_data = json.load(file)["role"]
        for role in role_data:
            Role.objects.create(** role)

def create_staff():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        staff_data = json.load(file)["staff"]
        for staff in staff_data:
            Staff.objects.create(** staff)

def create_discount():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        discount_data = json.load(file)["discount"]
        for discount in discount_data:
            dis = Discount(** discount)
            current_datetime = timezone.now()
            one_year_delta = timezone.timedelta(days=365)
            dis.expire_date = current_datetime + one_year_delta
            dis.save()

def create_category():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        category_data = json.load(file)["category"]
        for category in category_data:
            Category.objects.create(** category)

def create_genre():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        genre_data = json.load(file)["genre"]
        for genre in genre_data:
            Genre.objects.create(** genre)

def create_tag():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        tag_data = json.load(file)["tag"]
        for tag in tag_data:
            Tag.objects.create(** tag)

def create_author():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        authors_data = json.load(file)["author"]
        for author_data in authors_data:
            image_path = FOLDER + author_data.pop("image")
            author = Author.objects.create(** author_data)
            with open(image_path, 'rb') as img_file:
                author.image.save(Path(img_file.name).name, File(img_file))

def create_book():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        books_data = json.load(file)["book"]
        for book_data in books_data:
            image_path = FOLDER + book_data.pop("image")
            authors = book_data.pop("author")
            translators = book_data.pop("translator")
            genres = book_data.pop("genre")
            tags = book_data.pop("tag")
            likes = book_data.pop("like")
            saves = book_data.pop("save")
            book = Book.objects.create(** book_data)
            with open(image_path, 'rb') as img_file:
                book.image.save(Path(img_file.name).name, File(img_file))
            book.author.set(Author.objects.filter(id__in=authors))
            book.translator.set(Author.objects.filter(id__in=translators))
            book.genre.set(Genre.objects.filter(id__in=genres))
            book.tag.set(Tag.objects.filter(id__in=tags))
            book.likes.set(User.objects.filter(id__in=likes))
            book.saves.set(User.objects.filter(id__in=saves))


def create_comment():
    with open(FOLDER + "/data.json", encoding="utf-8") as file:
        comment_data = json.load(file)["comment"]
        for comment in comment_data:
            comment = Comment.objects.create(** comment)


if __name__ == '__main__':
    create_user()
    create_address()
    create_role()
    create_staff()
    create_discount()
    create_category()
    create_genre()
    create_tag()
    create_author()
    create_book()
    create_comment()
    print("Database Filled Successfully :D")