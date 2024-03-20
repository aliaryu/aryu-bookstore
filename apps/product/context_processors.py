from .models import Category


def categories(request):
    categories = Category.objects.filter(cat_parent__isnull=True)
    return {"categories": categories}
